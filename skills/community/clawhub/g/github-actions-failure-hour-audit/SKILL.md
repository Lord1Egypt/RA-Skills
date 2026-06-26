---
name: github-actions-failure-hour-audit
description: Audit GitHub Actions failure timing by day/hour to surface recurring outage windows and staffing hotspots.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Failure Hour Audit

Use this skill to identify when failures cluster so teams can target flaky time windows and on-call coverage.

## What this skill does
- Reads one or more GitHub Actions workflow run JSON exports
- Keeps only failure-like conclusions (`failure`, `cancelled`, `timed_out`, `action_required`, `startup_failure`)
- Buckets failures into day/hour windows (with optional timezone offset)
- Ranks windows by severity using failure-run thresholds
- Emits text or JSON output for dashboards or CI gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `24`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_FAILURE_RUNS` (default: `3`)
- `CRITICAL_FAILURE_RUNS` (default: `6`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `TZ_OFFSET_HOURS` (default: `0`) — integer timezone shift from UTC, between `-23` and `23`
- `WORKFLOW_MATCH`, `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH`, `BRANCH_EXCLUDE` (regex, optional)
- `REPO_MATCH`, `REPO_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,conclusion,createdAt,updatedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WARN_FAILURE_RUNS=3 \
CRITICAL_FAILURE_RUNS=6 \
TZ_OFFSET_HOURS=7 \
bash skills/github-actions-failure-hour-audit/scripts/failure-hour-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-failure-hour-audit/scripts/failure-hour-audit.sh
```

## Output contract
- Exit `0` in reporting mode
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more critical windows are found
- Text output includes summary and top windows by severity
- JSON output includes `summary`, ranked `windows`, and `critical_windows`
