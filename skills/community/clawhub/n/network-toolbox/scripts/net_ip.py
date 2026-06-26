#!/usr/bin/env python3
"""Get public IP address and local network interface info."""

import argparse, json, socket, sys, urllib.request

def get_public_ip():
    services = [
        'https://api.ipify.org',
        'https://icanhazip.com',
        'https://ifconfig.me/ip',
    ]
    for service in services:
        try:
            req = urllib.request.Request(service, headers={'User-Agent': 'curl/8.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                ip = resp.read().decode().strip()
                return ip
        except:
            continue
    return None

def get_local_info():
    hostname = socket.gethostname()
    info = {'hostname': hostname}

    # Get all IPs
    ips = []
    try:
        addrs = socket.getaddrinfo(hostname, None)
        seen = set()
        for addr in addrs:
            ip = addr[4][0]
            if ip not in seen and not ip.startswith('127.'):
                seen.add(ip)
                ips.append(ip)
    except:
        pass
    info['local_ips'] = ips

    # Default route IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        info['default_ip'] = s.getsockname()[0]
        s.close()
    except:
        pass

    return info

def main():
    p = argparse.ArgumentParser(description='IP address and network info')
    p.add_argument('--json', action='store_true', help='JSON output')
    args = p.parse_args()

    local = get_local_info()
    public = get_public_ip()

    if args.json:
        result = {**local, 'public_ip': public}
        print(json.dumps(result, indent=2))
    else:
        print(f"Hostname:     {local['hostname']}")
        print(f"Public IP:    {public or 'unknown'}")
        if local.get('default_ip'):
            print(f"Default IP:   {local['default_ip']}")
        if local.get('local_ips'):
            print(f"Local IPs:    {', '.join(local['local_ips'])}")

if __name__ == '__main__':
    main()
