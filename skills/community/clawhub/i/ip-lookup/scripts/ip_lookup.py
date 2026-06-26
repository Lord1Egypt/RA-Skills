#!/usr/bin/env python3
"""
ip-lookup — Network intelligence CLI (stdlib only, no pip required)
Combines IP geolocation, ASN, reverse DNS, PTR, and RDAP/WHOIS
using free public APIs with no authentication required.

APIs used:
  - ip-api.com       : Geolocation + ASN (free, no key, 45 req/min)
  - ipwho.is         : Geolocation fallback (free, no key)
  - rdap.arin.net    : WHOIS/RDAP (free, no key) — falls back to RIPE
  - dns.google       : Reverse DNS / PTR (free, no key)
  - api.abuseipdb.com: Abuse check (requires free API key via ABUSEIPDB_KEY env var)
"""


import argparse
import json
import os
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone


# ── ANSI colours (gracefully disabled when not a TTY) ────────────────────────


USE_COLOR = sys.stdout.isatty()


def c(text: str, code: str) -> str:
    if not USE_COLOR:
        return text
    codes = {
        "bold": "\033[1m", "dim": "\033[2m",
        "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
        "blue": "\033[34m", "cyan": "\033[36m", "white": "\033[37m",
        "reset": "\033[0m",
    }
    return f"{codes.get(code, '')}{text}{codes['reset']}"


def box(title: str, lines: list[tuple[str, str]], border: str = "cyan") -> None:
    """Print a simple bordered panel with key-value rows."""
    print()
    print(c(f"  ╔══ {title} ", border))
    for key, val in lines:
        k = c(f"  ║  {key:<22}", "dim")
        print(f"{k}{val}")
    print(c("  ╚" + "═" * 50, border))


# ── Networking helpers ────────────────────────────────────────────────────────


def fetch(url: str, params: dict | None = None,
          headers: dict | None = None, timeout: int = 8) -> dict | None:
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception:
        return None


def resolve_target(target: str) -> tuple[str, str | None]:
    """Return (ip_address, hostname_if_resolved). Resolves hostnames → IP."""
    if _is_ip(target):
        return target, None
    try:
        ip = socket.gethostbyname(target)
        return ip, target
    except socket.gaierror as e:
        print(c(f"Cannot resolve '{target}': {e}", "red"), file=sys.stderr)
        sys.exit(1)


def _is_ip(s: str) -> bool:
    for af in (socket.AF_INET, socket.AF_INET6):
        try:
            socket.inet_pton(af, s)
            return True
        except socket.error:
            pass
    return False


# ── Data fetchers ─────────────────────────────────────────────────────────────


def fetch_geo(ip: str) -> dict:
    """ip-api.com geolocation + ASN. Falls back to ipwho.is."""
    fields = ("status,message,country,countryCode,regionName,city,zip,"
              "lat,lon,timezone,isp,org,as,asname,mobile,proxy,hosting,query")
    data = fetch(f"http://ip-api.com/json/{ip}", params={"fields": fields})
    if data and data.get("status") == "success":
        return {"_source": "ip-api.com", **data}
    data2 = fetch(f"https://ipwho.is/{ip}")
    if data2 and data2.get("success"):
        return {"_source": "ipwho.is", **data2}
    return {}


def fetch_ptr(ip: str) -> str | None:
    """Reverse DNS via Google Public DNS API."""
    parts = ip.split(".")
    if len(parts) == 4:
        arpa = ".".join(reversed(parts)) + ".in-addr.arpa"
    else:
        return None  # IPv6 PTR not handled
    data = fetch("https://dns.google/resolve", params={"name": arpa, "type": "PTR"})
    if data and data.get("Answer"):
        return data["Answer"][0].get("data", "").rstrip(".")
    return None


def fetch_rdap(ip: str) -> dict:
    """ARIN RDAP for IP/network block info + abuse contacts. Falls back to RIPE."""
    data = fetch(f"https://rdap.arin.net/registry/ip/{ip}")
    if data:
        return data
    return fetch(f"https://rdap.db.ripe.net/ip/{ip}") or {}


def fetch_abuse(ip: str, api_key: str) -> dict:
    """AbuseIPDB reputation check (90-day window)."""
    data = fetch(
        "https://api.abuseipdb.com/api/v2/check",
        params={"ipAddress": ip, "maxAgeInDays": "90"},
        headers={"Key": api_key, "Accept": "application/json"},
    )
    return (data or {}).get("data", {})


# ── Display ───────────────────────────────────────────────────────────────────


def display_geo(geo: dict, hostname: str | None):
    rows: list[tuple[str, str]] = []
    if hostname:
        rows.append(("Resolved From", c(hostname, "yellow")))
    ip = geo.get("query") or geo.get("ip", "—")
    rows.append(("IP Address", c(ip, "bold")))
    country = geo.get("country", "—")
    cc = geo.get("countryCode") or geo.get("country_code", "—")
    rows.append(("Country", f"{country} [{cc}]"))
    rows.append(("Region", geo.get("regionName") or geo.get("region", "—")))
    rows.append(("City", geo.get("city", "—")))
    rows.append(("ZIP", geo.get("zip") or geo.get("postal", "—")))
    lat = geo.get("lat") or geo.get("latitude", "—")
    lon = geo.get("lon") or geo.get("longitude", "—")
    rows.append(("Coordinates", f"{lat}, {lon}"))
    rows.append(("Timezone", geo.get("timezone", "—")))
    rows.append(("ISP", geo.get("isp") or str(geo.get("connection", {}).get("isp", "—"))))
    rows.append(("Org", geo.get("org") or str(geo.get("connection", {}).get("org", "—"))))
    asn = geo.get("as") or f"AS{geo.get('connection', {}).get('asn', '—')}"
    rows.append(("ASN", asn))


    flags = []
    if geo.get("proxy") or (geo.get("security") or {}).get("proxy"):
        flags.append(c("PROXY", "blue"))
    if geo.get("hosting") or (geo.get("security") or {}).get("hosting"):
        flags.append(c("HOSTING/VPN", "yellow"))
    if geo.get("mobile") or (geo.get("security") or {}).get("mobile"):
        flags.append(c("MOBILE", "cyan"))
    rows.append(("Flags", "  ".join(flags) if flags else c("none", "dim")))


    src = geo.get("_source", "unknown")
    box(c(f"🌍  Geolocation   [via {src}]", "green"), rows, "green")


