---
name: github-actions-conclusion-volatility-audit
description: Audit GitHub Actions workflow conclusion volatility to surface unstable pipelines before they become chronic failures.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Conclusion Volatility Audit

Use this skill to detect unstable workflows that frequently flip between success and failure-like outcomes.

## What this skill does
- Reads one or more workflow run JSON exports
- Groups runs by repository + workflow + branch
- Calculates volatility using conclusion transitions across run history
- Flags groups by warn/critical instability thresholds
- Emits text or JSON output for CI reporting and quality gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS` (default: `5`) — minimum runs before severity is applied
- `WARN_INSTABILITY_PCT` (default: `35`)
- `CRITICAL_INSTABILITY_PCT` (default: `60`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `WORKFLOW_MATCH`, `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH`, `BRANCH_EXCLUDE` (regex, optional)
- `REPO_MATCH`, `REPO_EXCLUDE` (regex, optional)

Failure-like conclusions are: `failure`, `cancelled`, `timed_out`, `action_required`, `startup_failure`.

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,conclusion,createdAt,updatedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WARN_INSTABILITY_PCT=35 \
CRITICAL_INSTABILITY_PCT=60 \
bash skills/github-actions-conclusion-volatility-audit/scripts/conclusion-volatility-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-conclusion-volatility-audit/scripts/conclusion-volatility-audit.sh
```

## Output contract
- Exit `0` in reporting mode
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more critical groups are found
- Text output includes summary and top unstable workflow groups
- JSON output includes `summary`, ranked `groups`, and `critical_groups`
