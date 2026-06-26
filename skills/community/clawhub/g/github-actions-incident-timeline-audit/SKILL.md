---
name: github-actions-incident-timeline-audit
description: Cluster failed GitHub Actions runs into incident windows by repo to expose outage duration, impact scope, and escalation severity.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Incident Timeline Audit

Use this skill to convert noisy failed run exports into incident windows you can triage quickly during CI reliability reviews.

## What this skill does
- Reads GitHub Actions run JSON exports
- Keeps only failed/cancelled/timed-out style outcomes
- Groups failures by repository into incident windows using a configurable gap threshold
- Scores each incident using failed-run and duration thresholds
- Emits text or JSON output for review docs, ops dashboards, and CI fail gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `INCIDENT_GAP_MINUTES` (default: `45`)
- `WARN_FAILED_RUNS` (default: `2`)
- `CRITICAL_FAILED_RUNS` (default: `4`)
- `WARN_DURATION_MINUTES` (default: `20`)
- `CRITICAL_DURATION_MINUTES` (default: `60`)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,createdAt,updatedAt,startedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
INCIDENT_GAP_MINUTES=45 \
bash skills/github-actions-incident-timeline-audit/scripts/incident-timeline-audit.sh
```

JSON output with fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-incident-timeline-audit/scripts/incident-timeline-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-incident-timeline-audit/fixtures/*.json' \
bash skills/github-actions-incident-timeline-audit/scripts/incident-timeline-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more incidents are critical
- Text mode prints summary + ranked incident windows
- JSON mode prints summary + incidents + critical incident details
