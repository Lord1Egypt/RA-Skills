---
name: github-actions-duplicate-run-audit
description: Detect duplicate GitHub Actions run bursts by workflow/branch/commit and quantify wasted rerun minutes.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Duplicate Run Audit

Use this skill to detect accidental duplicate workflow execution bursts (for example trigger overlap, force-push storms, or retried dispatches) and measure wasted CI minutes.

## What this skill does
- Reads GitHub Actions run JSON exports
- Groups runs by repository + workflow + branch + event + commit SHA
- Clusters bursts where runs happen inside a configurable time window
- Counts duplicate runs and estimates wasted runtime minutes
- Scores severity (`ok`, `warn`, `critical`) for CI hygiene enforcement
- Emits text or JSON for automation

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `DUPLICATE_WINDOW_MINUTES` (default: `30`)
- `MIN_DUPLICATE_RUNS` (default: `2`)
- `WARN_DUPLICATE_RUNS` (default: `3`)
- `CRITICAL_DUPLICATE_RUNS` (default: `6`)
- `WARN_WASTED_MINUTES` (default: `20`)
- `CRITICAL_WASTED_MINUTES` (default: `60`)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` (regex, optional)
- `BRANCH_EXCLUDE` (regex, optional)
- `EVENT_MATCH` (regex, optional)
- `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `HEAD_SHA_MATCH` (regex, optional)
- `HEAD_SHA_EXCLUDE` (regex, optional)
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
DUPLICATE_WINDOW_MINUTES=20 \
bash skills/github-actions-duplicate-run-audit/scripts/duplicate-run-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-duplicate-run-audit/scripts/duplicate-run-audit.sh
```

Run against bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-duplicate-run-audit/fixtures/*.json' \
bash skills/github-actions-duplicate-run-audit/scripts/duplicate-run-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked duplicate-run groups
- JSON mode prints summary + ranked groups + critical groups
