---
name: github-actions-runtime-regression-audit
description: Compare baseline vs current GitHub Actions run exports to catch workflow/job runtime regressions before CI costs and lead time spike.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Runtime Regression Audit

Use this skill to detect runtime regressions between historical baseline runs and current runs.

## What this skill does
- Reads baseline and current GitHub Actions run JSON exports (`gh run view --json ...`)
- Calculates average and p95 runtime per repository + workflow + job
- Compares current metrics against baseline and ranks largest regressions
- Flags warn/critical regressions by absolute seconds and percent delta
- Emits text summary for humans or JSON for automation

## Inputs
Required:
- `BASELINE_GLOB` (glob for baseline run JSON files)
- `CURRENT_GLOB` (glob for current run JSON files)

Optional:
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_DELTA_SECONDS` (default: `30`)
- `CRITICAL_DELTA_SECONDS` (default: `90`)
- `WARN_DELTA_PERCENT` (default: `15`)
- `CRITICAL_DELTA_PERCENT` (default: `35`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `JOB_MATCH` (regex, optional)
- `JOB_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,headSha,url,repository,jobs \
  > artifacts/github-actions/run-<run-id>.json
```

Capture a stable baseline window (for example previous 2 weeks), then current runs from latest commits.

## Run

Text report:

```bash
BASELINE_GLOB='artifacts/github-actions/baseline/*.json' \
CURRENT_GLOB='artifacts/github-actions/current/*.json' \
TOP_N=15 \
WARN_DELTA_SECONDS=45 \
CRITICAL_DELTA_SECONDS=120 \
bash skills/github-actions-runtime-regression-audit/scripts/runtime-regression-audit.sh
```

JSON output with CI gate:

```bash
BASELINE_GLOB='artifacts/github-actions/baseline/*.json' \
CURRENT_GLOB='artifacts/github-actions/current/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-runtime-regression-audit/scripts/runtime-regression-audit.sh
```

Run with bundled fixtures:

```bash
BASELINE_GLOB='skills/github-actions-runtime-regression-audit/fixtures/baseline-*.json' \
CURRENT_GLOB='skills/github-actions-runtime-regression-audit/fixtures/current-*.json' \
bash skills/github-actions-runtime-regression-audit/scripts/runtime-regression-audit.sh
```

## Output contract
- Exit `0` in reporting mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and at least one job crosses critical regression thresholds
- `text` mode prints summary + top regressions + new jobs without baseline
- `json` mode outputs summary, ranked regressions, and newly observed jobs
