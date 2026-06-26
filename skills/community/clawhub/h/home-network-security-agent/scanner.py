import argparse
import json
import subprocess
import requests
import re

def get_network_topology():
    try:
        # Extract default gateway using ip route
        route_out = subprocess.run(['ip', 'route'], capture_output=True, text=True).stdout
        gateway_match = re.search(r'default via ([0-9\.]+)', route_out)
        gateway = gateway_match.group(1) if gateway_match else "Unknown"
        
        # Retrieve public IP
        pub_ip = requests.get('https://ifconfig.me/ip', timeout=5).text.strip()
        
        return json.dumps({"gateway_ip": gateway, "public_ip": pub_ip})
    except Exception as e:
        return json.dumps({"error": str(e)})

def discover_lan_hosts(gateway_ip):
    try:
        # Infer /24 subnet from gateway (e.g., 192.168.1.1 -> 192.168.1.0/24)
        parts = gateway_ip.split('.')
        if len(parts) != 4:
            return json.dumps({"error": "Invalid gateway IP format."})
        
        subnet = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        
        # Run nmap ping sweep
        result = subprocess.run(['nmap', '-sn', subnet], capture_output=True, text=True)
        
        hosts = []
        for line in result.stdout.split('\n'):
            if 'Nmap scan report for' in line:
                hosts.append(line.replace('Nmap scan report for ', '').strip())
                
        return json.dumps({"subnet": subnet, "active_hosts": hosts})
    except Exception as e:
        return json.dumps({"error": str(e)})

def scan_ports_and_vulns(ip_address, scan_type="fast"):
    try:
        # Fast scan (-F) gets top 100 ports. Deep scan (-p-) checks all 65535.
        # -sV determines service/version info for vulnerability mapping by the LLM.
        if scan_type == "deep":
            cmd = ['nmap', '-p-', '-sV', '-T4', ip_address]
        else:
            cmd = ['nmap', '-F', '-sV', ip_address]
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        open_ports = []
        for line in result.stdout.split('\n'):
            if '/tcp' in line and 'open' in line:
                open_ports.append(line.strip())
                
        return json.dumps({"target": ip_address, "scan_type": scan_type, "services_found": open_ports})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True)
    parser.add_argument("--target")
    parser.add_argument("--type", default="fast")
    args = parser.parse_args()

    if args.tool == "get_network_topology":
        print(get_network_topology())
    elif args.tool == "discover_lan_hosts":
        print(discover_lan_hosts(args.target))
    elif args.tool == "scan_ports_and_vulns":
        print(scan_ports_and_vulns(args.target, args.type))