def display_ptr(ptr: str | None):
    val = c(ptr, "cyan") if ptr else c("(no PTR record)", "dim")
    box(c("🔄  Reverse DNS (PTR)", "yellow"), [("PTR Record", val)], "yellow")


def display_rdap(rdap: dict):
    if not rdap:
        print(c("  RDAP: no data returned", "dim"))
        return
    rows: list[tuple[str, str]] = []
    rows.append(("Network Name", rdap.get("name", "—")))
    rows.append(("Handle", rdap.get("handle", "—")))
    rows.append(("Type", rdap.get("type", "—")))


    cidr_list = rdap.get("cidr0_cidrs", [])
    if cidr_list:
        cidrs = ", ".join(
            f"{e.get('v4prefix') or e.get('v6prefix')}/{e.get('length')}"
            for e in cidr_list
        )
        rows.append(("CIDR Block(s)", cidrs))
    else:
        start = rdap.get("startAddress", "")
        end = rdap.get("endAddress", "")
        if start:
            rows.append(("IP Range", f"{start} – {end}"))


    for entity in rdap.get("entities", []):
        if "abuse" in entity.get("roles", []):
            vcard = entity.get("vcardArray", [])
            if len(vcard) > 1:
                for entry in vcard[1]:
                    if entry[0] == "email":
                        rows.append(("Abuse Email", c(str(entry[3]), "red")))
                    elif entry[0] == "fn":
                        rows.append(("Abuse Contact", str(entry[3])))


    for ev in rdap.get("events", []):
        action = ev.get("eventAction", "")
        date = ev.get("eventDate", "")
        if action in ("registration", "last changed"):
            rows.append((action.title(), date[:10] if date else "—"))


    box(c("📋  RDAP / WHOIS", "blue"), rows, "blue")


def display_abuse(abuse: dict):
    if not abuse:
        return
    score = abuse.get("abuseConfidenceScore", 0)
    if score == 0:
        score_str = c(f"{score}%  (clean)", "green")
    elif score < 50:
        score_str = c(f"{score}%  (suspicious)", "yellow")
    else:
        score_str = c(f"{score}%  (likely malicious)", "red")


    rows: list[tuple[str, str]] = [
        ("Abuse Score", score_str),
        ("Total Reports (90d)", str(abuse.get("totalReports", 0))),
        ("Last Reported", str(abuse.get("lastReportedAt") or "never")[:19]),
        ("Usage Type", abuse.get("usageType", "—")),
        ("Domain", abuse.get("domain", "—")),
    ]
    box(c("🛡   Abuse Reputation (AbuseIPDB)", "red"), rows, "red")


# ── CLI entry point ───────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="IP network intelligence: geolocation, RDAP/WHOIS, reverse DNS, abuse check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ip_lookup.py 8.8.8.8
  ip_lookup.py github.com
  ip_lookup.py 1.1.1.1 --json
  ip_lookup.py 185.220.101.1 --abuse        (requires ABUSEIPDB_KEY env var)
  ip_lookup.py 8.8.8.8 --no-rdap            (skip RDAP, faster)
""",
    )
    parser.add_argument("target", help="IP address or hostname to investigate")
    parser.add_argument("--json", action="store_true", help="Output raw JSON (machine-readable)")
    parser.add_argument("--abuse", action="store_true",
                        help="Include AbuseIPDB reputation check (set ABUSEIPDB_KEY env var)")
    parser.add_argument("--no-rdap", action="store_true", help="Skip RDAP/WHOIS lookup")
    parser.add_argument("--no-ptr", action="store_true", help="Skip reverse DNS lookup")
    args = parser.parse_args()


    ip, hostname = resolve_target(args.target)


    if not args.json:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        print()
        target_str = c(args.target, "cyan")
        resolved = (f"  →  {c(ip, 'yellow')}" if hostname else "")
        print(f"  {c('🔍  Investigating:', 'bold')} {target_str}{resolved}  {c(ts, 'dim')}")


    results: dict = {"ip": ip, "hostname": hostname, "queried_at": datetime.now(timezone.utc).isoformat()}


    # Geolocation
    geo = fetch_geo(ip)
    results["geo"] = geo
    if not args.json:
        display_geo(geo, hostname)


    # PTR / Reverse DNS
    if not args.no_ptr:
        ptr = fetch_ptr(ip)
        results["ptr"] = ptr
        if not args.json:
            display_ptr(ptr)


    # RDAP / WHOIS
    if not args.no_rdap:
        rdap = fetch_rdap(ip)
        results["rdap"] = rdap
        if not args.json:
            display_rdap(rdap)


    # Abuse reputation
    if args.abuse:
        api_key = os.environ.get("ABUSEIPDB_KEY", "")
        if not api_key:
            print(c("  ✗  --abuse requires ABUSEIPDB_KEY environment variable", "red"), file=sys.stderr)
        else:
            abuse = fetch_abuse(ip, api_key)
            results["abuse"] = abuse
            if not args.json:
                display_abuse(abuse)


    if args.json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print()


if __name__ == "__main__":
    main()