---
name: nuclei-analysis
description: Intelligently analyzes Nuclei scan results, prioritizes real bugs, reduces noise, and enriches findings with context.
version: 1.0.0
author: NyetNighy
tags: [bugbounty, nuclei, vulnerability-analysis, reporting]
metadata:
  {"openclaw":{"emoji":"🔬","os":["linux","darwin","win32"],"requires":{"bins":["nuclei","python3","node"]}}}
---

# Nuclei Analysis Skill

Parses raw Nuclei scan output and generates prioritized, actionable bug bounty reports.

## When to Use

Use this skill when:
- A Nuclei scan has completed and you want to turn raw output into a structured report
- You need to separate signal from noise in large scans
- You want severity-prioritized findings with business impact context

## Usage

```bash
python3 scripts/nuclei_analyzer.py /path/to/nuclei-output.txt
python3 scripts/nuclei_analyzer.py /path/to/nuclei-output.txt --min-severity high --output report.md
```

## Workflow

When user says "analyze nuclei results", "review scan", or similar:

1. Read the nuclei output file
2. Parse and categorize by severity and template type
3. Reduce noise (filter common false positives)
4. Enrich high/critical findings with business context
5. Generate a Markdown report

## Severity Levels

Nuclei severities (highest to lowest):
- `critical` — Immediate action required
- `high` — Significant risk, exploit likely
- `medium` — Moderate risk, requires context
- `low` — Minor risk, informational
- `info` — Informational, usually noise

## Noise Reduction

Filter out common false positives:
- Generic 403 Forbidden (without further context)
- Self-signed certificates (info only)
- Leaking server/version headers without actual exploit
- Template matches on redirect pages

## Output

Always produces:
- **Summary table** of all findings by severity
- **Detailed section** for High+ severity findings
- **Attack scenario** for critical/high issues
- **Steps to reproduce** for actionable findings

Report saved to: `reports/nuclei-analysis/<target>-<date>.md`

## Example Prompts

- "Analyze nuclei results for example.com"
- "Review scan findings and prioritize"
- "Turn nuclei.txt into a bug bounty report"

## Requirements

- Python 3.7+
- Nuclei installed and in PATH
- nuclei output in text format (newline-delimited JSON also supported)