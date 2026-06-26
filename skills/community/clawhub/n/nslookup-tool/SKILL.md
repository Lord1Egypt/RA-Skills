---
name: nslookup-tool
description: Query DNS servers to resolve domain names to IP addresses. Use for network troubleshooting and DNS diagnostics.
---
# NSLookup - DNS Resolution Utility

Query Domain Name System servers to resolve hostnames to IP addresses or perform reverse DNS lookups. Essential for network troubleshooting and DNS configuration verification.

## Usage
```bash
nslookup-tool [options] <hostname>
```

## Features

- Forward DNS lookup (hostname → IP)
- Reverse DNS lookup (IP → hostname)
- Query specific DNS record types (A, AAAA, MX, CNAME, TXT)
- Specify custom DNS server

## Examples

```bash
# Basic lookup
nslookup-tool example.com

# MX record lookup
nslookup-tool -type=mx example.com

# Use specific DNS server
nslookup-tool google.com 8.8.8.8
```