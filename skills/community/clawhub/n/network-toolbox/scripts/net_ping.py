#!/usr/bin/env python3
"""Check host connectivity with ping timing using raw sockets."""

import argparse, socket, struct, sys, time, os

def ping(host, count=4, timeout=2):
    """Simple ping using ICMP echo via raw socket."""
    try:
        dest_ip = socket.gethostbyname(host)
    except socket.gaierror:
        return [("ERROR", f"Cannot resolve {host}")]

    results = []
    # Try system ping first (more reliable)
    import subprocess
    try:
        # -c count, -W timeout (seconds) on Linux
        start = time.time()
        r = subprocess.run(
            ['ping', '-c', str(count), '-W', str(timeout), host],
            capture_output=True, text=True, timeout=timeout * count + 2
        )
        elapsed = time.time() - start
        output = r.stdout + r.stderr
        # Parse summary
        for line in output.split('\n'):
            if 'packets transmitted' in line:
                results.append(line.strip())
            elif 'rtt min/avg/max' in line or 'round-trip' in line:
                results.append(line.strip())
        if not results:
            if r.returncode == 0:
                results.append(f"OK ({count} pings to {host}, {elapsed:.1f}s)")
            else:
                results.append(f"FAIL: {host} unreachable")
        return results
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback: TCP connect test
    results.append(f"TCP connect test to {host} ({dest_ip}):")
    for port in [80, 443, 22]:
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((dest_ip, port))
            s.close()
            elapsed = (time.time() - start) * 1000
            status = "OPEN" if result == 0 else "CLOSED"
            results.append(f"  Port {port}: {status} ({elapsed:.0f}ms)")
        except Exception as e:
            results.append(f"  Port {port}: ERROR ({e})")

    return results

def main():
    p = argparse.ArgumentParser(description='Ping/connectivity test')
    p.add_argument('host', help='Hostname or IP address')
    p.add_argument('--count', '-c', type=int, default=4, help='Number of pings')
    p.add_argument('--timeout', '-t', type=int, default=2, help='Timeout per ping (s)')
    args = p.parse_args()

    results = ping(args.host, args.count, args.timeout)
    for line in results:
        print(line)

if __name__ == '__main__':
    main()
