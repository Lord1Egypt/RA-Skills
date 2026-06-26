---
name: github-actions-oidc-hardening-audit
description: Audit GitHub Actions cloud auth workflows for OIDC hardening gaps like missing id-token write permissions, static cloud secrets, and floating auth action refs.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions OIDC Hardening Audit

Use this skill to catch risky cloud-auth patterns in workflow YAML before they become identity or secret exposure incidents.

## What this skill does
- Scans workflow YAML files (`.github/workflows/*.yml` by default)
- Detects AWS/GCP/Azure auth action usage:
  - `aws-actions/configure-aws-credentials`
  - `google-github-actions/auth`
  - `azure/login`
- Flags workflows that use cloud auth actions but miss `permissions.id-token: write`
- Flags AWS auth usage without `role-to-assume`
- Flags likely static cloud credential usage (`aws-access-key-id`, `aws-secret-access-key`, cloud credential secrets)
- Flags floating auth action refs (`@main`, `@master`, `@v1`) unless allow-listed
- Supports text/json output and CI fail gate

## Inputs
Optional:
- `WORKFLOW_GLOB` (default: `.github/workflows/*.y*ml`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_SCORE` (default: `3`)
- `CRITICAL_SCORE` (default: `7`)
- `WORKFLOW_FILE_MATCH` / `WORKFLOW_FILE_EXCLUDE` (regex, optional)
- `ALLOW_REF_REGEX` (regex, optional) — allow-listed action refs
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Run

Text report:

```bash
WORKFLOW_GLOB='.github/workflows/*.yml' \
WARN_SCORE=3 \
CRITICAL_SCORE=7 \
bash skills/github-actions-oidc-hardening-audit/scripts/oidc-hardening-audit.sh
```

JSON output + fail gate:

```bash
WORKFLOW_GLOB='.github/workflows/*.y*ml' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-oidc-hardening-audit/scripts/oidc-hardening-audit.sh
```

Run against bundled fixtures:

```bash
WORKFLOW_GLOB='skills/github-actions-oidc-hardening-audit/fixtures/*.y*ml' \
bash skills/github-actions-oidc-hardening-audit/scripts/oidc-hardening-audit.sh
```

## Output contract
- Exit `0` in reporting mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more workflows are critical
- Text mode prints summary + top risky workflows
- JSON mode prints summary + flagged workflows + critical workflows
