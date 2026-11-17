#!/usr/bin/env python3
"""Passive Reconnaissance Module — comprehensive OSINT data collection (v3.0.0).

Gathers target intelligence without directly interacting with the target:
  1. Certificate Transparency (crt.sh) — subdomain enumeration
  2. DNS Enumeration — A/AAAA via getaddrinfo, CNAME/MX/NS/TXT/SOA via raw
     DNS queries, zone transfer attempt detection
  3. WHOIS Lookup — IANA referral + TLD-specific whois server query
  4. Technology Stack Detection — HTTP headers, cookies, meta tags, script/CSS
     patterns, CMS fingerprinting
  5. Wayback Machine — CDX API for historical URL discovery
  6. GitHub Dorking — search URL generation for credential/config leaks
  7. Shodan/Censys — API integration points + manual query URL generation
  8. Email Discovery — regex extraction + common format enumeration

Pure Python 3.10+ standard library. Imports load_json/dump_json from utils.py.

Usage (CLI):
  python passive_recon.py --domain example.com
  python passive_recon.py --domain example.com --mode crtsh
  python passive_recon.py --domain example.com --output recon.json
  python passive_recon.py --domain example.com --dns-server 8.8.8.8
  python passive_recon.py --domain example.com --shodan-key $KEY --censys-id $ID --censys-secret $SECRET
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import random
import re
import socket
import ssl
import struct
import sys
import time
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json  # noqa: E402

# =============================================================================
# Constants & Defaults
# =============================================================================

DEFAULT_TIMEOUT = 10.0  # seconds for network operations
DEFAULT_DNS_SERVERS = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]
DEFAULT_RATE_LIMIT = 0.5  # seconds between requests to the same service
WHOIS_IANA = ("whois.iana.org", 43)
CRTSH_URL = "https://crt.sh/?q=%25.{domain}&output=json"
WAYBACK_CDX_URL = "http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&fl=original,timestamp&collapse=urlkey&limit=500"

# DNS record types for raw queries
DNS_A = 1
DNS_NS = 2
DNS_CNAME = 5
DNS_SOA = 6
DNS_MX = 15
DNS_TXT = 16
DNS_AAAA = 28
DNS_AXFR = 252

# Common subdomains to probe even if crt.sh fails
COMMON_SUBDOMAINS = [
    "www", "mail", "remote", "blog", "webmail", "server", "ns1", "ns2",
    "smtp", "secure", "vpn", "m", "shop", "ftp", "dev", "staging", "api",
    "cdn", "admin", "portal", "dashboard", "login", "test", "beta", "app",
    "docs", "support", "status", "auth", "cloud", "db", "git", "jenkins",
    "jira", "wiki", "monitor", "demo", "sandbox", "mobile", "mob", "intranet",
    "assets", "static", "media", "files", "images", "img", "css", "js",
]

# Technology detection patterns
TECH_PATTERNS = {
    "web_server": [
        ("nginx", re.compile(r"(?:Server:\s*nginx)(?:/([\d.]+))?", re.IGNORECASE)),
        ("Apache", re.compile(r"(?:Server:\s*Apache)(?:/([\d.]+))?", re.IGNORECASE)),
        ("IIS", re.compile(r"(?:Server:\s*Microsoft-IIS)(?:/([\d.]+))?", re.IGNORECASE)),
        ("Apache-Coyote", re.compile(r"(?:Server:\s*Apache-Coyote)(?:/([\d.]+))?", re.IGNORECASE)),
        ("CloudFlare", re.compile(r"(?:Server:\s*cloudflare)", re.IGNORECASE)),
        ("LiteSpeed", re.compile(r"(?:Server:\s*LiteSpeed)", re.IGNORECASE)),
        ("Caddy", re.compile(r"(?:Server:\s*Caddy)", re.IGNORECASE)),
        ("Tomcat", re.compile(r"(?:Server:\s*Apache[-\s]Tomcat)", re.IGNORECASE)),
        ("Gunicorn", re.compile(r"(?:Server:\s*gunicorn)", re.IGNORECASE)),
        ("GSE", re.compile(r"(?:Server:\s*gse)", re.IGNORECASE)),
        ("openresty", re.compile(r"(?:Server:\s*openresty)", re.IGNORECASE)),
    ],
    "language": [
        ("PHP", re.compile(r"(?:X-Powered-By:\s*PHP)(?:/([\d.]+))?", re.IGNORECASE)),
        ("ASP.NET", re.compile(r"(?:X-Powered-By:\s*ASP\.NET)", re.IGNORECASE)),
        ("Node.js", re.compile(r"(?:X-Powered-By:\s*Express)", re.IGNORECASE)),
        ("Java", re.compile(r"(?:X-Powered-By:\s*(?:Servlet|JSP|JSF))", re.IGNORECASE)),
        ("Python", re.compile(r"(?:X-Powered-By:\s*(?:Django|Flask|Pyramid))", re.IGNORECASE)),
        ("Ruby", re.compile(r"(?:X-Powered-By:\s*(?:Rails|Sinatra|Rack))", re.IGNORECASE)),
    ],
    "cookies": [
        ("PHPSESSID", re.compile(r"PHPSESSID=([^;]+)", re.IGNORECASE)),
        ("JSESSIONID", re.compile(r"JSESSIONID=([^;]+)", re.IGNORECASE)),
        ("ASP.NET_SessionId", re.compile(r"ASP\.NET_SessionId=([^;]+)", re.IGNORECASE)),
        ("laravel_session", re.compile(r"laravel_session=([^;]+)", re.IGNORECASE)),
        ("django", re.compile(r"csrftoken=([^;]+)", re.IGNORECASE)),
        ("rails", re.compile(r"_session_id=([^;]+)", re.IGNORECASE)),
        ("flask", re.compile(r"(?:session)=([^;]+)", re.IGNORECASE)),
    ],
}

SCRIPT_FRAMEWORKS = [
    ("jQuery", re.compile(r"(?:jquery)[-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE)),
    ("React", re.compile(r"(?:react)(?:\.production)?[.-]([\d.]+)(?:\.min)?\.js", re.IGNORECASE)),
    ("Vue.js", re.compile(r"(?:vue)[-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE)),
    ("Angular", re.compile(r"(?:angular)[-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE)),
    ("Bootstrap", re.compile(r"(?:bootstrap)[-.]([\d.]+)(?:\.min)?\.(?:js|css)", re.IGNORECASE)),
    ("Tailwind CSS", re.compile(r"(?:tailwindcss)[@/-]([\d.]+)", re.IGNORECASE)),
    ("D3.js", re.compile(r"(?:d3)[-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE)),
    ("Lodash", re.compile(r"(?:lodash)[-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE)),
    ("Axios", re.compile(r"(?:axios)[-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE)),
    ("Moment.js", re.compile(r"(?:moment)[-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE)),
    ("Next.js", re.compile(r"/_next/static/", re.IGNORECASE)),
    ("Nuxt.js", re.compile(r"/_nuxt/", re.IGNORECASE)),
]

META_GENERATOR_PATTERNS = [
    ("WordPress", re.compile(r'<meta\s[^>]*name="generator"[^>]*content="WordPress\s*([\d.]*)"', re.IGNORECASE)),
    ("Drupal", re.compile(r'<meta\s[^>]*name="generator"[^>]*content="Drupal\s*([\d.]*)"', re.IGNORECASE)),
    ("Joomla", re.compile(r'<meta\s[^>]*name="generator"[^>]*content="Joomla!?\s*([\d.]*)"', re.IGNORECASE)),
    ("MediaWiki", re.compile(r'<meta\s[^>]*name="generator"[^>]*content="MediaWiki\s*([\d.]*)"', re.IGNORECASE)),
    ("Magento", re.compile(r'<meta\s[^>]*name="generator"[^>]*content="Magento', re.IGNORECASE)),
    ("Ghost", re.compile(r'<meta\s[^>]*name="generator"[^>]*content="Ghost\s*([\d.]*)"', re.IGNORECASE)),
    ("Hugo", re.compile(r'<meta\s[^>]*name="generator"[^>]*content="Hugo\s*([\d.]*)"', re.IGNORECASE)),
    ("Jekyll", re.compile(r'<meta\s[^>]*name="generator"[^>]*content="Jekyll\s*([\d.]*)"', re.IGNORECASE)),
    ("Hexo", re.compile(r'<meta\s[^>]*name="generator"[^>]*content="Hexo', re.IGNORECASE)),
]

CMS_DIRECT_PATTERNS = [
    ("WordPress", re.compile(r"/wp-content/", re.IGNORECASE)),
    ("WordPress", re.compile(r"/wp-includes/", re.IGNORECASE)),
    ("WordPress", re.compile(r"/wp-json/", re.IGNORECASE)),
    ("Drupal", re.compile(r"/sites/default/files/", re.IGNORECASE)),
    ("Drupal", re.compile(r"/sites/all/modules/", re.IGNORECASE)),
    ("Joomla", re.compile(r"/components/com_", re.IGNORECASE)),
    ("Joomla", re.compile(r"/modules/mod_", re.IGNORECASE)),
    ("Magento", re.compile(r"/skin/frontend/", re.IGNORECASE)),
    ("Shopify", re.compile(r"cdn\.shopify\.com", re.IGNORECASE)),
    ("Wix", re.compile(r"static\.wixstatic\.com", re.IGNORECASE)),
]

# Common email patterns for enumeration
EMAIL_PATTERNS = [
    "admin@{domain}", "info@{domain}", "support@{domain}",
    "contact@{domain}", "sales@{domain}", "webmaster@{domain}",
    "hostmaster@{domain}", "postmaster@{domain}", "security@{domain}",
    "abuse@{domain}", "noc@{domain}", "root@{domain}",
    "it@{domain}", "dev@{domain}", "devops@{domain}",
    "hello@{domain}", "team@{domain}", "office@{domain}",
    "help@{domain}", "press@{domain}", "media@{domain}",
    "marketing@{domain}", "privacy@{domain}", "legal@{domain}",
    "finance@{domain}", "hr@{domain}", "jobs@{domain}",
    "ceo@{domain}", "cto@{domain}", "cfo@{domain}",
]

# =============================================================================
# Utility Helpers
# =============================================================================


def _now_iso() -> str:
    """Return current UTC timestamp as ISO-8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _clean_domain(domain: str) -> str:
    """Strip protocol, path, and trailing dot from a domain string."""
    d = domain.strip().lower()
    if "://" in d:
        d = urlparse(d).hostname or d
    return d.rstrip(".")


