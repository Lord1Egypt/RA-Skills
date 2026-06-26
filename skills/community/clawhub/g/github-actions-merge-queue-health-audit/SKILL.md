---
name: github-actions-merge-queue-health-audit
description: Audit GitHub merge queue workflow health with failure-rate, queue-latency, and stale-success risk scoring.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Merge Queue Health Audit

Use this skill to catch unhealthy `merge_group` (or pull-request gate) workflows before queue times and failures block merges.

## What this skill does
- Reads GitHub Actions run JSON exports
- Focuses on merge queue style events (`merge_group` by default)
- Aggregates health by repo/workflow (or repo/workflow/branch)
- Scores risk using failure rate, queue latency, and stale-success age
- Emits `ok` / `warn` / `critical` with optional CI fail gate

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `GROUP_BY` (`repo-workflow` or `repo-workflow-branch`, default: `repo-workflow`)
- `NOW_ISO` (optional ISO timestamp override for deterministic replay)
- `EVENTS` (comma list, default: `merge_group`)
- `WARN_FAILURE_RATE` (0..1, default: `0.2`)
- `CRITICAL_FAILURE_RATE` (0..1, default: `0.4`)
- `WARN_P95_QUEUE_MINUTES` (default: `8`)
- `CRITICAL_P95_QUEUE_MINUTES` (default: `20`)
- `WARN_STALE_SUCCESS_HOURS` (default: `18`)
- `CRITICAL_STALE_SUCCESS_HOURS` (default: `48`)
- `MIN_RUNS` (default: `3`)
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` / `BRANCH_EXCLUDE` (regex, optional)
- `REPO_MATCH` / `REPO_EXCLUDE` (regex, optional)
- `EVENT_MATCH` / `EVENT_EXCLUDE` (regex, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Collect run JSON

```bash
gh run view <run-id> \
  --json databaseId,workflowName,event,headBranch,status,conclusion,createdAt,runStartedAt,updatedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
bash skills/github-actions-merge-queue-health-audit/scripts/merge-queue-health-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-merge-queue-health-audit/scripts/merge-queue-health-audit.sh
```

Run against bundled fixtures:

```bash
NOW_ISO='2026-03-08T00:00:00Z' \
RUN_GLOB='skills/github-actions-merge-queue-health-audit/fixtures/*.json' \
bash skills/github-actions-merge-queue-health-audit/scripts/merge-queue-health-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked risk groups
- JSON mode prints summary + ranked groups + critical groups
