#!/usr/bin/env python3
"""WHOIS domain lookup using WHOIS protocol (port 43). No external dependency."""

import argparse, json, socket, sys, re

WHOIS_SERVERS = {
    'com': 'whois.verisign-grs.com',
    'net': 'whois.verisign-grs.com',
    'org': 'whois.pir.org',
    'io': 'whois.nic.io',
    'co': 'whois.nic.co',
    'app': 'whois.nic.google',
    'dev': 'whois.nic.google',
    'info': 'whois.afilias.net',
    'me': 'whois.nic.me',
    'xyz': 'whois.nic.xyz',
    'cloud': 'whois.nic.cloud',
    'ai': 'whois.nic.ai',
    'my': 'whois.mynic.my',
    'sg': 'whois.sgnic.sg',
}

def get_tld(domain):
    parts = domain.split('.')
    if len(parts) >= 2:
        return parts[-1].lower()
    return None

def whois_lookup(domain, server=None, timeout=15):
    tld = get_tld(domain)
    if not server:
        server = WHOIS_SERVERS.get(tld, 'whois.verisign-grs.com')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((server, 43))
        sock.send(f"{domain}\r\n".encode())
        response = b''
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        sock.close()
        text = response.decode('utf-8', errors='replace')
        # Remove excessive blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text[:5000]  # Limit output size
    except socket.timeout:
        return f"Timeout connecting to {server}"
    except socket.gaierror:
        return f"Cannot resolve WHOIS server: {server}"
    except Exception as e:
        return f"WHOIS lookup failed: {e}"

def main():
    p = argparse.ArgumentParser(description='WHOIS domain lookup')
    p.add_argument('domain', help='Domain name (e.g., example.com)')
    p.add_argument('--server', help='WHOIS server (auto-detected from TLD by default)')
    p.add_argument('--json', action='store_true', help='JSON output')
    args = p.parse_args()

    domain = args.domain.lower().strip()
    tld = get_tld(domain)

    print(f"WHOIS Lookup: {domain}")
    if tld in WHOIS_SERVERS:
        print(f"WHOIS Server: {WHOIS_SERVERS[tld]} (auto-detected for .{tld})")
    print()

    result = whois_lookup(domain, args.server)

    if args.json:
        print(json.dumps({'domain': domain, 'raw': result}, indent=2))
    else:
        print(result)

if __name__ == '__main__':
    main()
