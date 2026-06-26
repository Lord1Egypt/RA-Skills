---
name: github-actions-permission-scope-audit
description: Audit GitHub Actions workflow permission scope drift to enforce least-privilege token access.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Permission Scope Audit

Use this skill to detect over-broad `GITHUB_TOKEN` permissions and scope drift across GitHub Actions workflows.

## What this skill does
- Reads workflow YAML files
- Detects explicit broad permission grants (`write-all`, `contents: write`, etc.)
- Flags risky patterns like `pull_request_target` workflows with write permissions
- Identifies workflows with no explicit `permissions` policy
- Emits text or JSON for CI triage and policy gates

## Inputs
Optional:
- `WORKFLOW_GLOB` (default: `.github/workflows/*.y*ml`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_SCORE` (default: `2`)
- `CRITICAL_SCORE` (default: `5`)
- `FLAG_MISSING_PERMISSIONS` (`0` or `1`, default: `1`)
- `FLAG_WRITE_ALL` (`0` or `1`, default: `1`)
- `FLAG_WRITE_SCOPES` (`0` or `1`, default: `1`)
- `WORKFLOW_FILE_MATCH` / `WORKFLOW_FILE_EXCLUDE` (regex, optional)
- `EVENT_MATCH` / `EVENT_EXCLUDE` (regex, optional)
- `PERMISSION_MATCH` / `PERMISSION_EXCLUDE` (regex, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Run

Text report:

```bash
WORKFLOW_GLOB='.github/workflows/*.yml' \
bash skills/github-actions-permission-scope-audit/scripts/permission-scope-audit.sh
```

JSON output + fail gate:

```bash
WORKFLOW_GLOB='.github/workflows/*.yml' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-permission-scope-audit/scripts/permission-scope-audit.sh
```

Run against bundled fixtures:

```bash
WORKFLOW_GLOB='skills/github-actions-permission-scope-audit/fixtures/*.yml' \
bash skills/github-actions-permission-scope-audit/scripts/permission-scope-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more workflows are critical
- Text mode prints summary + ranked workflows
- JSON mode prints summary + ranked workflows + critical workflows
