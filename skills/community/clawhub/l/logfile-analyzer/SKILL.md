---
name: log-analyzer
description: Analyze application logs to produce actionable error digests with pattern detection, severity classification, trend analysis, and remediation recommendations. Supports auto-detection of common log formats including syslog, JSON structured logs, Apache/Nginx access and error logs, Python tracebacks, Node.js errors, Docker logs, and generic timestamped formats. Use when asked to analyze logs, debug errors from log files, find recurring issues in logs, create error reports from log data, investigate production incidents from logs, summarize log output, identify error patterns, check application health from logs, or parse server logs. Triggers on "analyze logs", "check logs", "log errors", "error digest", "parse logs", "log report", "what's failing", "production errors", "log summary", "incident analysis", "error patterns".
---

# Log Analyzer

Parse application logs into actionable error digests with pattern grouping, severity classification, trend detection, and remediation recommendations.

## Quick Start

```bash
# Analyze a single log file
python3 scripts/analyze_logs.py /var/log/app.log

# Analyze all logs in a directory
python3 scripts/analyze_logs.py /var/log/myapp/

# Last 24 hours only, errors and above
python3 scripts/analyze_logs.py /var/log/app.log --since 24h --severity error

# JSON output for programmatic use
python3 scripts/analyze_logs.py /var/log/app.log --output json

# Markdown report with trends
python3 scripts/analyze_logs.py /var/log/app.log --output markdown --trends

# Ignore noisy patterns
python3 scripts/analyze_logs.py /var/log/app.log --ignore "healthcheck" --ignore "GET /favicon"
```

## Supported Formats (Auto-Detected)

- **JSON structured** — Bunyan, Winston, Pino, structlog, any `{"level": ..., "msg": ...}` format
- **Syslog** — RFC 3164 (`Mar 28 02:31:00 host service: msg`)
- **Apache/Nginx access** — Combined log format
- **Nginx error** — `2026/03/28 02:31:00 [error] ...`
- **Python tracebacks** — Multi-line traceback collection
- **Docker** — ISO 8601 timestamps with container output
- **Generic timestamped** — `[2026-03-28 02:31:00] LEVEL: message`

Force format with `--format <name>` if auto-detection fails.

## What It Does

1. **Parses** log entries with format auto-detection
2. **Classifies** severity (TRACE → DEBUG → INFO → WARN → ERROR → FATAL)
3. **Normalizes** messages (replaces UUIDs, IPs, timestamps, paths with placeholders)
4. **Groups** similar errors by fingerprint to find recurring patterns
5. **Ranks** by severity and frequency
6. **Detects trends** with `--trends` (hourly frequency buckets)
7. **Recommends fixes** for 15+ known error patterns (OOM, connection refused, disk full, timeouts, SSL issues, rate limits, etc.)

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--format` | auto | Force log format |
| `--since` | all | Time filter (`1h`, `24h`, `7d`, or ISO date) |
| `--severity` | warn | Minimum severity to report |
| `--top` | 20 | Number of top patterns to show |
| `--output` | text | Output format: text, json, markdown |
| `--trends` | off | Show hourly frequency trends |
| `--ignore` | none | Regex patterns to exclude (repeatable) |
| `-q` | off | Summary only, skip individual entries |

## Exit Codes

- `0` — No errors found
- `1` — Errors found (warn/error level)
- `2` — Fatal/critical entries found

Use in CI/CD pipelines to fail builds on log errors.

## Workflow

### Incident Investigation

1. Run with `--since 1h --severity error --trends` to see recent errors with frequency
2. Review top patterns — the most frequent errors are usually the root cause
3. Check recommendations for known patterns
4. Use `--output json` to feed into monitoring dashboards

### Periodic Health Check

1. Run with `--since 24h --output markdown` for a daily report
2. Compare pattern counts across days to spot trends
3. Set up as cron job for automated daily digests

### Deep Dive

1. Run with `--severity debug` to see full picture
2. Use `--ignore` to filter out known noise
3. Check `references/error-patterns.md` for detailed remediation steps on specific error types

## Error Pattern Reference

For detailed remediation guidance on specific error types (memory, network, database, SSL, etc.), see `references/error-patterns.md`.
