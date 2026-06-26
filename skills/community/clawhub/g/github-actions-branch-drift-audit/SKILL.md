---
name: github-actions-branch-drift-audit
description: Detect branch-level GitHub Actions reliability drift by comparing failure and runtime deltas against a mainline baseline.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Branch Drift Audit

Use this skill to catch branch-specific CI reliability regressions before they spread into your mainline release flow.

## What this skill does
- Reads GitHub Actions run JSON exports
- Groups runs by repository + workflow + branch
- Selects a baseline branch per repository/workflow (defaults to `main|master`)
- Compares each non-baseline branch against that baseline on:
  - failure-rate drift (percentage points)
  - average runtime drift (ratio)
- Flags warning/critical drift severity and supports CI fail gates
- Emits text or JSON output for pipeline checks and triage dashboards

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS_PER_BRANCH` (default: `2`)
- `MIN_BRANCHES` (default: `2`)
- `BASELINE_BRANCH_MATCH` (default: `^(main|master)$`)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `FAILURE_DRIFT_WARN_PP` (default: `10`)
- `FAILURE_DRIFT_CRITICAL_PP` (default: `25`)
- `RUNTIME_DRIFT_WARN_RATIO` (default: `1.25`)
- `RUNTIME_DRIFT_CRITICAL_RATIO` (default: `1.6`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,headSha,createdAt,updatedAt,startedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
BASELINE_BRANCH_MATCH='^(main|release/.*)$' \
MIN_RUNS_PER_BRANCH=3 \
bash skills/github-actions-branch-drift-audit/scripts/branch-drift-audit.sh
```

JSON output with fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-branch-drift-audit/scripts/branch-drift-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-branch-drift-audit/fixtures/*.json' \
bash skills/github-actions-branch-drift-audit/scripts/branch-drift-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more drift rows are critical
- Text mode prints summary + ranked branch drift rows
- JSON mode prints summary + drift rows + critical-only slice
