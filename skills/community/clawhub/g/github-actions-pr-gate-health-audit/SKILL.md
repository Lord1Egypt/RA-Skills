---
name: github-actions-pr-gate-health-audit
description: Audit pull-request and merge-queue GitHub Actions reliability by scoring failure rate, queue latency, and stale-success risk for merge gates.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions PR Gate Health Audit

Use this skill to detect unreliable pull-request merge gates before they block developers or hide degraded CI health.

## What this skill does
- Reads GitHub Actions run JSON exports
- Filters to PR/merge-gate events by default (`pull_request`, `pull_request_target`, `merge_group`)
- Groups by repository + workflow + event
- Scores risk using:
  - failure rate
  - consecutive current failures
  - average queue wait before run start
  - days since last successful run
- Flags warning/critical groups via configurable thresholds
- Emits text or JSON output for CI gates and operational dashboards

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS` (default: `2`)
- `EVENT_MATCH` (default: `^(pull_request|pull_request_target|merge_group)$`)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `FAIL_WARN_PERCENT` (default: `15`)
- `FAIL_CRITICAL_PERCENT` (default: `30`)
- `QUEUE_WARN_SECONDS` (default: `120`)
- `QUEUE_CRITICAL_SECONDS` (default: `300`)
- `SUCCESS_STALE_DAYS` (default: `3`)
- `WARN_SCORE` (default: `25`)
- `CRITICAL_SCORE` (default: `45`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,headSha,createdAt,runStartedAt,updatedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
EVENT_MATCH='^(pull_request|merge_group)$' \
MIN_RUNS=3 \
bash skills/github-actions-pr-gate-health-audit/scripts/pr-gate-health-audit.sh
```

JSON output with fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-pr-gate-health-audit/scripts/pr-gate-health-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-pr-gate-health-audit/fixtures/*.json' \
bash skills/github-actions-pr-gate-health-audit/scripts/pr-gate-health-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked PR gate risk groups
- JSON mode prints summary + scored groups + critical group details
