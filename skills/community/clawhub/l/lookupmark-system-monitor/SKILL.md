---
name: system-monitor
description: >
  Monitor system health on the gateway host (Raspberry Pi / ARM / Linux).
  Reports CPU, RAM, disk, temperature, uptime, load, top processes.
  Can check alert thresholds for proactive notifications.
  Triggers on "system status", "system health", "pi status", "monitor",
  "how is the pi", "stato sistema", "temperatura", "ram usage", "disk space".
  NOT for: application-level monitoring, network monitoring, or remote hosts.
---

# System Monitor

Real-time system health monitoring for the gateway host. Zero external dependencies.

## Usage

```bash
# Full status report (human-readable)
python3 scripts/monitor.py

# JSON output (for programmatic use)
python3 scripts/monitor.py --json

# Check alert thresholds
python3 scripts/monitor.py --check-alerts

# Top N processes
python3 scripts/monitor.py --top 10
```

## What It Reports

| Metric | Source |
|--------|--------|
| CPU usage % | `/proc/stat` |
| RAM used/total/available | `/proc/meminfo` |
| Swap used/total | `/proc/meminfo` |
| Disk usage per mount | `df -h` |
| CPU temperature | `/sys/class/thermal/thermal_zone0/temp` |
| Uptime | `/proc/uptime` |
| Load average (1/5/15m) | `/proc/loadavg` |
| Top processes by CPU | `ps aux` |

## Alert Thresholds

Default (configurable in SKILL.md or via code):

| Alert | Threshold |
|-------|-----------|
| RAM | > 90% used |
| Swap | > 500MB used |
| CPU temp | > 75°C |
| Disk | > 90% full |

## Security

- **Read-only**: Never writes, modifies, or executes anything beyond reading system stats
- **No network access**: Purely local `/proc`, `/sys`, `ps`, `df`
- **No secrets**: Does not access config files, tokens, or credentials
- **Safe in groups**: Output contains no sensitive paths, tokens, or user data

## Automation

Use with cron for periodic health checks:

```bash
# Every 30 minutes via OpenClaw cron → alerts to Telegram
# Or via HEARTBEAT.md
```
