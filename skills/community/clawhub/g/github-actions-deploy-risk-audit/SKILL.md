---
name: github-actions-deploy-risk-audit
description: Audit deployment workflow risk from GitHub Actions runs by scoring failure rate, unresolved failure streaks, and time since last successful deploy.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Deploy Risk Audit

Use this skill to rank deployment workflows that are currently risky to trust for production releases.

## What this skill does
- Reads GitHub Actions run JSON exports
- Filters to deployment/release workflows (configurable regex)
- Groups by repository + workflow + branch
- Scores risk using:
  - failure rate
  - unresolved trailing failure streak
  - days since last successful run
- Flags warning/critical groups based on configurable score thresholds
- Emits text or JSON output for CI dashboards and release gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS` (default: `2`)
- `DEPLOY_WORKFLOW_MATCH` (default: `(?i)(deploy|release|ship|production)`)
- `BRANCH_MATCH` (regex, optional)
- `BRANCH_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `FAIL_WARN_PERCENT` (default: `20`)
- `FAIL_CRITICAL_PERCENT` (default: `40`)
- `STALE_SUCCESS_DAYS` (default: `7`)
- `WARN_SCORE` (default: `35`)
- `CRITICAL_SCORE` (default: `60`)
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
DEPLOY_WORKFLOW_MATCH='(?i)(deploy|release)' \
MIN_RUNS=3 \
bash skills/github-actions-deploy-risk-audit/scripts/deploy-risk-audit.sh
```

JSON output with fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-deploy-risk-audit/scripts/deploy-risk-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-deploy-risk-audit/fixtures/*.json' \
bash skills/github-actions-deploy-risk-audit/scripts/deploy-risk-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked deploy risk groups
- JSON mode prints summary + scored groups + critical group details
