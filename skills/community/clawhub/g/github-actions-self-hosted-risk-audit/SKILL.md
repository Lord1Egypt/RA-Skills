---
name: github-actions-self-hosted-risk-audit
description: Audit GitHub Actions workflows that use self-hosted runners for untrusted trigger and credential-hardening risks.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Self-Hosted Risk Audit

Use this skill to flag risky workflow patterns when jobs run on self-hosted GitHub Actions runners.

## What this skill does
- Scans workflow YAML files (`.github/workflows/*.yml` by default)
- Detects workflows that reference `self-hosted` runners
- Flags high-risk trigger combinations (`pull_request_target`, `pull_request`, `issue_comment`)
- Flags broad/self-hosted-only runner selection (no extra routing labels)
- Flags workflows with write-capable permissions in self-hosted contexts
- Flags `actions/checkout` steps that do not set `persist-credentials: false`
- Supports text/json output and CI fail gate

## Inputs
Optional:
- `WORKFLOW_GLOB` (default: `.github/workflows/*.y*ml`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_SCORE` (default: `4`)
- `CRITICAL_SCORE` (default: `8`)
- `WORKFLOW_FILE_MATCH` / `WORKFLOW_FILE_EXCLUDE` (regex, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Run

Text report:

```bash
WORKFLOW_GLOB='.github/workflows/*.yml' \
WARN_SCORE=4 \
CRITICAL_SCORE=8 \
bash skills/github-actions-self-hosted-risk-audit/scripts/self-hosted-risk-audit.sh
```

JSON output + fail gate:

```bash
WORKFLOW_GLOB='.github/workflows/*.y*ml' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-self-hosted-risk-audit/scripts/self-hosted-risk-audit.sh
```

Run against bundled fixtures:

```bash
WORKFLOW_GLOB='skills/github-actions-self-hosted-risk-audit/fixtures/*.y*ml' \
bash skills/github-actions-self-hosted-risk-audit/scripts/self-hosted-risk-audit.sh
```

## Output contract
- Exit `0` in reporting mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more workflows are critical
- Text mode prints summary + top flagged workflows
- JSON mode prints summary + flagged workflows + critical workflows
