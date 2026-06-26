#!/usr/bin/env python3
"""Fast TCP port scanner with service detection and banner grabbing."""

import argparse
import json
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Top 100 most commonly open ports
TOP_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 119, 135, 139, 143, 161, 179, 389,
    443, 445, 465, 514, 515, 587, 631, 636, 993, 995, 1080, 1433, 1434,
    1521, 1723, 2049, 2082, 2083, 2086, 2087, 2095, 2096, 2222, 3000,
    3128, 3306, 3389, 4443, 5000, 5432, 5900, 5901, 5984, 6379, 6667,
    7001, 7002, 8000, 8008, 8080, 8443, 8888, 9000, 9090, 9200, 9300,
    10000, 11211, 27017, 27018, 28017, 50000, 50070, 50075,
]

# Default scan: top 20 most common
DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995,
                 1433, 3306, 3389, 5432, 5900, 6379, 8080, 8443]

COMMON_SERVICES = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 67: "DHCP", 68: "DHCP", 69: "TFTP", 80: "HTTP",
    110: "POP3", 111: "RPC", 119: "NNTP", 123: "NTP", 135: "MSRPC",
    139: "NetBIOS", 143: "IMAP", 161: "SNMP", 179: "BGP", 389: "LDAP",
    443: "HTTPS", 445: "SMB", 465: "SMTPS", 514: "Syslog", 515: "LPD",
    587: "SMTP-SUB", 631: "IPP", 636: "LDAPS", 993: "IMAPS", 995: "POP3S",
    1080: "SOCKS", 1433: "MSSQL", 1434: "MSSQL-UDP", 1521: "Oracle",
    1723: "PPTP", 2049: "NFS", 2222: "SSH-ALT", 3000: "Dev-Server",
    3128: "Squid", 3306: "MySQL", 3389: "RDP", 4443: "HTTPS-ALT",
    5000: "Dev-Server", 5432: "PostgreSQL", 5900: "VNC", 5901: "VNC",
    5984: "CouchDB", 6379: "Redis", 6667: "IRC", 7001: "WebLogic",
    8000: "HTTP-ALT", 8008: "HTTP-ALT", 8080: "HTTP-Proxy",
    8443: "HTTPS-ALT", 8888: "HTTP-ALT", 9000: "PHP-FPM",
    9090: "Prometheus", 9200: "Elasticsearch", 9300: "ES-Transport",
    10000: "Webmin", 11211: "Memcached", 27017: "MongoDB",
    27018: "MongoDB", 28017: "MongoDB-Web", 50000: "SAP",
}


def parse_ports(port_spec: str) -> list[int]:
    """Parse port specification: single, range, or comma-separated."""
    ports = set()
    for part in port_spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(p for p in ports if 1 <= p <= 65535)


def grab_banner(sock: socket.socket, port: int) -> str:
    """Try to grab a banner from an open port."""
    try:
        # Some services send a banner immediately
        sock.settimeout(1.5)
        # For HTTP-like services, send a minimal request
        if port in (80, 8080, 8000, 8008, 8888, 443, 8443, 4443):
            sock.sendall(b"HEAD / HTTP/1.0\r\nHost: target\r\n\r\n")
        banner = sock.recv(256)
        return banner.decode("utf-8", errors="replace").strip().split("\n")[0][:120]
    except Exception:
        return ""


def scan_port(host: str, port: int, timeout: float, banner: bool = True) -> dict | None:
    """Scan a single port. Returns result dict if open, None if closed."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            service = COMMON_SERVICES.get(port, "unknown")
            banner_text = ""
            if banner:
                banner_text = grab_banner(sock, port)
            return {
                "port": port,
                "state": "open",
                "service": service,
                "banner": banner_text,
            }
    except (socket.timeout, socket.error):
        pass
    finally:
        sock.close()
    return None


def scan_host(host: str, ports: list[int], timeout: float, workers: int, banner: bool) -> dict:
    """Scan all specified ports on a host."""
    # Resolve hostname first
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        return {"host": host, "ip": None, "error": f"Cannot resolve hostname '{host}'", "open_ports": []}

    open_ports = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(scan_port, ip, p, timeout, banner): p for p in ports}
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)

    open_ports.sort(key=lambda x: x["port"])
    return {"host": host, "ip": ip, "ports_scanned": len(ports), "open_ports": open_ports}


def format_text(result: dict) -> str:
    """Format scan results as human-readable text."""
    lines = []
    if result.get("error"):
        return f"Error: {result['error']}"

    lines.append(f"Scan results for {result['host']} ({result['ip']})")
    lines.append(f"Ports scanned: {result['ports_scanned']}")
    lines.append(f"Open ports: {len(result['open_ports'])}")
    lines.append("")

    if not result["open_ports"]:
        lines.append("No open ports found.")
        return "\n".join(lines)

    lines.append(f"{'PORT':<8} {'STATE':<8} {'SERVICE':<16} {'BANNER'}")
    lines.append("-" * 60)
    for p in result["open_ports"]:
        banner_str = p["banner"][:50] if p["banner"] else ""
        lines.append(f"{p['port']:<8} {p['state']:<8} {p['service']:<16} {banner_str}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fast TCP port scanner with service detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s example.com
  %(prog)s 192.168.1.1 --ports 1-1024
  %(prog)s 10.0.0.1 --ports 22,80,443
  %(prog)s example.com --top 100 --format json
""",
    )
    parser.add_argument("host", help="Target hostname or IP address")
    parser.add_argument("--ports", help="Ports to scan: single, range (1-1024), or comma-separated (22,80,443)")
    parser.add_argument("--top", type=int, help="Scan top N most common ports (max 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds (default: 1.0)")
    parser.add_argument("--workers", type=int, default=100, help="Max concurrent connections (default: 100)")
    parser.add_argument("--no-banner", action="store_true", help="Skip banner grabbing (faster)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")
    args = parser.parse_args()

    # Determine ports to scan
    if args.ports:
        try:
            ports = parse_ports(args.ports)
        except ValueError:
            print(f"Error: Invalid port specification '{args.ports}'", file=sys.stderr)
            sys.exit(1)
    elif args.top:
        n = min(args.top, len(TOP_PORTS))
        ports = TOP_PORTS[:n]
    else:
        ports = DEFAULT_PORTS

    if not ports:
        print("Error: No valid ports to scan", file=sys.stderr)
        sys.exit(1)

    result = scan_host(args.host, ports, args.timeout, args.workers, not args.no_banner)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_text(result))


if __name__ == "__main__":
    main()
