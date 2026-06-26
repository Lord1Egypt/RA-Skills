---
name: network-toolbox
description: Network diagnostics and analysis toolkit using Python standard library. Check connectivity, resolve DNS, inspect HTTP headers, scan ports, trace routes, and look up WHOIS/SSL info. Use when the user wants to: (1) Ping a host to check connectivity, (2) Resolve DNS records (A, AAAA, MX, NS, TXT), (3) Inspect HTTP response headers and status codes, (4) Scan open ports on a host, (5) Trace route to a destination, (6) Look up WHOIS domain registration info, (7) Check SSL certificate details, (8) Get your public IP address, (9) Measure network latency.
---

# Network Toolbox

Network diagnostics using Python stdlib — no external tools required.

## Quick Start

```bash
# Ping a host
python3 skills/network-toolbox/scripts/net_ping.py example.com

# DNS lookup
python3 skills/network-toolbox/scripts/net_dns.py example.com --type mx

# HTTP headers
python3 skills/network-toolbox/scripts/net_http.py https://example.com
```

## Common Commands

### Connectivity Check
```bash
python3 skills/network-toolbox/scripts/net_ping.py google.com --count 5
```

### DNS Resolution
```bash
python3 skills/network-toolbox/scripts/net_dns.py example.com --type A
python3 skills/network-toolbox/scripts/net_dns.py example.com --type MX --all
```

### HTTP Inspection
```bash
python3 skills/network-toolbox/scripts/net_http.py https://api.github.com --headers-only
python3 skills/network-toolbox/scripts/net_http.py https://example.com --follow --full
```

### Port Scan
```bash
python3 skills/network-toolbox/scripts/net_portscan.py scanme.nmap.org --ports 22,80,443
python3 skills/network-toolbox/scripts/net_portscan.py localhost --range 1-1024 --timeout 1
```

### SSL Check
```bash
python3 skills/network-toolbox/scripts/net_ssl.py https://example.com --verbose
```

### Public IP
```bash
python3 skills/network-toolbox/scripts/net_ip.py
```

## Scripts

| Script | Purpose |
|--------|---------|
| `net_ping.py` | Ping/connectivity test with timing |
| `net_dns.py` | DNS record lookup (A, AAAA, MX, NS, TXT, CNAME) |
| `net_http.py` | HTTP headers, status, response inspection |
| `net_portscan.py` | TCP port scanning |
| `net_ssl.py` | SSL certificate details and chain |
| `net_ip.py` | Public IP and network interface info |
| `net_whois.py` | WHOIS domain registration lookup |

All scripts run with Python 3 stdlib — no pip installs needed.
