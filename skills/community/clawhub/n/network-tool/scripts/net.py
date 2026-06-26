#!/usr/bin/env python3
"""Network Tool - Diagnostic and testing utilities."""

import argparse
import socket
import subprocess
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional, List


def ping_host(host: str, count: int = 4, timeout: int = 5) -> bool:
    """Ping a host."""
    print(f"Pinging {host} ({count} times)...")
    
    cmd = ['ping', '-c', str(count), '-W', str(timeout), host]
    
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout * count + 5
        )
        print(result.stdout)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Timeout: {host} did not respond")
        return False
    except FileNotFoundError:
        print("Error: ping command not found")
        return False


def curl_request(
    url: str,
    method: str = 'GET',
    data: Optional[str] = None,
    headers: Optional[dict] = None,
    follow_redirects: bool = True
) -> bool:
    """Make HTTP request (simplified curl)."""
    print(f"{method} {url}")
    
    req = urllib.request.Request(url, method=method)
    
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)
    
    if data:
        if isinstance(data, dict):
            data = urllib.parse.urlencode(data)
        req.data = data.encode('utf-8')
    
    try:
        if follow_redirects:
            response = urllib.request.urlopen(req, timeout=30)
        else:
            # Don't follow redirects
            class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None
            
            opener = urllib.request.build_opener(NoRedirectHandler)
            response = opener.open(req, timeout=30)
        
        print(f"\nStatus: {response.status} {response.reason}")
        print(f"Headers: {dict(response.headers)}")
        
        content = response.read().decode('utf-8')
        print(f"\n--- Response ({len(content)} bytes) ---")
        print(content[:2000])  # Limit output
        
        return True
        
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def dns_lookup(hostname: str, record_type: str = 'A') -> bool:
    """DNS lookup."""
    print(f"DNS lookup for {hostname} (type: {record_type})...")
    
    try:
        if record_type == 'A':
            result = socket.gethostbyname(hostname)
            print(f"A record: {result}")
        elif record_type == 'AAAA':
            result = socket.getaddrinfo(hostname, None, socket.AF_INET6)
            for r in result:
                print(f"AAAA: {r[4][0]}")
        elif record_type == 'MX':
            import dns.resolver
            answers = dns.resolver.resolve(hostname, 'MX')
            for rdata in answers:
                print(f"MX: {rdata.exchange} (priority: {rdata.preference})")
        elif record_type == 'TXT':
            import dns.resolver
            answers = dns.resolver.resolve(hostname, 'TXT')
            for rdata in answers:
                print(f"TXT: {rdata.strings}")
        else:
            print(f"Unsupported record type: {record_type}")
            return False
        return True
    except socket.gaierror as e:
        print(f"DNS Error: {e}")
        return False
    except ImportError:
        print("Note: For MX/TXT records, install dnspython: pip install dnspython")
        # Fallback to basic
        try:
            result = socket.gethostbyname(hostname)
            print(f"A record: {result}")
            return True
        except:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def check_port(host: str, port: int, timeout: int = 5) -> bool:
    """Check if a port is open."""
    print(f"Checking {host}:{port}...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"✓ Port {port} is OPEN")
            return True
        else:
            print(f"✗ Port {port} is CLOSED")
            return False
    except socket.timeout:
        print(f"✗ Timeout connecting to {host}:{port}")
        return False
    except socket.gaierror:
        print(f"✗ Unknown host: {host}")
        return False
    finally:
        sock.close()


def scan_ports(host: str, start_port: int, end_port: int, timeout: float = 0.5) -> List[int]:
    """Scan a range of ports."""
    print(f"Scanning {host} ports {start_port}-{end_port}...")
    
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        try:
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"✓ Port {port} is OPEN")
                open_ports.append(port)
        except:
            pass
        finally:
            sock.close()
    
    print(f"\nScan complete. Found {len(open_ports)} open ports")
    return open_ports


