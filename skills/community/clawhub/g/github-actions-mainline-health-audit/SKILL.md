---
name: github-actions-mainline-health-audit
description: Audit GitHub Actions mainline branch reliability by scoring failure rate, consecutive failures, and stale-success risk for critical workflows.
version: 1.4.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Mainline Health Audit

Use this skill to detect unstable workflows on protected branches (main/master/release) before they silently degrade delivery confidence.

## What this skill does
- Reads GitHub Actions run JSON exports
- Filters to mainline/protected branches (configurable regex)
- Groups by repository + workflow + branch + event
- Scores risk using:
  - failure rate
  - current consecutive failure streak
  - days since last successful run
- Flags warning/critical groups based on configurable thresholds
- Emits text or JSON output for CI checks and ops dashboards

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS` (default: `2`)
- `MAINLINE_BRANCH_MATCH` (default: `^(main|master|release.*)$`)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `EVENT_MATCH` (regex, optional)
- `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `HEAD_SHA_MATCH` (regex, optional)
- `HEAD_SHA_EXCLUDE` (regex, optional)
- `CONCLUSION_MATCH` (regex, optional)
- `CONCLUSION_EXCLUDE` (regex, optional)
- `RUN_ID_MATCH` (regex, optional)
- `RUN_ID_EXCLUDE` (regex, optional)
- `RUN_URL_MATCH` (regex, optional)
- `RUN_URL_EXCLUDE` (regex, optional)
- `FAIL_WARN_PERCENT` (default: `20`)
- `FAIL_CRITICAL_PERCENT` (default: `40`)
- `STALE_SUCCESS_DAYS` (default: `7`)
- `WARN_SCORE` (default: `30`)
- `CRITICAL_SCORE` (default: `55`)
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
MAINLINE_BRANCH_MATCH='^(main|release/.*)$' \
HEAD_SHA_MATCH='^[a-f0-9]{7,40}$' \
CONCLUSION_EXCLUDE='^(success)$' \
RUN_ID_MATCH='^50(0[1-5])$' \
MIN_RUNS=3 \
bash skills/github-actions-mainline-health-audit/scripts/mainline-health-audit.sh
```

JSON output with fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-mainline-health-audit/scripts/mainline-health-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-mainline-health-audit/fixtures/*.json' \
bash skills/github-actions-mainline-health-audit/scripts/mainline-health-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked mainline-risk groups
- JSON mode prints summary + scored groups + critical group details
