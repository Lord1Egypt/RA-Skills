# Log To Alert

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Extracts error patterns from server logs and converts them into structured alert rules for monitoring

## What Problem This Solves

Recurring errors in logs keep appearing but nobody has time to manually create alert rules. This skill parses log entries, identifies error/warning patterns (≥3 occurrences = recurring), and outputs ready-to-use alert specs for Prometheus, Grafana, or PagerDuty.

**When triggered:** Log text + alert/monitor/create rule intent.

## Features

- **Multi-format log parsing** — handles JSON logs, semi-structured (Nginx/Apache), and plain text logs
- **Automatic deduplication** — groups identical error messages into one rule with frequency threshold
- **Severity classification** — ERROR/FATAL → critical, WARN → warning, INFO/DEBUG → skipped
- **Dynamic value extraction** — converts hardcoded IPs, hostnames, user IDs to regex variables

## Quick Start

```bash
# Via ClawHub
clawhub install log-to-alert

# Or manually
cp -r log-to-alert ~/.openclaw/skills/
```

### Usage

```
/log-to-alert
```

Paste logs, ask to create alert rules.

```
/log-to-alert/dedupe
```

Groups similar log lines into a single alert, eliminating duplicates.

## Modes

| Mode | Description |
|------|-------------|
| `/log-to-alert` | Parses logs, outputs alert rules (Prometheus, Grafana, etc.) |
| `/log-to-alert/dedupe` | Groups similar errors into one rule with threshold |

## Examples

| Scenario | Output |
|----------|--------|
| 500 identical error lines | 1 alert rule with `threshold: 3` — not 500 separate alerts |
| Dynamic error: "user 123 not found" | Pattern: `user \d+ not found` (not literal string) |
| Multiple services in logs | Alerts named by service: `auth-DB-connection-failed` |
| One INFO log line | Skipped — INFO level is not alert-worthy |

## Directory Structure

```
log-to-alert/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # Regex patterns, alert format schemas
└── tests/
```

## License

MIT License — see [LICENSE](LICENSE).