def _rate_sleep(seconds: float = DEFAULT_RATE_LIMIT) -> None:
    """Sleep to respect rate limits. Short jitter to avoid synchronization."""
    jitter = random.uniform(0, seconds * 0.3)
    time.sleep(seconds + jitter)


def _http_fetch(
    url: str,
    timeout: float = DEFAULT_TIMEOUT,
    headers: dict[str, str] | None = None,
    accept: str = "text/html,application/json,*/*",
) -> tuple[int, dict[str, str], str]:
    """Fetch a URL via urllib, returning (status, headers_dict, body).

    Gracefully degrades: never raises. Returns (0, {}, "") on any error.
    Supports HTTPS with certificate validation disabled for resilience.
    """
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

    req_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": accept,
        "Accept-Language": "en-US,en;q=0.9",
    }
    if headers:
        req_headers.update(headers)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = Request(url, headers=req_headers)
        resp = urlopen(req, timeout=timeout, context=ctx)
        body = resp.read().decode("utf-8", errors="replace")
        headers_dict = {}
        for k, v in resp.getheaders():
            key_lower = k.lower()
            headers_dict[key_lower] = v
        return (resp.getcode(), headers_dict, body)
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        hdrs = {}
        for k, v in (e.headers.items() if e.headers else []):
            hdrs[k.lower()] = v
        return (e.code, hdrs, body)
    except (URLError, OSError, ValueError) as e:
        return (0, {}, str(e))


