---
name: log-parser
description: Parse and analyze various log formats (nginx, apache, syslog, application logs). Extract key information and generate reports.
metadata: { "openclaw": { "emoji": "📋", "requires": { "bins": ["python3"] } } }
---

# Log Parser

A log parsing and analysis tool for security operations and DevOps.

## Features

- **Multi-format Support** - nginx, apache, syslog, application logs
- **Auto-detection** - Automatically detect log format
- **Key Extraction** - Extract IPs, timestamps, error codes, URLs
- **Filtering** - Filter logs by IP, status code, time range
- **Statistics** - Generate summary reports
- **Error Detection** - Identify and highlight error entries

## Usage

```bash
python3 skills/log-parser/scripts/log_parser.py <action> [options]
```

## Actions

| Action | Description |
|--------|-------------|
| `parse` | Parse log file and extract fields |
| `stats` | Generate statistics report |
| `filter` | Filter logs by criteria |
| `errors` | Extract error entries only |
| `top` | Top N items (IPs, URLs, etc.) |

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--file` | string | - | Log file path |
| `--format` | string | auto | Log format (auto, nginx, apache, syslog) |
| `--limit` | int | 100 | Max results to return |
| `--filter-ip` | string | - | Filter by IP address |
| `--filter-status` | string | - | Filter by status code |
| `--top-field` | string | - | Field for top N (ip, url, status) |

## Supported Log Formats

### nginx
```
192.168.1.1 - - [22/Mar/2026:14:00:00 +0800] "GET /api/test HTTP/1.1" 200 1234
```

### apache
```
192.168.1.1 - - [22/Mar/2026:14:00:00 +0800] "GET /api/test HTTP/1.1" 200 1234
```

### syslog
```
Mar 22 14:00:00 server sshd[12345]: Failed password for root from 192.168.1.1
```

### application logs (JSON)
```json
{"timestamp": "2026-03-22T14:00:00Z", "level": "ERROR", "message": "..."}
```

## Examples

```bash
# Parse log file
python3 skills/log-parser/scripts/log_parser.py parse --file /var/log/nginx/access.log

# Generate statistics
python3 skills/log-parser/scripts/log_parser.py stats --file /var/log/nginx/access.log

# Filter by IP
python3 skills/log-parser/scripts/log_parser.py filter --file /var/log/nginx/access.log --filter-ip 192.168.1.1

# Get top 10 IPs
python3 skills/log-parser/scripts/log_parser.py top --file /var/log/nginx/access.log --top-field ip --limit 10

# Extract errors
python3 skills/log-parser/scripts/log_parser.py errors --file /var/log/nginx/access.log
```

## Use Cases

1. **Security Analysis** - Identify suspicious IPs, failed logins
2. **Performance Monitoring** - Find slow requests, errors
3. **Traffic Analysis** - Top URLs, user agents
4. **Debugging** - Extract error entries quickly

## Output Format

All results are returned in JSON format:

```json
{
  "success": true,
  "total": 1000,
  "parsed": 998,
  "entries": [...],
  "stats": {...}
}
```

## Current Status

In development.
