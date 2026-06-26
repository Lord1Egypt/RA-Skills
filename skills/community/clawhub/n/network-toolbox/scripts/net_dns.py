#!/usr/bin/env python3
"""DNS record lookup using socket.getaddrinfo and /etc/hosts."""

import argparse, socket, sys

def get_records(host, rtype):
    results = []
    try:
        ip = socket.gethostbyname(host)
        results.append(("A", host, ip))
    except socket.gaierror:
        pass

    # Try IPv6
    try:
        info = socket.getaddrinfo(host, None, socket.AF_INET6)
        for addr in info:
            results.append(("AAAA", host, addr[4][0]))
    except socket.gaierror:
        pass

    # Get canonical name
    try:
        cname = socket.getfqdn(host)
        if cname and cname != host:
            results.append(("CNAME", host, cname))
    except:
        pass

    return results

def resolve_host(host):
    """Resolve host to all IP addresses."""
    results = {}
    try:
        info = socket.getaddrinfo(host, None)
        for addr in info:
            family = addr[0]
            ip = addr[4][0]
            fname = "IPv4" if family == socket.AF_INET else "IPv6"
            results[ip] = fname
    except socket.gaierror as e:
        return {"error": str(e)}
    return results

def main():
    p = argparse.ArgumentParser(description='DNS record lookup')
    p.add_argument('host', help='Hostname to look up')
    p.add_argument('--type', choices=['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'ALL'], default='ALL',
                   help='DNS record type')
    p.add_argument('--all', action='store_true', help='Show all available records')
    args = p.parse_args()

    # Basic DNS resolution
    results = resolve_host(args.host)
    print(f"DNS Lookup: {args.host}")
    print(f"Target record type: {args.type}")
    print()

    if 'error' in results:
        print(f"ERROR: {results['error']}")
        sys.exit(1)

    print("Resolved addresses:")
    for ip, family in results.items():
        print(f"  {family}: {ip}")

    print()
    print(f"Hostname: {args.host}")
    print(f"Canonical: {socket.getfqdn(args.host)}")

    # Try reverse DNS
    for ip, _ in list(results.items())[:1]:
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            print(f"Reverse:   {ip} → {hostname}")
        except:
            pass

    print()
    print("NOTE: Full MX/NS/TXT records require dnspython (`pip install dnspython`).")
    print("Basic stdlib resolution provides A, AAAA, CNAME, and PTR records only.")

if __name__ == '__main__':
    main()
