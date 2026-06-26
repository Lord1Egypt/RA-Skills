---
name: jrv-log-analyzer
description: Analyze log files to detect error patterns, aggregate by severity, group repeated errors by fingerprint, and flag anomaly time windows. Use when asked to analyze logs, find errors in log files, debug server issues from logs, summarize log output, or identify error spikes. Supports syslog, application logs, nginx/apache logs, and any text-based log format.
---

# Log Analyzer

Analyze any text-based log file for error patterns, severity breakdown, and anomaly detection.

## Quick Start

```bash
python3 scripts/analyze_logs.py <logfile>
python3 scripts/analyze_logs.py app.log --top 20 --severity ERROR
python3 scripts/analyze_logs.py server.log --json --since "2026-03-01"
```

## Features

- **Severity classification** — auto-detects FATAL, ERROR, WARN, INFO, DEBUG from log lines
- **Error fingerprinting** — groups similar errors by stripping variable parts (IPs, UUIDs, PIDs, timestamps)
- **Anomaly detection** — flags hours with error rates >2x the average
- **Timestamp parsing** — handles ISO 8601, syslog, and nginx/apache formats
- **Flexible output** — human-readable report or `--json` for piping

## Options

| Flag | Description |
|------|-------------|
| `--top N` | Number of top error patterns (default: 15) |
| `--severity LEVEL` | Minimum severity filter (FATAL, ERROR, WARN, INFO, DEBUG) |
| `--json` | Output structured JSON |
| `--since TIMESTAMP` | Only analyze lines after this timestamp |

## Workflow

1. Run the analyzer on the target log file
2. Review severity breakdown for overall health
3. Check top error patterns for recurring issues
4. Look at anomaly hours for incident windows
5. Use `--json` output to feed into other tools or reports
