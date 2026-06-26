---
name: jrv-ssl-monitor
description: Check SSL/TLS certificate expiry, issuer, protocol, and SANs for one or more domains. Use when asked to check SSL certificates, monitor cert expiry, verify HTTPS is working, audit domain security, or check if a certificate is about to expire. Supports custom ports and warning thresholds. No external dependencies — uses Python stdlib ssl module.
---

# SSL Certificate Monitor

Check SSL certificate health for any domain — expiry, issuer, protocol version, and Subject Alternative Names.

## Quick Start

```bash
python3 scripts/check_ssl.py example.com
python3 scripts/check_ssl.py example.com google.com github.com --warn-days 30
python3 scripts/check_ssl.py internal.host --port 8443 --json
```

## Features

- **Expiry check** — days remaining with configurable warning threshold
- **Multi-domain** — check multiple domains in one command
- **Certificate details** — subject, issuer, protocol, serial number, SANs
- **Error handling** — detects DNS failures, timeouts, verification errors, refused connections
- **Exit codes** — 0 = all ok, 1 = warnings, 2 = expired or failed (useful for cron/CI)
- **No dependencies** — Python stdlib only

## Options

| Flag | Description |
|------|-------------|
| `--warn-days N` | Warning threshold in days (default: 14) |
| `--port PORT` | Port to check (default: 443) |
| `--json` | Output structured JSON |
| `--timeout N` | Connection timeout in seconds (default: 10) |

## Use Cases

- Daily cron job to monitor production domains
- Pre-deployment cert validation
- Audit all company domains in one pass
- CI/CD pipeline gate for cert health
