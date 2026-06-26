---
name: log-to-alert
description: >
  Use when (1) user pastes server, application, or system log text and wants to extract error patterns into 
  structured alert rules. (2) user says "create alerts from these logs", "monitor for this error", 
  "set up alerts for this pattern", or "extract warning conditions". (3) user pastes log output and asks 
  "alert me if this happens again". 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# Log to Alert

Use when (1) user pastes server, application, or system log text and wants to extract error patterns into structured alert rules. (2) user says "create alerts from these logs", "monitor for this error", "set up alerts for this pattern", or "extract warning conditions". (3) user pastes log output and asks "alert me if this happens again".

## Core Position

This skill solves the specific problem of: *recurring errors in logs need to become automated alert rules — not just documented, but actively monitored.*

This skill IS NOT:
- A log analysis tool — it does not produce statistics or dashboards
- A debugging tool — it does not fix the root cause
- A configuration manager — it outputs alert specs, not deployed hooks

This skill IS activated ONLY when: log text + alert creation intent are both present.

## Modes

### `/log-to-alert`

**Default mode.** Parses log entries, identifies error/warning patterns, and outputs structured alert rules.

When to use: User provides log text and wants alert rules (Prometheus, PagerDuty, Grafana, etc.)

### `/log-to-alert/dedupe`

Groups similar log lines into a single alert rule, eliminating duplicates.

When to use: Log contains many repeated instances of the same error.

## Execution Steps

### Step 1 — Parse the Log

1. Receive log text (pasted, file, or path)
2. Detect log format:
   - Structured (JSON): extract `level`, `message`, `timestamp`, `service`
   - Semi-structured (e.g., Nginx, Apache): parse using known regex patterns
   - Plain text: detect timestamp patterns, log levels, and error keywords
3. Classify each line:
   - `ERROR` / `FATAL` / `CRITICAL` → high severity
   - `WARN` / `WARNING` → medium severity
   - `INFO` / `DEBUG` → informational (usually not alert-worthy)
4. Identify recurring patterns (≥3 occurrences of similar message with same template)

### Step 2 — Extract Alert Patterns

For each error class found:

| Field | Source |
|---|---|
| Alert name | Derived from error type + service name |
| Match pattern | Regex extracted from error message template |
| Severity | From log level (ERROR→critical, WARN→warning) |
| Source service | From log source field or filename |
| Frequency threshold | Trigger count before alert fires (default: ≥3 in 5 min) |

### Step 3 — Format Alert Rule

Output in the target system's format:

**Prometheus AlertManager:**
```yaml
- alert: HighMemoryUsage
  expr: node_memory_MemAvailable / node_memory_MemTotal < 0.1
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High memory usage on {{ $labels.instance }}"
```

**Generic alert spec:**
```json
{
  "name": "DatabaseConnectionFailed",
  "pattern": "Connection refused|Connection timeout",
  "severity": "critical",
  "threshold": 3,
  "window": "5m",
  "action": "notify"
}
```

### Step 4 — Validate

- Every alert rule has a unique name
- Regex pattern matches the original error type without false positives
- No alert rule is duplicated from another
- Severity levels are consistent with log levels

## Mandatory Rules

### Do not

- Do not alert on INFO/DEBUG level entries
- Do not create alerts for one-off transient errors (only recurring patterns)
- Do not invent log sources not present in the text
- Do not set threshold to 1 (causes alert fatigue)

### Do

- Group similar error messages into a single alert rule
- Include the original error message as a comment in the alert rule
- Set severity to match log level (ERROR=critical, WARN=warning)
- Extract dynamic values as variables (IP, hostname, user ID), not hardcoded

## Quality Bar

**A good output:**
- Each recurring error type has exactly one alert rule
- Regex patterns are specific enough to match the error but not generic logs
- Alert names clearly identify the error type and service
- Severity matches the log level from the source

**A bad output:**
- Creates separate alerts for every log line (no deduplication)
- Matches all log lines including INFO-level (false positives)
- Hardcodes dynamic values (specific IPs, timestamps) in patterns
- Alert names are generic like "Error Alert 1"

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| 500 identical error lines | 500 separate alert rules | 1 alert rule with threshold=3 |
| Dynamic error message | Pattern matches literal string | Pattern uses regex: `user \d+ not found` |
| Multiple services in logs | All alerts named "Error" | Alerts named by service: `auth-DB-connection-failed` |
| One INFO log line | Creates an alert | Skipped — INFO not alert-worthy |

## References

- `references/` — Regex extraction patterns, alert format schemas for Prometheus/Grafana/PagerDuty