---
name: github-actions-retry-recovery-audit
description: Audit GitHub Actions runs for fail-then-success retry recovery patterns to quantify flaky rerun waste.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Retry Recovery Audit

Use this skill to find workflow/job slices that repeatedly fail before eventually succeeding, so teams can target flaky reruns with the biggest minute waste.

## What this skill does
- Reads one or more GitHub Actions workflow run JSON exports
- Groups attempts by repository/workflow/branch/commit (`headSha`)
- Detects recovery sequences where one or more failure-like attempts are followed by success
- Calculates wasted minutes consumed before first success in each sequence
- Emits text or JSON output for triage dashboards and CI fail gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_WASTE_MINUTES` (default: `20`)
- `CRITICAL_WASTE_MINUTES` (default: `60`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `WORKFLOW_MATCH`, `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH`, `BRANCH_EXCLUDE` (regex, optional)
- `REPO_MATCH`, `REPO_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,headSha,conclusion,createdAt,updatedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WARN_WASTE_MINUTES=20 \
CRITICAL_WASTE_MINUTES=60 \
bash skills/github-actions-retry-recovery-audit/scripts/retry-recovery-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-retry-recovery-audit/scripts/retry-recovery-audit.sh
```

## Output contract
- Exit `0` in report mode
- Exit `1` when `FAIL_ON_CRITICAL=1` and critical recoveries are present
- Text output includes summary plus top recovery groups ranked by wasted minutes
- JSON output includes `summary`, ranked `recoveries`, and `critical_recoveries`
