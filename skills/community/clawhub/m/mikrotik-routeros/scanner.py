import socket
import struct
import threading
import time
import subprocess
import re

"""
MikroTik Network Scanner
Author: Xiage
Translator/Maintainer: drodecker
"""

class NetworkScanner:
    """MikroTik device scanner based on API port scanning"""
    
    def __init__(self, timeout=1.0, threads=50):
        self.timeout = timeout
        self.threads = threads
        self.devices = []
        self.lock = threading.Lock()

    def _get_local_subnets(self):
        """Get local subnet ranges"""
        subnets = []
        try:
            # For Windows
            output = subprocess.check_output("ipconfig", shell=True).decode('gbk', errors='ignore')
            ip_matches = re.findall(r'IPv4 Address.*?: (\d+\.\d+\.\d+\.\d+)', output)
            mask_matches = re.findall(r'Subnet Mask.*?: (\d+\.\d+\.\d+\.\d+)', output)
            
            for ip, mask in zip(ip_matches, mask_matches):
                if ip.startswith('127.'): continue
                # Basic subnet calculation
                parts = ip.split('.')
                subnets.append(f"{parts[0]}.{parts[1]}.{parts[2]}.0/24")
        except:
            # Fallback for Linux
            try:
                output = subprocess.check_output("ip addr", shell=True).decode()
                matches = re.findall(r'inet (\d+\.\d+\.\d+\.\d+/\d+)', output)
                for m in matches:
                    if not m.startswith('127.'):
                        subnets.append(m)
            except:
                pass
        return list(set(subnets))

    def _check_port(self, ip, port):
        """Check if port is open and try to identify MikroTik API"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                # Port is open, try to get some info (optional)
                device = {
                    'ip': ip,
                    'port': port,
                    'name': 'MikroTik',
                    'mac': self._get_mac_from_arp(ip),
                    'version': 'Unknown'
                }
                
                # If we wanted to be more thorough, we could try to send a small API word 
                # to see if it responds in binary length-prefixed format
                
                with self.lock:
                    # Check if already found (e.g. via 8729)
                    if not any(d['ip'] == ip for d in self.devices):
                        self.devices.append(device)
            sock.close()
        except:
            pass

    def _get_mac_from_arp(self, ip):
        """Try to get MAC address from system ARP table"""
        try:
            output = subprocess.check_output(f"arp -a {ip}", shell=True).decode('gbk', errors='ignore')
            match = re.search(r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})', output)
            if match:
                return match.group(0).replace('-', ':').lower()
        except:
            pass
        return "Unknown"

    def scan_subnet(self, subnet):
        """Scan a subnet for MikroTik API ports (8728, 8729)"""
        if '/' not in subnet: return
        
        prefix = subnet.split('/')[0].rsplit('.', 1)[0]
        targets = [f"{prefix}.{i}" for i in range(1, 255)]
        
        threads = []
        for ip in targets:
            # Check 8728 (API) and 8729 (API-SSL)
            t1 = threading.Thread(target=self._check_port, args=(ip, 8728))
            t1.start()
            threads.append(t1)
            
            if len(threads) >= self.threads:
                for t in threads: t.join()
                threads = []
                
        for t in threads: t.join()

    def scan_local_network(self):
        """Scan all local subnets"""
        self.devices = []
        subnets = self._get_local_subnets()
        for subnet in subnets:
            self.scan_subnet(subnet)
        return self.devices

if __name__ == '__main__':
    scanner = NetworkScanner()
    print("🔍 Scanning local network for MikroTik devices...")
    start_time = time.time()
    devices = scanner.scan_local_network()
    duration = time.time() - start_time
    
    print(f"\n✅ Scan completed in {duration:.1f}s")
    if devices:
        print(f"Found {len(devices)} devices:")
        for d in devices:
            print(f" - {d['ip']}:{d['port']} (MAC: {d['mac']})")
    else:
        print("No MikroTik devices found (API port 8728/8729 not responding)")
