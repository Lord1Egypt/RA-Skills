#!/usr/bin/env python3
"""DNS resolution checker — tests 5 domains against multiple DNS servers."""

import json
import socket
import sys
import time

DOMAINS = [
    "google.com",
    "cloudflare.com",
    "github.com",
    "amazon.com",
    "reddit.com",
]

DNS_SERVERS = {
    "google": "8.8.8.8",
    "cloudflare": "1.1.1.1",
    "system": None,  # uses OS resolver
}

SLOW_THRESHOLD_MS = 200  # flag lookups slower than this


def resolve_via_system(domain):
    """Resolve using the OS resolver (getaddrinfo)."""
    start = time.monotonic()
    try:
        results = socket.getaddrinfo(domain, None)
        elapsed_ms = (time.monotonic() - start) * 1000
        ips = list({r[4][0] for r in results})
        return {"success": True, "ips": ips, "latency_ms": round(elapsed_ms, 2)}
    except socket.gaierror as e:
        elapsed_ms = (time.monotonic() - start) * 1000
        return {"success": False, "error": str(e), "latency_ms": round(elapsed_ms, 2)}


def resolve_via_server(domain, server_ip):
    """
    Resolve using a specific DNS server via raw UDP query.
    Builds a minimal DNS A-record query packet.
    """
    import struct

    def build_query(domain):
        tid = 0x1234
        flags = 0x0100  # standard query, recursion desired
        qdcount = 1
        header = struct.pack(">HHHHHH", tid, flags, qdcount, 0, 0, 0)
        labels = b""
        for part in domain.split("."):
            enc = part.encode()
            labels += bytes([len(enc)]) + enc
        labels += b"\x00"
        qtype = 1   # A record
        qclass = 1  # IN
        question = labels + struct.pack(">HH", qtype, qclass)
        return header + question

    def skip_name(data, offset):
        """Skip a DNS name (handles pointers). Returns new offset."""
        while offset < len(data):
            length = data[offset]
            if length == 0:
                return offset + 1
            if (length & 0xC0) == 0xC0:
                # Pointer: 2-byte value
                return offset + 2
            offset += length + 1
        return offset

    def parse_response(data):
        """Extract IPs from DNS response (A records only)."""
        try:
            qdcount = struct.unpack(">H", data[4:6])[0]
            ancount = struct.unpack(">H", data[6:8])[0]
            if ancount == 0:
                return []
            # Skip header (12 bytes) and questions
            offset = 12
            for _ in range(qdcount):
                offset = skip_name(data, offset)
                offset += 4  # QTYPE + QCLASS
            ips = []
            for _ in range(ancount):
                if offset >= len(data):
                    break
                offset = skip_name(data, offset)
                if offset + 10 > len(data):
                    break
                rtype, rclass, ttl, rdlength = struct.unpack(">HHIH", data[offset:offset + 10])
                offset += 10
                if rtype == 1 and rdlength == 4:  # A record
                    ip = ".".join(str(b) for b in data[offset:offset + 4])
                    ips.append(ip)
                offset += rdlength
            return ips
        except Exception:
            return []

    start = time.monotonic()
    try:
        query = build_query(domain)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3.0)
        sock.sendto(query, (server_ip, 53))
        response, _ = sock.recvfrom(512)
        sock.close()
        elapsed_ms = (time.monotonic() - start) * 1000
        ips = parse_response(response)
        return {
            "success": True,
            "ips": ips,
            "latency_ms": round(elapsed_ms, 2),
        }
    except socket.timeout:
        elapsed_ms = (time.monotonic() - start) * 1000
        return {"success": False, "error": "timeout", "latency_ms": round(elapsed_ms, 2)}
    except Exception as e:
        elapsed_ms = (time.monotonic() - start) * 1000
        return {"success": False, "error": str(e), "latency_ms": round(elapsed_ms, 2)}


def run_dns_checks():
    results = {}
    for server_name, server_ip in DNS_SERVERS.items():
        results[server_name] = {}
        for domain in DOMAINS:
            if server_ip is None:
                r = resolve_via_system(domain)
            else:
                r = resolve_via_server(domain, server_ip)
            r["slow"] = r["latency_ms"] > SLOW_THRESHOLD_MS
            results[server_name][domain] = r

    # Summary
    summary = {
        "total_queries": len(DNS_SERVERS) * len(DOMAINS),
        "failures": 0,
        "slow_queries": 0,
        "server_avg_ms": {},
    }
    for server_name, domains in results.items():
        latencies = []
        for domain, r in domains.items():
            if not r["success"]:
                summary["failures"] += 1
            if r.get("slow"):
                summary["slow_queries"] += 1
            latencies.append(r["latency_ms"])
        if latencies:
            summary["server_avg_ms"][server_name] = round(
                sum(latencies) / len(latencies), 2
            )

    return {"checks": results, "summary": summary}


if __name__ == "__main__":
    data = run_dns_checks()
    print(json.dumps(data, indent=2))
