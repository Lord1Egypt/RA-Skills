---
name: github-actions-manual-trigger-audit
description: Audit manual GitHub Actions trigger dependence by workflow/event to flag automation gaps and intervention risk.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Manual Trigger Audit

Use this skill to detect workflows that rely too heavily on manual triggers (`workflow_dispatch` / `repository_dispatch`) instead of automated CI events.

## What this skill does
- Reads GitHub Actions run JSON exports
- Groups runs by repository + workflow (+ branch)
- Measures manual-trigger share vs total run volume
- Tracks recent manual-trigger streaks (latest N runs)
- Scores severity (`ok`, `warn`, `critical`) for operational risk gating
- Emits text or JSON output for automation

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `GROUP_BY` (`workflow` or `workflow-branch`, default: `workflow`)
- `MANUAL_EVENTS` (comma-separated, default: `workflow_dispatch,repository_dispatch`)
- `RECENT_WINDOW` (latest runs inspected for streak, default: `5`)
- `MIN_RUNS` (minimum runs required, default: `5`)
- `WARN_MANUAL_RATIO` (0..1, default: `0.35`)
- `CRITICAL_MANUAL_RATIO` (0..1, default: `0.65`)
- `WARN_MANUAL_RUNS` (default: `5`)
- `CRITICAL_MANUAL_RUNS` (default: `12`)
- `WARN_RECENT_MANUAL_STREAK` (default: `3`)
- `CRITICAL_RECENT_MANUAL_STREAK` (default: `5`)
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` / `BRANCH_EXCLUDE` (regex, optional)
- `EVENT_MATCH` / `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` / `REPO_EXCLUDE` (regex, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,event,headBranch,conclusion,createdAt,updatedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
bash skills/github-actions-manual-trigger-audit/scripts/manual-trigger-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-manual-trigger-audit/scripts/manual-trigger-audit.sh
```

Run against bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-manual-trigger-audit/fixtures/*.json' \
bash skills/github-actions-manual-trigger-audit/scripts/manual-trigger-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked workflow groups
- JSON mode prints summary + ranked groups + critical groups
