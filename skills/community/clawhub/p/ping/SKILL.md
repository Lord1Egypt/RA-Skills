---
name: ping
version: "1.0.0"
description: "Monitor network connectivity and diagnose latency issues using ping and traceroute. Use when troubleshooting network problems or checking host availability."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [network, ping, traceroute, latency, monitoring, connectivity, diagnostics]
---

# Ping — Network Connectivity Tool

A thorough network connectivity diagnostic tool that checks host availability, traces routes, sweeps subnets, monitors uptime, and analyzes latency patterns. All results are stored locally in JSONL format for historical analysis and reporting.

## Prerequisites

- `ping` command (pre-installed on most systems)
- `traceroute` or `tracepath` (for route tracing)
- `python3` (for data processing and reporting)
- `bash` 4.0+

## Data Storage

All ping results and configuration are stored in `~/.ping/`:
- `~/.ping/data.jsonl` — historical ping results (JSONL format)
- `~/.ping/config.json` — user configuration (default count, timeout, etc.)

## Commands

### `check`
Check connectivity to a target host. Sends ICMP echo requests and records results.
```bash
PING_TARGET="8.8.8.8" PING_COUNT="4" bash scripts/script.sh check
```

### `trace`
Trace the network route to a target host, showing each hop and latency.
```bash
PING_TARGET="google.com" bash scripts/script.sh trace
```

### `sweep`
Sweep a subnet to discover responsive hosts. Scans a CIDR range.
```bash
PING_SUBNET="192.168.1.0/24" bash scripts/script.sh sweep
```

### `monitor`
Continuously monitor a host and log results. Runs a configurable number of pings over time.
```bash
PING_TARGET="8.8.8.8" PING_INTERVAL="5" PING_DURATION="60" bash scripts/script.sh monitor
```

### `report`
Generate a summary report from stored ping history for a specific target or all targets.
```bash
PING_TARGET="8.8.8.8" bash scripts/script.sh report
```

### `latency`
Analyze latency statistics (min, max, avg, jitter, percentiles) for a target.
```bash
PING_TARGET="8.8.8.8" bash scripts/script.sh latency
```

### `compare`
Compare connectivity and latency between multiple hosts side by side.
```bash
PING_TARGETS="8.8.8.8,1.1.1.1,208.67.222.222" bash scripts/script.sh compare
```

### `history`
View stored ping history with optional filtering by target, date range, or status.
```bash
PING_TARGET="8.8.8.8" PING_LIMIT="20" bash scripts/script.sh history
```

### `export`
Export ping history to CSV or JSON format.
```bash
PING_FORMAT="csv" PING_OUTPUT="ping_report.csv" bash scripts/script.sh export
```

### `config`
View or update ping configuration (default count, timeout, interval).
```bash
PING_KEY="count" PING_VALUE="10" bash scripts/script.sh config
```

### `help`
Show usage information and available commands.
```bash
bash scripts/script.sh help
```

### `version`
Display the current version of the ping skill.
```bash
bash scripts/script.sh version
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `PING_TARGET` | Target host or IP address | — |
| `PING_TARGETS` | Comma-separated list of targets (for compare) | — |
| `PING_COUNT` | Number of ping packets to send | `4` |
| `PING_TIMEOUT` | Timeout in seconds per packet | `5` |
| `PING_INTERVAL` | Seconds between pings (monitor mode) | `5` |
| `PING_DURATION` | Total monitoring duration in seconds | `60` |
| `PING_SUBNET` | CIDR notation subnet for sweep | — |
| `PING_LIMIT` | Max records to display in history | `50` |
| `PING_FORMAT` | Export format: `csv` or `json` | `json` |
| `PING_OUTPUT` | Output file path for export | stdout |
| `PING_KEY` | Config key to set | — |
| `PING_VALUE` | Config value to set | — |

## Examples

```bash
# Quick connectivity check
PING_TARGET="google.com" bash scripts/script.sh check

# Monitor DNS server for 5 minutes
PING_TARGET="8.8.8.8" PING_INTERVAL="10" PING_DURATION="300" bash scripts/script.sh monitor

# Compare DNS providers
PING_TARGETS="8.8.8.8,1.1.1.1,9.9.9.9" bash scripts/script.sh compare

# Export last week's data as CSV
PING_FORMAT="csv" bash scripts/script.sh export
```

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
