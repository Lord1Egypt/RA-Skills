---
name: github-actions-secret-exposure-audit
description: Audit GitHub Actions workflow files for secret exposure risks like pull_request_target secret usage, secret echo commands, and unpinned action secret passing.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Secret Exposure Audit

Use this skill to catch risky secret handling patterns in workflow YAML before they leak credentials or allow unsafe token use.

## What this skill does
- Scans workflow YAML files (`.github/workflows/*.yml` by default)
- Flags `pull_request_target` workflows that also reference `${{ secrets.* }}`
- Flags shell output commands that print secret expressions (`echo`, `printf`, `tee`, `::set-output`)
- Flags secret values passed into unpinned third-party actions (`@main`, `@master`, `@v1`, etc.)
- Flags likely hardcoded credential values in workflow config
- Supports text/json output and CI fail gate

## Inputs
Optional:
- `WORKFLOW_GLOB` (default: `.github/workflows/*.y*ml`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_SCORE` (default: `4`)
- `CRITICAL_SCORE` (default: `8`)
- `WORKFLOW_FILE_MATCH` / `WORKFLOW_FILE_EXCLUDE` (regex, optional)
- `ALLOW_REF_REGEX` (regex, optional) — allow listed action refs (for example `^v1\.2\.3$`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Run

Text report:

```bash
WORKFLOW_GLOB='.github/workflows/*.yml' \
WARN_SCORE=4 \
CRITICAL_SCORE=8 \
bash skills/github-actions-secret-exposure-audit/scripts/secret-exposure-audit.sh
```

JSON output + fail gate:

```bash
WORKFLOW_GLOB='.github/workflows/*.y*ml' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-secret-exposure-audit/scripts/secret-exposure-audit.sh
```

Run against bundled fixtures:

```bash
WORKFLOW_GLOB='skills/github-actions-secret-exposure-audit/fixtures/*.y*ml' \
bash skills/github-actions-secret-exposure-audit/scripts/secret-exposure-audit.sh
```

## Output contract
- Exit `0` in reporting mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more workflows are critical
- Text mode prints summary + top risky workflows
- JSON mode prints summary + ranked workflows + critical workflows
