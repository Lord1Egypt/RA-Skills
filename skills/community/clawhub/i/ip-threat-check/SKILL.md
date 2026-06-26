---
name: ip-threat-check
description: Check IP address threat intelligence. Query multiple sources for IP reputation, geolocation, and threat scores.
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python3"], "env": ["ABUSEIPDB_API_KEY"] } } }
---

# IP Threat Check

Check IP address threat intelligence from multiple sources.

## Features

- **Multi-source Query** - Query multiple threat intelligence sources
- **Geolocation** - Get IP geolocation info
- **Threat Score** - Check abuse/threat scores
- **History** - View recent abuse reports
- **Bulk Check** - Check multiple IPs at once

## Usage

```bash
python3 skills/ip-threat-check/scripts/ip_threat.py <action> [options]
```

## Actions

| Action | Description |
|--------|-------------|
| `check` | Check single IP address |
| `bulk` | Check multiple IPs |
| `info` | Get basic IP info (no API key needed) |

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--ip` | string | - | IP address to check |
| `--file` | string | - | File with IPs (one per line) |
| `--source` | string | all | Source (all, abuseipdb, ipapi) |
| `--days` | int | 30 | Days of history to check |

## Data Sources

| Source | API Key | Info Provided |
|--------|---------|---------------|
| ip-api.com | ❌ Free | Geolocation, ISP |
| AbuseIPDB | ✅ Required | Threat score, reports |
| VirusTotal | ✅ Optional | Additional threat info |

## Examples

```bash
# Basic IP info (no API key)
python3 skills/ip-threat-check/scripts/ip_threat.py info --ip 8.8.8.8

# Full threat check (requires API key)
python3 skills/ip-threat-check/scripts/ip_threat.py check --ip 192.168.1.1

# Bulk check
python3 skills/ip-threat-check/scripts/ip_threat.py bulk --file ips.txt
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ABUSEIPDB_API_KEY` | Optional | AbuseIPDB API key |

## Output Example

```json
{
  "success": true,
  "ip": "8.8.8.8",
  "geolocation": {
    "country": "United States",
    "city": "Mountain View",
    "isp": "Google LLC"
  },
  "threat": {
    "score": 0,
    "reports": 0,
    "risk": "low"
  }
}
```

## Use Cases

1. **Security Analysis** - Check suspicious IPs
2. **Log Analysis** - Enrich log data with threat info
3. **Incident Response** - Quick IP reputation check
4. **Threat Hunting** - Identify malicious IPs

## Current Status

In development.
