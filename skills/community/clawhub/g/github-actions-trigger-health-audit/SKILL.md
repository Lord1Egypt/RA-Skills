---
name: github-actions-trigger-health-audit
description: Audit GitHub Actions run health by trigger event and workflow so flaky or noisy automation sources are easy to prioritize.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Trigger Health Audit

Use this skill to find which GitHub Actions trigger events are driving the highest failure rates.

## What this skill does
- Reads one or more GitHub Actions run JSON exports
- Groups runs by repository + event + workflow
- Calculates failure/cancel/timeout rates and average runtime
- Flags warning/critical hotspots based on configurable failure-rate thresholds
- Supports regex include/exclude filters for repo, workflow, and event
- Emits text or JSON output for dashboards and automation gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS` (default: `2`) — skip low-sample groups
- `FAIL_WARN_PERCENT` (default: `20`)
- `FAIL_CRITICAL_PERCENT` (default: `40`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `EVENT_MATCH` (regex, optional)
- `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,headSha,createdAt,updatedAt,startedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
MIN_RUNS=3 \
FAIL_WARN_PERCENT=25 \
FAIL_CRITICAL_PERCENT=50 \
bash skills/github-actions-trigger-health-audit/scripts/trigger-health-audit.sh
```

JSON output with fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-trigger-health-audit/scripts/trigger-health-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-trigger-health-audit/fixtures/*.json' \
bash skills/github-actions-trigger-health-audit/scripts/trigger-health-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and any group meets critical threshold
- Text mode prints summary + ranked trigger health hotspots
- JSON mode prints summary + grouped metrics + critical group details
