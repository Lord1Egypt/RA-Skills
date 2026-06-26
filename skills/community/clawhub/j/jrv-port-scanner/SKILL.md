---
name: port-scanner
description: Fast TCP port scanner for network reconnaissance and security auditing. Scan hosts for open ports, detect common services, and identify potential attack surface. Use when checking what ports are open on a server, scanning a network range, auditing firewall rules, or performing pre-deployment security checks. Triggers on "scan ports", "check open ports", "port scan", "network recon", "what ports are open", "firewall audit".
---

# Port Scanner

Lightweight, zero-dependency TCP port scanner for network recon and security auditing.

## Quick Start

```bash
# Scan common ports on a host
python3 scripts/port_scan.py example.com

# Scan specific port range
python3 scripts/port_scan.py 192.168.1.1 --ports 1-1024

# Scan specific ports
python3 scripts/port_scan.py 10.0.0.1 --ports 22,80,443,3306,5432,8080

# Fast scan with short timeout
python3 scripts/port_scan.py example.com --timeout 0.5 --workers 200

# JSON output
python3 scripts/port_scan.py example.com --format json

# Scan top N most common ports
python3 scripts/port_scan.py example.com --top 100
```

## Features

- Concurrent scanning with configurable thread count
- Common service identification (HTTP, SSH, MySQL, PostgreSQL, Redis, etc.)
- Banner grabbing for open ports
- Supports single ports, ranges, comma-separated lists, and top-N common ports
- JSON and text output formats
- No external dependencies — pure Python stdlib