# =============================================================================
# Certificate Transparency (crt.sh)
# =============================================================================


def crtsh_query(
    domain: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Query crt.sh JSON API for certificate transparency logs.

    Returns:
        {"subdomains": [str], "errors": [str]}
    """
    result: dict[str, Any] = {"subdomains": [], "errors": []}
    clean = _clean_domain(domain)
    url = CRTSH_URL.format(domain=clean)
    _rate_sleep()

    _, headers, body = _http_fetch(url, timeout=timeout, accept="application/json")

    if not body or body.startswith("Traceback") or body.startswith("<"):
        result["errors"].append(f"crt.sh returned non-JSON for {clean}")
        return result

    try:
        entries = json.loads(body)
    except json.JSONDecodeError as e:
        result["errors"].append(f"crt.sh JSON decode error: {e}")
        return result

    if not isinstance(entries, list):
        result["errors"].append("crt.sh returned unexpected data format")
        return result

    seen: set[str] = set()
    for entry in entries:
        for field in ("common_name", "name_value"):
            raw = (entry.get(field) or "").strip()
            if not raw:
                continue
            # name_value can be newline-separated
            for name in raw.split("\n"):
                name = name.strip().lower().rstrip(".")
                if not name or name == clean:
                    continue
                # Filter wildcards
                if name.startswith("*."):
                    name = name[2:]
                if name == clean:
                    continue
                # Accept only names that are subdomains of the target
                if name.endswith("." + clean) or name == clean:
                    if name not in seen:
                        seen.add(name)
                        result["subdomains"].append(name)

    result["subdomains"].sort()
    return result


# =============================================================================
# DNS Enumeration — Raw DNS Client
# =============================================================================


def _encode_dns_name(name: str) -> bytes:
    """Encode a domain name into DNS label-sequence format."""
    result = b""
    for label in name.rstrip(".").split("."):
        label_bytes = label.encode("ascii", errors="replace")
        result += bytes([len(label_bytes)]) + label_bytes
    result += b"\x00"
    return result


def _decode_dns_name(data: bytes, offset: int) -> tuple[str, int]:
    """Decode a DNS name at offset (handles compression pointers).

    Returns (decoded_name, next_offset).
    """
    labels: list[str] = []
    jumped = False
    end_offset = offset
    jumps_left = 10  # prevent pointer loops

    while jumps_left > 0:
        if offset >= len(data):
            break
        length = data[offset]
        if length == 0:
            offset += 1
            if not jumped:
                end_offset = offset
            break
        # Compression pointer (top 2 bits == 0b11)
        if (length & 0xC0) == 0xC0:
            if offset + 1 >= len(data):
                break
            pointer = ((length & 0x3F) << 8) | data[offset + 1]
            if not jumped:
                end_offset = offset + 2
            offset = pointer
            jumped = True
            jumps_left -= 1
            continue
        offset += 1
        if offset + length > len(data):
            break
        labels.append(data[offset:offset + length].decode("ascii", errors="replace"))
        offset += length

    if not jumped:
        end_offset = offset
    return ".".join(labels) if labels else "", end_offset


def _build_dns_query(domain: str, qtype: int) -> bytes:
    """Build a DNS query packet for the given domain and query type."""
    txid = random.randint(0, 0xFFFF)
    flags = 0x0100  # standard query, recursion desired
    header = struct.pack("!HHHHHH", txid, flags, 1, 0, 0, 0)
    question = _encode_dns_name(domain) + struct.pack("!HH", qtype, 1)  # IN class
    return header + question


def _send_dns_udp(
    packet: bytes, server: str, timeout: float = DEFAULT_TIMEOUT
) -> bytes | None:
    """Send a DNS query via UDP and return the response bytes, or None."""
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        sock.sendto(packet, (server, 53))
        response, _ = sock.recvfrom(4096)
        return response
    except (socket.timeout, OSError):
        return None
    finally:
        if sock:
            sock.close()


def _parse_dns_rr(
    data: bytes, offset: int, count: int
) -> tuple[list[dict[str, Any]], int]:
    """Parse `count` resource records from `data` at `offset`.

    Returns (list_of_rr_dicts, new_offset).
    """
    records: list[dict[str, Any]] = []
    for _ in range(count):
        name, offset = _decode_dns_name(data, offset)
        if offset + 10 > len(data):
            break
        rtype, rclass, ttl, rdlength = struct.unpack(
            "!HHIH", data[offset:offset + 10]
        )
        offset += 10
        if offset + rdlength > len(data):
            break
        rdata_bytes = data[offset:offset + rdlength]
        rdata: Any = None

        if rtype == DNS_A and rdlength == 4:
            rdata = socket.inet_ntop(socket.AF_INET, rdata_bytes)
        elif rtype == DNS_AAAA and rdlength == 16:
            rdata = socket.inet_ntop(socket.AF_INET6, rdata_bytes)
        elif rtype in (DNS_CNAME, DNS_NS):
            rdata, _ = _decode_dns_name(data, offset)
        elif rtype == DNS_MX and rdlength >= 3:
            preference = struct.unpack("!H", rdata_bytes[0:2])[0]
            exchange, _ = _decode_dns_name(data, offset + 2)
            rdata = {"preference": preference, "exchange": exchange}
        elif rtype == DNS_TXT:
            txt_parts: list[str] = []
            pos = 0
            while pos < rdlength:
                chunk_len = rdata_bytes[pos]
                pos += 1
                if pos + chunk_len > rdlength:
                    break
                txt_parts.append(
                    rdata_bytes[pos:pos + chunk_len].decode("utf-8", errors="replace")
                )
                pos += chunk_len
            rdata = "".join(txt_parts)
        elif rtype == DNS_SOA:
            mname, off2 = _decode_dns_name(data, offset)
            rname, off3 = _decode_dns_name(data, off2)
            if off3 + 20 <= offset + rdlength:
                serial, refresh, retry, expire, minimum = struct.unpack(
                    "!IIIII", data[off3:off3 + 20]
                )
                rdata = {
                    "mname": mname,
                    "rname": rname,
                    "serial": serial,
                    "refresh": refresh,
                    "retry": retry,
                    "expire": expire,
                    "minimum": minimum,
                }
            else:
                rdata = {"mname": mname, "rname": rname}
        else:
            rdata = base64.b64encode(rdata_bytes).decode("ascii")

        records.append({
            "name": name,
            "type": rtype,
            "ttl": ttl,
            "data": rdata,
        })
        offset += rdlength

    return records, offset


def _parse_dns_response(response: bytes) -> dict[str, Any]:
    """Parse a DNS response packet into structured records."""
    if len(response) < 12:
        return {"error": "response too short", "answers": [], "authorities": []}

    # Header
    _, flags, qdcount, ancount, nscount, arcount = struct.unpack(
        "!HHHHHH", response[0:12]
    )
    rcode = flags & 0x000F
    if rcode != 0:
        rcode_names = {
            1: "FORMERR", 2: "SERVFAIL", 3: "NXDOMAIN",
            4: "NOTIMP", 5: "REFUSED",
        }
        return {
            "error": f"DNS rcode={rcode} ({rcode_names.get(rcode, 'UNKNOWN')})",
            "answers": [], "authorities": [],
        }

    offset = 12

    # Skip question section
    for _ in range(qdcount):
        _, offset = _decode_dns_name(response, offset)
        offset += 4  # QTYPE + QCLASS

    answers, offset = _parse_dns_rr(response, offset, ancount)
    authorities, _ = _parse_dns_rr(response, offset, nscount)

    return {"answers": answers, "authorities": authorities}


_TYPE_NAMES: dict[int, str] = {
    1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 15: "MX", 16: "TXT", 28: "AAAA",
}


def _raw_dns_lookup(
    domain: str, qtype: int, server: str, timeout: float = DEFAULT_TIMEOUT
) -> list[dict[str, Any]]:
    """Perform a single raw DNS query for the given type."""
    try:
        packet = _build_dns_query(domain, qtype)
        response = _send_dns_udp(packet, server, timeout=timeout)
        if response is None:
            return []
        parsed = _parse_dns_response(response)
        return parsed.get("answers", [])
    except Exception:
        return []


def _dns_axfr_attempt(
    domain: str, ns_server: str, timeout: float = 8.0
) -> dict[str, Any]:
    """Attempt a DNS zone transfer (AXFR) via TCP to an authoritative NS.

    Returns {"success": bool, "records": [...], "error": str}.
    """
    result: dict[str, Any] = {"success": False, "records": [], "error": ""}
    sock = None
    try:
        packet = _build_dns_query(domain, DNS_AXFR)
        # Prepend 2-byte length for TCP DNS
        tcp_packet = struct.pack("!H", len(packet)) + packet

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ns_server, 53))
        sock.sendall(tcp_packet)

        all_data = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                all_data += chunk
            except socket.timeout:
                break

        if len(all_data) <= 2:
            result["error"] = "No data received (AXFR likely refused)"
            return result

        # Parse TCP DNS response(s)
        offset = 0
        all_records: list[dict[str, Any]] = []
        while offset + 2 <= len(all_data):
            msg_len = struct.unpack("!H", all_data[offset:offset + 2])[0]
            offset += 2
            if offset + msg_len > len(all_data):
                break
            msg = all_data[offset:offset + msg_len]
            offset += msg_len
            if len(msg) >= 12:
                parsed = _parse_dns_response(msg)
                all_records.extend(parsed.get("answers", []))

        if all_records:
            result["success"] = True
            result["records"] = [
                {**_TYPE_NAMES.get(r["type"], f"TYPE{r['type']}"), "record": r}
                for r in all_records
            ]
        else:
            result["error"] = "AXFR returned no records (likely refused)"

    except (socket.timeout, OSError) as e:
        result["error"] = f"AXFR connection error: {e}"
    finally:
        if sock:
            sock.close()

    return result


def dns_enumeration(
    domain: str,
    dns_server: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Perform comprehensive DNS enumeration on a domain.

    Returns structured dict with keys: A, AAAA, CNAME, MX, NS, TXT, SOA,
    zone_transfer, errors.
    """
    clean = _clean_domain(domain)
    servers = [dns_server] if dns_server else DEFAULT_DNS_SERVERS
    result: dict[str, Any] = {
        "A": [],
        "AAAA": [],
        "CNAME": [],
        "MX": [],
        "NS": [],
        "TXT": [],
        "SOA": None,
        "zone_transfer_attempted": False,
        "zone_transfer_result": None,
        "errors": [],
    }

    # --- A / AAAA via socket.getaddrinfo ---
    try:
        saved = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        try:
            infos_a = socket.getaddrinfo(clean, None, socket.AF_INET)
            for info in infos_a:
                ip = info[4][0]
                if ip not in result["A"]:
                    result["A"].append(ip)
        except (socket.gaierror, OSError):
            pass

        try:
            infos_aaaa = socket.getaddrinfo(clean, None, socket.AF_INET6)
            for info in infos_aaaa:
                ip = info[4][0]
                if ip not in result["AAAA"]:
                    result["AAAA"].append(ip)
        except (socket.gaierror, OSError):
            pass
        finally:
            socket.setdefaulttimeout(saved)
    except Exception as e:
        result["errors"].append(f"A/AAAA resolution error: {e}")

    # --- Raw DNS queries for CNAME, MX, NS, TXT, SOA ---
    for server in servers:
        _rate_sleep(0.15)

        # CNAME
        cname_records = _raw_dns_lookup(clean, DNS_CNAME, server, timeout)
        for r in cname_records:
            if r["data"] not in result["CNAME"]:
                result["CNAME"].append(r["data"])

        # MX
        mx_records = _raw_dns_lookup(clean, DNS_MX, server, timeout)
        for r in mx_records:
            entry = str(r["data"])
            if entry not in result["MX"]:
                result["MX"].append(r["data"])

        # NS
        ns_records = _raw_dns_lookup(clean, DNS_NS, server, timeout)
        for r in ns_records:
            if r["data"] not in result["NS"]:
                result["NS"].append(r["data"])

        # TXT
        txt_records = _raw_dns_lookup(clean, DNS_TXT, server, timeout)
        for r in txt_records:
            if r["data"] not in result["TXT"]:
                result["TXT"].append(r["data"])

        # SOA
        soa_records = _raw_dns_lookup(clean, DNS_SOA, server, timeout)
        for r in soa_records:
            if result["SOA"] is None:
                result["SOA"] = r["data"]

        # If we got results, stop trying more servers
        if any([result["CNAME"], result["MX"], result["NS"], result["TXT"]]):
            break

    # --- Zone transfer attempt ---
    if result["NS"]:
        for ns_entry in result["NS"]:
            ns_host = ns_entry if isinstance(ns_entry, str) else ns_entry.get("exchange", "")
            if not ns_host:
                continue
            # Resolve NS host to IP
            ns_ip = None
            try:
                infos = socket.getaddrinfo(ns_host, None, socket.AF_INET)
                ns_ip = infos[0][4][0] if infos else None
            except (socket.gaierror, OSError):
                pass
            if ns_ip:
                axfr_result = _dns_axfr_attempt(clean, ns_ip, timeout=8.0)
                result["zone_transfer_attempted"] = True
                result["zone_transfer_result"] = axfr_result
                if axfr_result.get("error"):
                    result["errors"].append(
                        f"AXFR attempt to {ns_host} ({ns_ip}): {axfr_result['error']}"
                    )
                break  # One attempt is sufficient

    return result


# =============================================================================
# WHOIS Lookup
# =============================================================================


def _whois_raw_query(
    query: str, server: str, port: int = 43, timeout: float = DEFAULT_TIMEOUT
) -> str:
    """Send a raw WHOIS query and return the response text."""
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((server, port))
        sock.sendall((query + "\r\n").encode("ascii"))
        data = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
            except socket.timeout:
                break
        return data.decode("utf-8", errors="replace")
    except (socket.gaierror, OSError, UnicodeError) as e:
        return f"ERROR: {e}"
    finally:
        if sock:
            sock.close()


def _parse_whois(raw: str, domain: str) -> dict[str, Any]:
    """Extract structured fields from a WHOIS response."""
    lines = raw.split("\n")
    result: dict[str, Any] = {
        "registrar": None,
        "creation_date": None,
        "expiration_date": None,
        "updated_date": None,
        "name_servers": [],
        "registrant_org": None,
        "registrant_country": None,
        "raw": raw[:2000],
    }

    registrar_patterns = [
        re.compile(r"(?:Registrar:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Sponsoring Registrar:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Registrar Name:\s*)(.+)", re.IGNORECASE),
    ]
    creation_patterns = [
        re.compile(r"(?:Creation Date:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Created on\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Registered on:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Domain Registration Date:\s*)(.+)", re.IGNORECASE),
    ]
    expiry_patterns = [
        re.compile(r"(?:Registry Expiry Date:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Registrar Registration Expiration Date:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Expiration Date:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Expiry date:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Expiry Date:\s*)(.+)", re.IGNORECASE),
    ]
    ns_patterns = [
        re.compile(r"(?:Name Server:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:nserver:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Nameserver:\s*)(.+)", re.IGNORECASE),
    ]

    for line in lines:
        line_stripped = line.strip()
        if result["registrar"] is None:
            for pat in registrar_patterns:
                m = pat.match(line_stripped)
                if m:
                    result["registrar"] = m.group(1).strip()
                    break
        if result["creation_date"] is None:
            for pat in creation_patterns:
                m = pat.match(line_stripped)
                if m:
                    result["creation_date"] = m.group(1).strip()
                    break
        if result["expiration_date"] is None:
            for pat in expiry_patterns:
                m = pat.match(line_stripped)
                if m:
                    result["expiration_date"] = m.group(1).strip()
                    break
        for pat in ns_patterns:
            m = pat.match(line_stripped)
            if m:
                ns = m.group(1).strip().lower().rstrip(".")
                if ns not in result["name_servers"]:
                    result["name_servers"].append(ns)

    # Also pull from Org patterns
    org_patterns = [
        re.compile(r"(?:Registrant Organization:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Organisation:\s*)(.+)", re.IGNORECASE),
    ]
    country_patterns = [
        re.compile(r"(?:Registrant Country:\s*)(.+)", re.IGNORECASE),
        re.compile(r"(?:Country:\s*)(.+)", re.IGNORECASE),
    ]
    for line in lines:
        ls = line.strip()
        if result["registrant_org"] is None:
            for pat in org_patterns:
                m = pat.match(ls)
                if m:
                    result["registrant_org"] = m.group(1).strip()
                    break
        if result["registrant_country"] is None:
            for pat in country_patterns:
                m = pat.match(ls)
                if m:
                    result["registrant_country"] = m.group(1).strip()
                    break

    return result


def whois_lookup(
    domain: str, timeout: float = DEFAULT_TIMEOUT
) -> dict[str, Any]:
    """Perform a WHOIS lookup with IANA referral.

    Returns structured dict with registrar, dates, name_servers, raw text.
    """
    clean = _clean_domain(domain)
    result: dict[str, Any] = {
        "domain": clean,
        "registrar": None,
        "creation_date": None,
        "expiration_date": None,
        "updated_date": None,
        "name_servers": [],
        "registrant_org": None,
        "registrant_country": None,
        "whois_server": None,
        "raw": "",
        "errors": [],
    }

    _rate_sleep()

    # Step 1: Query IANA for TLD whois server
    tld = clean.split(".")[-1] if "." in clean else clean
    iana_response = _whois_raw_query(tld, *WHOIS_IANA, timeout=timeout)
    if iana_response.startswith("ERROR:"):
        result["errors"].append(f"WHOIS IANA query failed: {iana_response}")
        # Fall back to a common whois server
        whois_host = "whois.verisign-grs.com" if tld in ("com", "net") else "whois.iana.org"
    else:
        # Extract referral from IANA response
        whois_host = None
        for line in iana_response.split("\n"):
            line_stripped = line.strip()
            m = re.match(r"(?:whois:\s*)(\S+)", line_stripped, re.IGNORECASE)
            if m:
                whois_host = m.group(1).strip()
                break
            m = re.match(r"(?:refer:\s*)(\S+)", line_stripped, re.IGNORECASE)
            if m:
                whois_host = m.group(1).strip()
                break
        if not whois_host:
            result["errors"].append("Could not determine TLD whois server from IANA")
            result["raw"] = iana_response[:2000]
            return result

    result["whois_server"] = whois_host
    _rate_sleep()

    # Step 2: Query TLD whois server
    raw = _whois_raw_query(clean, whois_host, timeout=timeout)
    if raw.startswith("ERROR:"):
        result["errors"].append(f"WHOIS query to {whois_host} failed: {raw}")
        return result

    parsed = _parse_whois(raw, clean)
    result.update({
        "registrar": parsed["registrar"],
        "creation_date": parsed["creation_date"],
        "expiration_date": parsed["expiration_date"],
        "updated_date": parsed.get("updated_date"),
        "name_servers": parsed["name_servers"],
        "registrant_org": parsed["registrant_org"],
        "registrant_country": parsed["registrant_country"],
        "raw": parsed["raw"],
    })

    return result


# =============================================================================
# Technology Stack Detection
# =============================================================================


def _detect_tech_from_headers(headers: dict[str, str]) -> list[dict[str, Any]]:
    """Detect technologies from HTTP response headers."""
    findings: list[dict[str, Any]] = []
    seen: set[str] = set()

    # Convert headers to a single string for regex matching
    header_lines = [f"{k}: {v}" for k, v in headers.items()]

    for category, patterns in [
        ("web_server", TECH_PATTERNS["web_server"]),
        ("language", TECH_PATTERNS["language"]),
    ]:
        for name, pattern in patterns:
            for line in header_lines:
                m = pattern.search(line)
                if m and name not in seen:
                    seen.add(name)
                    findings.append({
                        "category": category,
                        "name": name,
                        "version": m.group(1) if m.lastindex and m.lastindex >= 1 else None,
                        "evidence": line,
                    })

    # Cookie-based detection
    set_cookie = headers.get("set-cookie", "")
    if set_cookie:
        for name, pattern in TECH_PATTERNS["cookies"]:
            m = pattern.search(set_cookie)
            if m and name not in seen:
                seen.add(name)
                findings.append({
                    "category": "framework",
                    "name": name,
                    "version": None,
                    "evidence": f"Set-Cookie: {m.group(0)}",
                })

    return findings


def _detect_tech_from_html(html: str) -> list[dict[str, Any]]:
    """Detect technologies from HTML body content."""
    findings: list[dict[str, Any]] = []
    seen: set[str] = set()

    # Meta generator tags
    for name, pattern in META_GENERATOR_PATTERNS:
        m = pattern.search(html)
        if m and name not in seen:
            seen.add(name)
            findings.append({
                "category": "cms",
                "name": name,
                "version": m.group(1) if m.lastindex and m.lastindex >= 1 else None,
                "evidence": m.group(0)[:200],
            })

    # CMS direct path patterns
    for name, pattern in CMS_DIRECT_PATTERNS:
        m = pattern.search(html)
        if m and name not in seen:
            seen.add(name)
            findings.append({
                "category": "cms",
                "name": name,
                "version": None,
                "evidence": m.group(0)[:200],
            })

    # Script/CSS framework patterns
    for name, pattern in SCRIPT_FRAMEWORKS:
        m = pattern.search(html)
        if m and name not in seen:
            seen.add(name)
            findings.append({
                "category": "javascript",
                "name": name,
                "version": m.group(1) if m.lastindex and m.lastindex >= 1 else None,
                "evidence": m.group(0)[:200],
            })

    return findings


def tech_detect(
    domain: str, timeout: float = DEFAULT_TIMEOUT
) -> dict[str, Any]:
    """Detect technology stack by fetching the target's homepage.

    Returns {"technologies": [...], "url_fetched": str, "errors": [...]}.
    """
    clean = _clean_domain(domain)
    result: dict[str, Any] = {
        "technologies": [],
        "url_fetched": None,
        "errors": [],
    }

    for scheme in ("https", "http"):
        url = f"{scheme}://{clean}"
        _rate_sleep(0.3)
        status, headers, body = _http_fetch(url, timeout=timeout)
        if status > 0:
            result["url_fetched"] = url
            result["technologies"].extend(_detect_tech_from_headers(headers))
            result["technologies"].extend(_detect_tech_from_html(body))
            break
        elif scheme == "http":
            result["errors"].append(f"Could not fetch {url}: status={status}")

    return result


# =============================================================================
# Wayback Machine (CDX API)
# =============================================================================


def wayback_fetch(
    domain: str, timeout: float = DEFAULT_TIMEOUT
) -> dict[str, Any]:
    """Query the Wayback Machine CDX API for historical URLs.

    Returns {"urls": [{"url": str, "timestamp": str}], "errors": [...]}.
    """
    clean = _clean_domain(domain)
    result: dict[str, Any] = {"urls": [], "errors": []}
    url = WAYBACK_CDX_URL.format(domain=clean)

    _rate_sleep(0.5)
    _, headers, body = _http_fetch(url, timeout=timeout, accept="application/json")

    if not body:
        result["errors"].append("Wayback CDX returned empty response")
        return result

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        result["errors"].append("Wayback CDX returned non-JSON (possibly rate-limited)")
        return result

    if not isinstance(data, list) or len(data) < 2:
        result["errors"].append("Wayback CDX returned insufficient data")
        return result

    # First row is headers: ["urlkey","timestamp","original","mimetype","statuscode","digest","length"]
    for row in data[1:]:
        if isinstance(row, list) and len(row) >= 2:
            result["urls"].append({
                "url": row[0],
                "timestamp": row[1],
            })

    return result


# =============================================================================
# GitHub Dorking
# =============================================================================


_GITHUB_DORK_TEMPLATES = [
    ("API keys", '"{domain}" api_key OR apiKey OR apikey'),
    ("API secrets", '"{domain}" secret_key OR secretKey OR secret'),
    ("Passwords", '"{domain}" password OR passwd OR pwd'),
    ("Database config", '"{domain}" db_password OR db_user OR database_url OR connectionString'),
    ("AWS keys", '"{domain}" AKIA OR aws_access_key OR aws_secret_key'),
    ("Private keys", '"{domain}" -----BEGIN RSA PRIVATE KEY----- OR -----BEGIN EC PRIVATE KEY-----'),
    ("Config files", '"{domain}" filename:.env OR filename:config.json OR filename:web.config'),
    ("Docker config", '"{domain}" docker-compose.yml OR Dockerfile'),
    ("CI/CD leaks", '"{domain}" gitlab-ci.yml OR Jenkinsfile OR .travis.yml'),
    ("Internal URLs", '"{domain}" internal OR staging OR dev OR preprod'),
    ("Tokens", '"{domain}" bearer OR token OR jwt OR oauth'),
    ("SSH keys", '"{domain}" ssh-rsa OR ssh-ed25519 OR id_rsa'),
    ("Backup files", '"{domain}" filename:*.sql OR filename:*.bak OR filename:*.backup'),
    ("Credentials JSON", '"{domain}" filename:credentials.json OR filename:service-account.json'),
    ("Connection strings", '"{domain}" "Server=" OR "Data Source=" OR "jdbc:"'),
]


def github_dorks(domain: str) -> dict[str, Any]:
    """Generate GitHub search URLs for common secret patterns.

    Returns {"dorks": [{"category": str, "query": str, "search_url": str}], ...}.
    """
    clean = _clean_domain(domain)
    dorks: list[dict[str, str]] = []
    for category, query_template in _GITHUB_DORK_TEMPLATES:
        query = query_template.replace("{domain}", clean)
        search_url = f"https://github.com/search?q={quote(query)}&type=code"
        dorks.append({
            "category": category,
            "query": query,
            "search_url": search_url,
        })
    return {"dorks": dorks}


# =============================================================================
# Shodan / Censys Integration
# =============================================================================


def shodan_censys_queries(
    domain: str,
    shodan_key: str | None = None,
    censys_id: str | None = None,
    censys_secret: str | None = None,
) -> dict[str, Any]:
    """Generate Shodan and Censys query URLs.

    If API credentials are provided, generates API query details.
    Otherwise, generates manual search URLs for the web interfaces.

    Returns {
        "shodan": {"query_url": str, "api_url": str|None},
        "censys": {"query_url": str, "api_url": str|None},
    }
    """
    clean = _clean_domain(domain)
    result: dict[str, Any] = {"shodan": {}, "censys": {}}

    # Shodan
    shodan_query = f"hostname:{clean}"
    result["shodan"]["manual_url"] = (
        f"https://www.shodan.io/search?query={quote(shodan_query)}"
    )
    if shodan_key:
        result["shodan"]["api_url"] = (
            f"https://api.shodan.io/dns/domain/{clean}?key={shodan_key}"
        )
        result["shodan"]["api_query"] = shodan_query
    else:
        result["shodan"]["api_url"] = None
        result["shodan"]["note"] = "Provide --shodan-key for API access"

    # Censys
    censys_query = f"dns.names={clean}"
    result["censys"]["manual_url"] = (
        f"https://search.censys.io/search?resource=hosts&q={quote(censys_query)}"
    )
    if censys_id and censys_secret:
        result["censys"]["api_url"] = "https://search.censys.io/api/v2/hosts/search"
        result["censys"]["api_query"] = censys_query
        # Note: actual API call requires Basic auth with id:secret
    else:
        result["censys"]["api_url"] = None
        result["censys"]["note"] = "Provide --censys-id and --censys-secret for API access"

    return result


# =============================================================================
# Email Discovery
# =============================================================================


_EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    re.IGNORECASE,
)


