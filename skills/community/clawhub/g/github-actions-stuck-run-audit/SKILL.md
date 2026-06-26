---
name: github-actions-stuck-run-audit
description: Detect stale queued/in-progress GitHub Actions runs before they quietly block delivery.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Stuck Run Audit

Use this skill to catch workflows that are stuck in queued/in-progress states for too long.

## What this skill does
- Reads GitHub Actions run JSON exports
- Detects stale runs in non-terminal statuses (`queued`, `in_progress`, etc.)
- Aggregates stuck risk by repo/workflow (or repo/branch)
- Scores severity with stuck-age, stuck-run volume, and stuck-rate thresholds
- Emits `ok` / `warn` / `critical` and can fail CI gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `GROUP_BY` (`repo`, `repo-workflow`, `repo-workflow-branch`; default: `repo-workflow`)
- `NOW_ISO` (optional ISO timestamp override for deterministic replay)
- `STUCK_STATUSES` (comma list, default: `queued,in_progress,pending,waiting,requested`)
- `WARN_STUCK_MINUTES` (default: `45`)
- `CRITICAL_STUCK_MINUTES` (default: `120`)
- `WARN_STUCK_RUNS` (default: `2`)
- `CRITICAL_STUCK_RUNS` (default: `4`)
- `WARN_STUCK_RATE` (0..1, default: `0.2`)
- `CRITICAL_STUCK_RATE` (0..1, default: `0.45`)
- `MIN_RUNS` (default: `1`)
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` / `BRANCH_EXCLUDE` (regex, optional)
- `EVENT_MATCH` / `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` / `REPO_EXCLUDE` (regex, optional)
- `STATUS_MATCH` / `STATUS_EXCLUDE` (regex, optional)
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
bash skills/github-actions-stuck-run-audit/scripts/stuck-run-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-stuck-run-audit/scripts/stuck-run-audit.sh
```

Run against bundled fixtures:

```bash
NOW_ISO='2026-03-08T00:00:00Z' \
RUN_GLOB='skills/github-actions-stuck-run-audit/fixtures/*.json' \
bash skills/github-actions-stuck-run-audit/scripts/stuck-run-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked stuck-risk groups
- JSON mode prints summary + ranked groups + critical groups
