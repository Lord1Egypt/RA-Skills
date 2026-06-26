
---
name: ip-lookup
description: Investigate any IP address or hostname - geolocation, ASN/ISP, reverse DNS (PTR), RDAP/WHOIS network block, and optional AbuseIPDB reputation check. No API keys needed for core features. Use when the user asks about an IP address, wants to geolocate an IP, look up who owns a network block, find the ISP or ASN for an IP, check abuse reputation, or do a reverse DNS lookup. Trigger phrases include "who owns this IP", "where is this IP located", "look up IP", "check if IP is malicious", "reverse DNS for", "what ASN is", "whois for IP".
metadata: {"openclaw":{"emoji":":mag:","requires":{"bins":["python3"]}}}
---

# IP Lookup

Zero-dependency network intelligence for any IP address or hostname. Combines four data
 sources into one clean terminal report: geolocation, reverse DNS, RDAP/WHOIS network block info, and optional AbuseIPDB reputation check.

No pip install required. Uses only Python 3 stdlib (urllib, socket, json, argparse). Works on any machine that has Python - no virtual environments, no dependency management.

---

## Quick Start

    python3 {baseDir}/scripts/ip_lookup.py 8.8.8.8
    python3 {baseDir}/scripts/ip_lookup.py github.com

For a hostname, it auto-resolves to IP first, then runs all lookups.

---

## What each panel shows

### [Geo] Geolocation (always on)

Queries ip-api.com (45 req/min free, no key). Falls back to ipwho.is if ip-api.com fails.

Returns:
- Country, country code, region, city, postal/ZIP code
- Latitude and longitude coordinates
- Timezone (e.g. America/
New_York)
- ISP name and organisation
- ASN in "AS12345 Name" format
- Flags: PROXY, HOSTING/VPN, MOBILE - detected by ip-api.com heuristics

Example output for 8.8.8.8:
    IP Address        8.8.8.8
    Country           United States [US]
    Region            Virginia
    City              Ashburn
    Timezone          America/New_York
    ISP               Google LLC
    Org               Google Public DNS
    ASN               AS15169 Google LLC
    Flags             HOSTING/VPN

### [PTR] Reverse DNS (on by default, skip with --no-ptr)

Queries dns.google for the PTR record of the IP. Converts the IP to in-addr.arpa form internally. Returns the hostname if one exists, or "(no PTR record)" if none.

Useful for: identifying server hostnames, recognising CDN edge nodes (e.g. server-
13-35-12-1.fra50.r.cloudfront.net), confirming FCrDNS (forward-confirmed reverse DNS).

### [RDAP] RDAP / WHOIS (on by default, skip with --no-rdap)

Queries rdap.arin.net first. Falls back to rdap.db.ripe.net for European IPs.

Returns:
- Network name - registered handle for the IP block (e.g. APNIC-LABS, MSFT)
- CIDR block(s) - prefix in CIDR notation (e.g. 1.1.1.0/24)
- Abuse contact name and email - extracted from RDAP entities where roles includes "abuse"
- Registration date and Last changed date

Example output for 1.1.1.1:
    Network Name      APNIC-LABS
    CIDR Block(s)     1.1.1.0/24
    Abuse Email       helpdesk@apnic.net
    Registration      2011-08-10
    Last Changed      2023-04-26

### [Abuse] AbuseIPDB reputation (optional, requires free API key)

Queries api.abusei
pdb.com with 90-day lookback. Returns:
- Abuse confidence score 0-100 (0 = clean, 100 = confirmed malicious)
- Total reports in past 90 days
- Last reported timestamp
- Usage type (e.g. Data Center/Web Hosting/Transit)
- Domain associated with the IP

Score guide:
- 0       = no reports, likely clean
- 1-25    = low risk, possibly misconfigured server
- 26-75   = suspicious, investigate further
- 76-100  = high confidence malicious (scanner, spam source, Tor exit node, etc.)

---

## All flags

Flag       | Effect
-----------|---------------------------------------------------------------
--json     | Full result as JSON (no ANSI codes, safe to pipe)
--abuse    | Enable AbuseIPDB panel (needs ABUSEIPDB_KEY env var)
--no-rdap  | Skip RDAP/WHOIS (faster, avoids rate limits)
--no-ptr   | 
Skip reverse DNS PTR lookup

---

## Common workflows

Fast geo-only lookup:
    python3 {baseDir}/scripts/ip_lookup.py 104.21.0.1 --no-rdap --no-ptr

Find abuse contact for a network:
    python3 {baseDir}/scripts/ip_lookup.py 185.220.101.1

Check if IP is flagged malicious:
    export ABUSEIPDB_KEY=your_key
    python3 {baseDir}/scripts/ip_lookup.py 185.220.101.1 --abuse

Scripting with JSON output:
    python3 {baseDir}/scripts/ip_lookup.py 8.8.8.8 --json | python3 -c \
      "import json,sys; d=json.load(sys.stdin); print(d['geo']['country'], d['geo']['as'])"

Investigate a hostname (auto-resolves):
    python3 {baseDir}/scripts/ip_lookup.py suspicious-domain.example.com

---

## AbuseIPDB setup (one-time)

1. Sign up free at https://www.abuseipdb.com/register
2. Go to API tab in y
our dashboard and create a key (free tier: 1000 checks/day)
3. Run: export ABUSEIPDB_KEY=your_key_here

---

## Technical notes

- ANSI colour output is auto-disabled when stdout is not a TTY (pipes, CI, logs)
- IPv6 addresses are supported for geolocation and RDAP; PTR lookup is IPv4-only
- RDAP tries ARIN first (global coverage), retries RIPE directly if no data returned
- ip-api.com rate limit: 45 requests/minute on the free tier; auto-falls back to ipwho.is
- No caching - all calls are live; use --no-rdap --no-ptr for bulk queries
- Script uses only Python 3 stdlib - no pip install needed
