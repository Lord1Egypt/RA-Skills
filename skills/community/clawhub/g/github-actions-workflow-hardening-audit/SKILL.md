---
name: github-actions-workflow-hardening-audit
description: Audit GitHub Actions workflow files for hardening gaps (missing timeouts/permissions/concurrency and floating action refs).
version: 1.1.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Workflow Hardening Audit

Use this skill to statically audit `.github/workflows/*.yml` files before risky defaults leak into production CI.

## What this skill does
- Scans workflow YAML files and scores hardening risk per file
- Flags jobs missing `timeout-minutes`
- Flags missing `permissions` declarations (workflow-level or job-level)
- Optionally flags missing `concurrency` controls
- Flags floating `uses:` refs (`@main`, `@master`, `@latest`, major-only tags like `@v4`)
- Supports file/event regex filtering for targeted triage in large monorepos
- Raises severity (`ok` / `warn` / `critical`) and can fail CI gates

## Inputs
Optional:
- `WORKFLOW_GLOB` (default: `.github/workflows/*.y*ml`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_SCORE` (default: `3`)
- `CRITICAL_SCORE` (default: `7`)
- `REQUIRE_TIMEOUT` (`0`/`1`, default: `1`)
- `REQUIRE_PERMISSIONS` (`0`/`1`, default: `1`)
- `REQUIRE_CONCURRENCY` (`0`/`1`, default: `0`)
- `FLAG_FLOATING_REFS` (`0`/`1`, default: `1`)
- `ALLOW_REF_REGEX` (regex whitelist for approved refs, optional)
- `WORKFLOW_FILE_MATCH` (regex include filter on file path, optional)
- `WORKFLOW_FILE_EXCLUDE` (regex exclude filter on file path, optional)
- `EVENT_MATCH` (regex include filter on parsed `on:` triggers, optional)
- `EVENT_EXCLUDE` (regex exclude filter on parsed `on:` triggers, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Run

Text report:

```bash
WORKFLOW_GLOB='.github/workflows/*.y*ml' \
bash skills/github-actions-workflow-hardening-audit/scripts/workflow-hardening-audit.sh
```

JSON output + fail gate:

```bash
WORKFLOW_GLOB='.github/workflows/*.y*ml' \
OUTPUT_FORMAT=json \
REQUIRE_CONCURRENCY=1 \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-workflow-hardening-audit/scripts/workflow-hardening-audit.sh
```

Filter to only PR-target workflows:

```bash
WORKFLOW_GLOB='.github/workflows/*.y*ml' \
EVENT_MATCH='pull_request_target' \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-workflow-hardening-audit/scripts/workflow-hardening-audit.sh
```

Run against bundled fixtures:

```bash
WORKFLOW_GLOB='skills/github-actions-workflow-hardening-audit/fixtures/*.y*ml' \
bash skills/github-actions-workflow-hardening-audit/scripts/workflow-hardening-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more workflows are critical
- Text mode prints summary + ranked workflow risks
- JSON mode prints summary + ranked workflows + critical workflows
