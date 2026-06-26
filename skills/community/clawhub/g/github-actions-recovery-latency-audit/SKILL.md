---
name: github-actions-recovery-latency-audit
description: Measure GitHub Actions failure recovery latency and unresolved incident age by workflow group.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Recovery Latency Audit

Use this skill to measure how quickly workflows recover after failing, and to detect groups that remain red for too long.

## What this skill does
- Reads GitHub Actions run JSON exports
- Groups by repository + workflow + branch + event
- Builds failure incidents (first failing run until next success)
- Reports recovery latency for closed incidents
- Reports unresolved incident count + oldest unresolved age
- Scores severity (`ok`, `warn`, `critical`) for triage and CI gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS` (default: `4`)
- `WARN_P95_HOURS` (default: `6`)
- `CRITICAL_P95_HOURS` (default: `18`)
- `WARN_OPEN_HOURS` (default: `12`)
- `CRITICAL_OPEN_HOURS` (default: `36`)
- `WARN_OPEN_INCIDENTS` (default: `1`)
- `CRITICAL_OPEN_INCIDENTS` (default: `2`)
- `NOW_ISO` (optional fixed clock for deterministic tests)
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` (regex)
- `BRANCH_MATCH` / `BRANCH_EXCLUDE` (regex)
- `EVENT_MATCH` / `EVENT_EXCLUDE` (regex)
- `REPO_MATCH` / `REPO_EXCLUDE` (regex)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,createdAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
TOP_N=15 \
bash skills/github-actions-recovery-latency-audit/scripts/recovery-latency-audit.sh
```

JSON + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-recovery-latency-audit/scripts/recovery-latency-audit.sh
```

Run against bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-recovery-latency-audit/fixtures/*.json' \
NOW_ISO='2026-03-07T14:00:00Z' \
bash skills/github-actions-recovery-latency-audit/scripts/recovery-latency-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked recovery-risk groups
- JSON mode prints summary + ranked groups + critical groups
