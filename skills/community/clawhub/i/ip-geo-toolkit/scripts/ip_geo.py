#!/usr/bin/env python3
"""IP Geolocation Toolkit — look up IP geolocation, your public IP, WHOIS info, and bulk lookups.

No external dependencies required. Uses free APIs (ip-api.com, ipify).

Usage:
  python3 ip_geo.py lookup 8.8.8.8
  python3 ip_geo.py lookup 8.8.8.8 1.1.1.1
  python3 ip_geo.py myip
  python3 ip_geo.py bulk --input ips.txt
  python3 ip_geo.py lookup 8.8.8.8 --json
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import time
import socket


def get_public_ip():
    """Get the current public IP address."""
    apis = [
        "https://api.ipify.org?format=json",
        "https://api64.ipify.org?format=json",
        "https://httpbin.org/ip",
    ]
    for url in apis:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "IPGeoToolkit/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return data.get("ip") or data.get("origin", "").split(",")[0].strip()
        except (urllib.error.URLError, OSError, json.JSONDecodeError):
            continue
    return None


def lookup_ip(ip_address):
    """Look up geolocation for a single IP address using ip-api.com."""
    url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "IPGeoToolkit/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "fail":
                return {"error": data.get("message", "lookup failed"), "query": ip_address}
            return data
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
        return {"error": str(e), "query": ip_address}


def lookup_batch(ips):
    """Batch lookup using ip-api.com batch endpoint (max 100 per request)."""
    results = []
    # ip-api.com batch: POST up to 100 IPs
    for i in range(0, len(ips), 100):
        batch = ips[i:i+100]
        url = "http://ip-api.com/batch?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        payload = json.dumps(batch).encode("utf-8")
        try:
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "User-Agent": "IPGeoToolkit/1.0",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                results.extend(data)
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
            for ip in batch:
                results.append({"error": str(e), "query": ip})
        # Rate limit: 15 requests per minute for free tier
        if i + 100 < len(ips):
            time.sleep(1)
    return results


def reverse_dns(ip_address):
    """Perform reverse DNS lookup."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except (socket.herror, socket.gaierror, OSError):
        return None


def format_result(data, show_json=False):
    """Format a single lookup result for display."""
    if show_json:
        return json.dumps(data, indent=2)

    if "error" in data:
        return f"❌ {data.get('query', 'unknown')}: {data['error']}"

    lines = []
    ip = data.get("query", "unknown")
    lines.append(f"📍 {ip}")
    lines.append(f"   Location:  {data.get('city', '?')}, {data.get('regionName', '?')}, {data.get('country', '?')} ({data.get('countryCode', '?')})")
    lines.append(f"   Coords:    {data.get('lat', '?')}, {data.get('lon', '?')}")
    lines.append(f"   Timezone:  {data.get('timezone', '?')}")
    lines.append(f"   ZIP:       {data.get('zip', '?')}")
    lines.append(f"   ISP:       {data.get('isp', '?')}")
    lines.append(f"   Org:       {data.get('org', '?')}")
    lines.append(f"   AS:        {data.get('as', '?')}")

    # Try reverse DNS
    rdns = reverse_dns(ip)
    if rdns:
        lines.append(f"   rDNS:      {rdns}")

    return "\n".join(lines)


def validate_ip(ip_str):
    """Basic validation for IPv4/IPv6 address or domain."""
    ip_str = ip_str.strip()
    if not ip_str:
        return False
    # Accept IPs and domains
    return True


def main():
    parser = argparse.ArgumentParser(
        description="IP Geolocation Toolkit — lookup IP location, ISP, and network info",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s lookup 8.8.8.8
  %(prog)s lookup 8.8.8.8 1.1.1.1 --json
  %(prog)s myip
  %(prog)s myip --json
  %(prog)s bulk --input ips.txt
  %(prog)s bulk --input ips.txt --json
"""
    )
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # lookup
    lk_p = sub.add_parser("lookup", help="Look up geolocation for one or more IPs")
    lk_p.add_argument("ips", nargs="+", help="IP addresses or domains to look up")
    lk_p.add_argument("--json", action="store_true", help="Output as JSON")

    # myip
    my_p = sub.add_parser("myip", help="Show your public IP and geolocation")
    my_p.add_argument("--json", action="store_true", help="Output as JSON")

    # bulk
    bk_p = sub.add_parser("bulk", help="Bulk lookup from a file (one IP per line)")
    bk_p.add_argument("--input", required=True, help="Path to file with IPs (one per line, or - for stdin)")
    bk_p.add_argument("--json", action="store_true", help="Output as JSON")
    bk_p.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "myip":
        ip = get_public_ip()
        if not ip:
            print("❌ Could not determine public IP", file=sys.stderr)
            sys.exit(1)

        data = lookup_ip(ip)
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(f"🌐 Your public IP: {ip}\n")
            print(format_result(data))

    elif args.command == "lookup":
        results = []
        for ip in args.ips:
            if not validate_ip(ip):
                print(f"⚠️  Skipping invalid input: {ip}", file=sys.stderr)
                continue
            data = lookup_ip(ip)
            results.append(data)
            if not args.json:
                print(format_result(data))
                print()
            # Rate limit
            if len(args.ips) > 1:
                time.sleep(0.5)

        if args.json:
            if len(results) == 1:
                print(json.dumps(results[0], indent=2))
            else:
                print(json.dumps(results, indent=2))

    elif args.command == "bulk":
        # Load IPs
        try:
            if args.input == "-":
                raw = sys.stdin.read()
            else:
                with open(args.input, "r") as f:
                    raw = f.read()
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        ips = [line.strip() for line in raw.strip().split("\n") if line.strip() and not line.startswith("#")]
        if not ips:
            print("No IPs found in input", file=sys.stderr)
            sys.exit(1)

        print(f"🔍 Looking up {len(ips)} IPs...\n")
        results = lookup_batch(ips)

        output_lines = []
        for data in results:
            if args.json:
                pass  # handled below
            else:
                output_lines.append(format_result(data))
                output_lines.append("")

        if args.json:
            output_text = json.dumps(results, indent=2)
        else:
            output_text = "\n".join(output_lines)

        if args.output:
            with open(args.output, "w") as f:
                f.write(output_text + "\n")
            print(f"✅ Results written to {args.output} ({len(results)} IPs)")
        else:
            print(output_text)


if __name__ == "__main__":
    main()
