---
name: github-actions-cache-hardening-audit
description: Audit GitHub Actions workflow cache usage for poisoning, keying, and secret-path risks.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Cache Hardening Audit

Use this skill to statically audit `.github/workflows/*.yml` for risky cache patterns that can cause cache poisoning, stale cache churn, or secret leakage.

## What this skill checks
- `actions/cache` usage on untrusted triggers (`pull_request_target`)
- Cache keys that do not use `hashFiles(...)`
- Overly broad `restore-keys` prefixes
- Sensitive paths accidentally included in cache paths (`.aws`, `.ssh`, `.npmrc`, `.git`)
- Floating cache action refs (`@main`, `@master`)

## Inputs
Optional:
- `WORKFLOW_GLOB` (default: `.github/workflows/*.y*ml`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_SCORE` (default: `3`)
- `CRITICAL_SCORE` (default: `6`)
- `WORKFLOW_FILE_MATCH` (regex, optional)
- `WORKFLOW_FILE_EXCLUDE` (regex, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Run

Text report:

```bash
WORKFLOW_GLOB='.github/workflows/*.yml' \
bash skills/github-actions-cache-hardening-audit/scripts/cache-hardening-audit.sh
```

JSON output + fail gate:

```bash
WORKFLOW_GLOB='.github/workflows/*.yml' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-cache-hardening-audit/scripts/cache-hardening-audit.sh
```

Run against bundled fixtures:

```bash
WORKFLOW_GLOB='skills/github-actions-cache-hardening-audit/fixtures/*.yml' \
bash skills/github-actions-cache-hardening-audit/scripts/cache-hardening-audit.sh
```

## Output contract
- Exit `0` by default (report mode)
- Exit `1` when `FAIL_ON_CRITICAL=1` and at least one critical workflow is detected
- Text mode prints a summary and top flagged workflows
- JSON mode emits `summary`, `flagged_workflows`, and `critical_workflows`
