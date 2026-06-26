---
name: github-actions-run-gap-audit
description: Detect GitHub Actions workflow groups that stopped running on their normal cadence using median run intervals and current inactivity gap.
version: 1.1.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Run Gap Audit

Use this skill to detect workflow groups that have gone unexpectedly quiet (stale triggers, broken schedules, disabled automation, branch drift).

## What this skill does
- Reads GitHub Actions run JSON exports
- Groups by repository + workflow + branch + event
- Computes historical cadence (median and p90 interval hours)
- Compares latest inactivity gap vs historical cadence
- Scores risk severity (`ok`, `warn`, `critical`)
- Emits text or JSON for CI checks and automation guardrails

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS` (default: `4`)
- `WARN_GAP_MULTIPLIER` (default: `2.0`)
- `CRITICAL_GAP_MULTIPLIER` (default: `3.5`)
- `MIN_WARN_GAP_HOURS` (default: `12`)
- `MIN_CRITICAL_GAP_HOURS` (default: `24`)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` (regex, optional)
- `BRANCH_EXCLUDE` (regex, optional)
- `EVENT_MATCH` (regex, optional)
- `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `RUN_ID_MATCH` (regex, optional)
- `RUN_ID_EXCLUDE` (regex, optional)
- `RUN_URL_MATCH` (regex, optional)
- `RUN_URL_EXCLUDE` (regex, optional)
- `NOW_ISO` (optional fixed evaluation time for deterministic CI tests)
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
MIN_RUNS=5 \
WARN_GAP_MULTIPLIER=2.25 \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

JSON output with fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

Targeted run-scope triage:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
RUN_ID_MATCH='^(88|89)' \
RUN_URL_EXCLUDE='rerun' \
OUTPUT_FORMAT=json \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-run-gap-audit/fixtures/*.json' \
NOW_ISO='2026-03-07T00:00:00Z' \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked stale workflow groups
- JSON mode prints summary + ranked groups + critical group details