def email_discovery(
    domain: str,
    html_bodies: list[str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Discover emails via regex extraction from HTML and pattern enumeration.

    Args:
        domain: Target domain.
        html_bodies: Optional list of HTML strings to scrape.
        timeout: Network timeout for fetching pages.

    Returns {"discovered": [...], "enumerated_patterns": [...]}.
    """
    clean = _clean_domain(domain)
    result: dict[str, Any] = {
        "discovered": [],
        "enumerated_patterns": [],
    }

    # Extract emails from provided HTML
    for html in (html_bodies or []):
        for match in _EMAIL_REGEX.finditer(html or ""):
            email = match.group(0).lower()
            if email.endswith("@" + clean) or email.endswith("." + clean):
                if email not in result["discovered"]:
                    result["discovered"].append(email)

    # If no HTML provided, try fetching the homepage
    if not html_bodies:
        for scheme in ("https", "http"):
            url = f"{scheme}://{clean}"
            _rate_sleep(0.3)
            status, headers, body = _http_fetch(url, timeout=timeout)
            if status > 0 and body:
                for match in _EMAIL_REGEX.finditer(body):
                    email = match.group(0).lower()
                    if email.endswith("@" + clean) or email.endswith("." + clean):
                        if email not in result["discovered"]:
                            result["discovered"].append(email)
                break

    # Enumerate common email patterns
    for pattern in EMAIL_PATTERNS:
        result["enumerated_patterns"].append(pattern.format(domain=clean))

    result["discovered"].sort()
    return result


# =============================================================================
# Orchestrator
# =============================================================================


def run_recon(
    domain: str,
    mode: str = "all",
    dns_server: str | None = None,
    shodan_key: str | None = None,
    censys_id: str | None = None,
    censys_secret: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Run passive reconnaissance for the given domain and mode.

    Args:
        domain: Target domain (e.g., "example.com").
        mode: One of crtsh, dns, whois, tech, wayback, github, shodan-censys,
              email, all.
        dns_server: Optional custom DNS server IP.
        shodan_key: Optional Shodan API key.
        censys_id: Optional Censys API ID.
        censys_secret: Optional Censys API secret.
        timeout: Network timeout in seconds.

    Returns:
        Structured JSON-serializable dict with all recon results.
    """
    clean = _clean_domain(domain)
    result: dict[str, Any] = {
        "domain": clean,
        "timestamp": _now_iso(),
        "mode": mode,
        "subdomains": [],
        "dns_records": {},
        "whois": {},
        "technologies": [],
        "wayback_urls": [],
        "github_dorks": [],
        "shodan_censys": {},
        "emails": {"discovered": [], "enumerated_patterns": []},
        "errors": [],
    }

    def _run_mode(m: str) -> bool:
        return mode in (m, "all")

    # 1. Certificate Transparency
    if _run_mode("crtsh"):
        crtsh_result = crtsh_query(clean, timeout=timeout)
        result["subdomains"] = crtsh_result.get("subdomains", [])
        result["errors"].extend(crtsh_result.get("errors", []))

    # 2. DNS Enumeration
    if _run_mode("dns"):
        dns_result = dns_enumeration(clean, dns_server=dns_server, timeout=timeout)
        result["dns_records"] = dns_result
        # Also extract subdomains from NS/MX
        for mx in dns_result.get("MX", []):
            if isinstance(mx, dict):
                exchange = mx.get("exchange", "")
                if exchange and exchange.endswith("." + clean):
                    if exchange.rstrip(".") not in result["subdomains"]:
                        result["subdomains"].append(exchange.rstrip("."))
        for ns in dns_result.get("NS", []):
            if isinstance(ns, str) and ns.endswith("." + clean):
                if ns.rstrip(".") not in result["subdomains"]:
                    result["subdomains"].append(ns.rstrip("."))
        # Add common subdomains as probing targets if crt.sh gave nothing
        if not result["subdomains"]:
            for sub in COMMON_SUBDOMAINS:
                candidate = f"{sub}.{clean}"
                try:
                    infos = socket.getaddrinfo(candidate, None)
                    if infos:
                        result["subdomains"].append(candidate)
                except (socket.gaierror, OSError):
                    pass

    # 3. WHOIS
    if _run_mode("whois"):
        result["whois"] = whois_lookup(clean, timeout=timeout)
        result["errors"].extend(result["whois"].pop("errors", []))

    # 4. Technology Detection
    if _run_mode("tech"):
        tech_result = tech_detect(clean, timeout=timeout)
        result["technologies"] = tech_result.get("technologies", [])
        result["errors"].extend(tech_result.get("errors", []))

    # 5. Wayback Machine
    if _run_mode("wayback"):
        wb_result = wayback_fetch(clean, timeout=timeout)
        result["wayback_urls"] = wb_result.get("urls", [])
        result["errors"].extend(wb_result.get("errors", []))

    # 6. GitHub Dorking
    if _run_mode("github"):
        result["github_dorks"] = github_dorks(clean).get("dorks", [])

    # 7. Shodan / Censys
    if _run_mode("shodan-censys"):
        result["shodan_censys"] = shodan_censys_queries(
            clean,
            shodan_key=shodan_key,
            censys_id=censys_id,
            censys_secret=censys_secret,
        )

    # 8. Email Discovery
    if _run_mode("email"):
        result["emails"] = email_discovery(clean, timeout=timeout)

    # Deduplicate and sort subdomains
    result["subdomains"] = sorted(set(s.rstrip(".") for s in result["subdomains"]))

    return result


# =============================================================================
# CLI
# =============================================================================


def main() -> int:
    ap = argparse.ArgumentParser(
        description="GKN-Phantom Passive Reconnaissance Module (v3.0)"
    )
    ap.add_argument(
        "--domain", required=True,
        help="Target domain (e.g., example.com)"
    )
    ap.add_argument(
        "--mode", default="all",
        choices=["crtsh", "dns", "whois", "tech", "wayback", "github",
                 "shodan-censys", "email", "all"],
        help="Reconnaissance mode (default: all)"
    )
    ap.add_argument(
        "--output", "-o",
        help="Output JSON file path (default: stdout)"
    )
    ap.add_argument(
        "--dns-server",
        help="Custom DNS server IP for raw queries (default: 8.8.8.8)"
    )
    ap.add_argument(
        "--shodan-key",
        help="Shodan API key for enriched queries"
    )
    ap.add_argument(
        "--censys-id",
        help="Censys API ID for enriched queries"
    )
    ap.add_argument(
        "--censys-secret",
        help="Censys API secret for enriched queries"
    )
    ap.add_argument(
        "--timeout", type=float, default=DEFAULT_TIMEOUT,
        help=f"Network timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )
    args = ap.parse_args()

    result = run_recon(
        domain=args.domain,
        mode=args.mode,
        dns_server=args.dns_server,
        shodan_key=args.shodan_key,
        censys_id=args.censys_id,
        censys_secret=args.censys_secret,
        timeout=args.timeout,
    )

    output_json = dump_json(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output_json + "\n")
        print(f"passive_recon: output written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
