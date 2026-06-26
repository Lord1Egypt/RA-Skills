---
name: log-analyzer
description: Read a log file, extract ERROR/WARN/CRITICAL lines, group similar messages, and produce a concise summary report. Use when analyzing application logs, agent logs, service logs, or audit outputs for repeated failures, warning clusters, or critical events.
---

# Log Analyzer

Read a target log file, isolate important severity lines, group similar messages, and emit a Markdown summary.

## Workflow

1. Confirm the input log path.
2. Run `index.js` with `--input <logfile>` and optional `--out <report.md>`.
3. Review the grouped output for dominant error families.
4. Use the report as a triage artifact, not as the only source of truth.

## Output

Always include:
- total scanned lines
- WARN / ERROR / CRITICAL counts
- grouped issue buckets
- sample lines
- suggested first checks