def get_public_ip() -> bool:
    """Get public IP address."""
    print("Getting public IP...")
    
    services = [
        'https://api.ipify.org',
        'https://ifconfig.me/ip',
        'https://icanhazip.com'
    ]
    
    for service in services:
        try:
            response = urllib.request.urlopen(service, timeout=10)
            ip = response.read().decode('utf-8').strip()
            print(f"Public IP: {ip}")
            return True
        except:
            continue
    
    print("Could not determine public IP")
    return False


def speed_test() -> bool:
    """Simple speed test."""
    print("Running speed test...")
    
    # Test download speed
    test_urls = [
        ('https://speed.cloudflare.com/__down?bytes=1000000', 'Cloudflare'),
    ]
    
    for url, name in test_urls:
        print(f"\nTesting {name}...")
        try:
            start = time.time()
            response = urllib.request.urlopen(url, timeout=30)
            data = response.read()
            end = time.time()
            
            size_mb = len(data) / (1024 * 1024)
            duration = end - start
            speed_mbps = (size_mb * 8) / duration
            
            print(f"Downloaded: {size_mb:.2f} MB in {duration:.2f}s")
            print(f"Speed: {speed_mbps:.2f} Mbps")
            return True
        except Exception as e:
            print(f"Error: {e}")
    
    return False


def main():
    parser = argparse.ArgumentParser(description='Network diagnostic tool')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Ping
    ping_parser = subparsers.add_parser('ping', help='Ping a host')
    ping_parser.add_argument('host', help='Host to ping')
    ping_parser.add_argument('--count', '-c', type=int, default=4, help='Number of pings')
    ping_parser.add_argument('--timeout', '-t', type=int, default=5, help='Timeout in seconds')
    
    # Curl
    curl_parser = subparsers.add_parser('curl', help='Make HTTP request')
    curl_parser.add_argument('url', help='URL to request')
    curl_parser.add_argument('--method', '-X', default='GET', help='HTTP method')
    curl_parser.add_argument('--data', '-d', help='Request body')
    curl_parser.add_argument('--header', '-H', action='append', help='HTTP headers')
    
    # DNS
    dns_parser = subparsers.add_parser('dns', help='DNS lookup')
    dns_parser.add_argument('host', help='Hostname to lookup')
    dns_parser.add_argument('--type', '-t', default='A', help='Record type (A, AAAA, MX, TXT)')
    
    # Port
    port_parser = subparsers.add_parser('port', help='Check single port')
    port_parser.add_argument('host', help='Host')
    port_parser.add_argument('port', type=int, help='Port number')
    port_parser.add_argument('--timeout', '-t', type=int, default=5, help='Timeout')
    
    # Ports
    ports_parser = subparsers.add_parser('ports', help='Scan port range')
    ports_parser.add_argument('host', help='Host')
    ports_parser.add_argument('range', help='Port range (e.g., 80-90)')
    
    # IP
    subparsers.add_parser('ip', help='Get public IP')
    
    # Speed
    subparsers.add_parser('speed', help='Speed test')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        print("\nExamples:")
        print("  net-tool ping google.com")
        print("  net-tool curl https://example.com")
        print("  net-tool dns google.com")
        print("  net-tool port localhost 8080")
        print("  net-tool ports localhost 80-90")
        print("  net-tool ip")
        sys.exit(1)
    
    if args.command == 'ping':
        ping_host(args.host, args.count, args.timeout)
    elif args.command == 'curl':
        headers = {}
        if args.header:
            for h in args.header:
                if ':' in h:
                    k, v = h.split(':', 1)
                    headers[k.strip()] = v.strip()
        curl_request(args.url, args.method, args.data, headers)
    elif args.command == 'dns':
        dns_lookup(args.host, args.type)
    elif args.command == 'port':
        check_port(args.host, args.port, args.timeout)
    elif args.command == 'ports':
        if '-' in args.range:
            start, end = map(int, args.range.split('-'))
            scan_ports(args.host, start, end)
        else:
            print("Error: Range should be like 80-90")
    elif args.command == 'ip':
        get_public_ip()
    elif args.command == 'speed':
        speed_test()


if __name__ == '__main__':
    main()
