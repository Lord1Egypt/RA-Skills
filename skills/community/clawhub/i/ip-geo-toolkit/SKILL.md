---
name: ip-geo-toolkit
description: Look up IP geolocation, find your public IP, perform reverse DNS, and run bulk IP lookups. Uses free APIs (ip-api.com, ipify) with no API key required. No external dependencies — pure Python. Use when looking up IP address location, finding your public IP, checking ISP/ASN info, doing reverse DNS, or processing lists of IPs for geolocation data.
---

# IP Geolocation Toolkit

Look up IP locations, ISP info, and reverse DNS with zero dependencies.

## Commands

All commands use `scripts/ip_geo.py`.

### Look Up IP(s)

```bash
python3 scripts/ip_geo.py lookup 8.8.8.8
python3 scripts/ip_geo.py lookup 8.8.8.8 1.1.1.1 9.9.9.9
python3 scripts/ip_geo.py lookup 8.8.8.8 --json
```

Returns: country, region, city, ZIP, coordinates, timezone, ISP, organization, AS number, and reverse DNS.

### Find Your Public IP

```bash
python3 scripts/ip_geo.py myip
python3 scripts/ip_geo.py myip --json
```

Detects your public IP and runs a full geolocation lookup.

### Bulk Lookup

```bash
python3 scripts/ip_geo.py bulk --input ips.txt
python3 scripts/ip_geo.py bulk --input ips.txt --json --output results.json
cat ips.txt | python3 scripts/ip_geo.py bulk --input -
```

Processes up to 100 IPs per batch via ip-api.com batch endpoint. Input file: one IP per line, lines starting with # are skipped.

## Data Returned

Each lookup returns: country, countryCode, region, regionName, city, zip, lat, lon, timezone, isp, org, as (ASN), and reverse DNS (via local socket).

## Rate Limits

Free ip-api.com tier: 45 requests/minute for single lookups, 15 requests/minute for batch. The script auto-throttles between requests.
