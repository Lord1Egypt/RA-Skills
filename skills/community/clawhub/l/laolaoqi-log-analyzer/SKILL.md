---
name: log-analyzer
description: Analyze server logs for error patterns, IP frequency, time-based analysis, and alert generation. Use when a user needs log file analysis, error pattern detection, anomaly/spike identification, top error messages, frequency aggregation, or time-based log analysis — works with syslog, custom log files, or piped input.
---

# Log Analyzer

## Script

`scripts/log-analyzer.sh` — the single entry point for all analyses.

The script is self-contained, works on any Linux system with standard tools (grep, awk, sort, uniq), and handles both file and piped input.

## Quick Start

Analyze `/var/log/syslog` with all checks:

```bash
bash scripts/log-analyzer.sh -f /var/log/syslog --all
```

Or pipe logs directly:

```bash
journalctl -u nginx --since "24 hours ago" | bash scripts/log-analyzer.sh --all
```

## Options

| Option | Description |
|---|---|
| `-f <file>` | Log file to analyze (use `-` for stdin) |
| `-p <pattern>` | Custom error pattern (default: error/i, fail/i, warn/i, critical/i, exception) |
| `-t <hours>` | Time window in hours (default: 24) |
| `--errors` | Find top error messages and their frequency |
| `--time-analysis` | Group errors by time period (hourly/daily) |
| `--ips` | Analyze IP frequency from log entries |
| `--spikes` | Identify unusual patterns and spikes |
| `--all` | Run all analyses (default if no option given) |
| `--help` | Show this help message |

## Analysis Modules

### Error Patterns (`--errors`)
Scans for configured error patterns, groups and sorts by frequency, shows the top most common error messages.

### Time-based Analysis (`--time-analysis`)
Groups errors into hourly and daily buckets to show when issues occur most frequently.

### IP Frequency (`--ips`)
Extracts IPv4 addresses from log entries, counts occurrences, and shows the top sources.

### Spike Detection (`--spikes`)
Compares error counts per time bucket against the average. Flags buckets that exceed 2x the average as potential anomalies.

## Common Findings & Recommendations

- **Repeated errors from the same source**: Check application/service health; consider rate limiting or restart
- **Time-based spikes**: Correlate with cron jobs, deployments, or traffic patterns at the flagged times
- **High-frequency IPs**: Could indicate brute-force attempts, scrapers, or DDoS — consider firewall rules or fail2ban
- **New error patterns appearing**: Recent changes or deployments may have introduced regressions
- **Sudden increase in warnings**: Often precedes critical failures — investigate proactively

## Notes

- Piped input reads from stdin; use `-f -` explicitly when piping
- For large log files (>100MB), consider reducing the time window with `-t` or pre-filtering with grep
- Time-based analysis expects standard syslog date formats (RFC 3164 or RFC 5424); custom formats may need adjustment
- IP detection uses a standard IPv4 regex — IPv6 is not currently supported
- Works without root for user-owned log files; system logs may require sudo
