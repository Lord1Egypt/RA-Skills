#!/usr/bin/env python3
"""TCP port scanner with timeout and concurrent support."""

import argparse, socket, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_port(host, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    start = time.time()
    try:
        result = s.connect_ex((host, port))
        elapsed = (time.time() - start) * 1000
        if result == 0:
            # Try to get service banner
            try:
                s.send(b'GET / HTTP/1.0\r\n\r\n')
                banner = s.recv(256).decode('utf-8', errors='replace').strip()[:80]
            except:
                banner = ''
            s.close()
            return (port, 'OPEN', f"{elapsed:.0f}ms", banner)
        else:
            s.close()
            return (port, 'CLOSED', '', '')
    except Exception as e:
        s.close()
        return (port, 'ERROR', '', str(e))

def parse_ports(port_arg, port_range):
    ports = set()
    if port_arg:
        for part in port_arg.split(','):
            part = part.strip()
            if '-' in part:
                a, b = part.split('-', 1)
                ports.update(range(int(a), int(b) + 1))
            else:
                ports.add(int(part))
    if port_range:
        a, b = port_range.split('-', 1)
        ports.update(range(int(a), int(b) + 1))
    return sorted(ports)

def main():
    p = argparse.ArgumentParser(description='TCP port scanner')
    p.add_argument('host', help='Hostname or IP')
    p.add_argument('--ports', help='Port list: 22,80,443 or 1-1024')
    p.add_argument('--range', help='Port range: 1-1000')
    p.add_argument('--timeout', type=float, default=1.0, help='Connection timeout (s)')
    p.add_argument('--threads', type=int, default=50, help='Concurrent threads')
    args = p.parse_args()

    ports = parse_ports(args.ports, args.range)
    if not ports:
        ports = list(range(1, 1025))

    try:
        host_ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"ERROR: Cannot resolve {args.host}")
        sys.exit(1)

    print(f"Scanning {args.host} ({host_ip}) — {len(ports)} ports ({args.timeout}s timeout)")
    print(f"{'Port':>6}  {'Status':>6}  {'Time':>6}  {'Banner'}")
    print('-' * 60)

    open_ports = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(check_port, args.host, port, args.timeout): port for port in ports}
        for future in as_completed(futures):
            port, status, timing, banner = future.result()
            if status == 'OPEN':
                open_ports.append(port)
                banner_str = f"  {banner}" if banner else ''
                print(f"{port:>6}  {status:>6}  {timing:>6}  {banner_str}")
            elif status == 'ERROR':
                print(f"{port:>6}  {status:>6}  {'':>6}")

    print(f"\nScan complete: {len(open_ports)} open / {len(ports)} ports")
    if open_ports:
        print(f"Open ports: {', '.join(str(p) for p in sorted(open_ports))}")

if __name__ == '__main__':
    main()
