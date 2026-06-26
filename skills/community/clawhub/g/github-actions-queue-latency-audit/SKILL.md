---
name: github-actions-queue-latency-audit
description: Audit GitHub Actions queue wait hotspots from run/job JSON so CI bottlenecks are visible before they stall merges.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Queue Latency Audit

Use this skill to quantify where workflows are waiting in queue before jobs start.

## What this skill does
- Reads one or more GitHub Actions run JSON exports (from `gh run view --json ...`)
- Computes per-job queue wait (`startedAt - createdAt`) and runtime duration (`completedAt - startedAt`)
- Groups repeated jobs by repository + workflow + job name
- Ranks hotspots by worst queue wait and average queue wait
- Flags warning/critical queue waits with configurable thresholds
- Emits output as human-readable text or machine-readable JSON

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `QUEUE_WARN_SECONDS` (default: `120`)
- `QUEUE_CRITICAL_SECONDS` (default: `300`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`) — exit non-zero when any job instance hits/exceeds critical queue wait
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `JOB_MATCH` (regex, optional)
- `JOB_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,headSha,url,repository,jobs \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
TOP_N=15 \
QUEUE_WARN_SECONDS=180 \
QUEUE_CRITICAL_SECONDS=420 \
bash skills/github-actions-queue-latency-audit/scripts/queue-latency-audit.sh
```

JSON output for dashboards:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-queue-latency-audit/scripts/queue-latency-audit.sh
```

Filter to one repo/workflow family:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
REPO_MATCH='^flowcreatebot/' \
WORKFLOW_MATCH='(CI|Build|Test)' \
bash skills/github-actions-queue-latency-audit/scripts/queue-latency-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-queue-latency-audit/fixtures/*.json' \
bash skills/github-actions-queue-latency-audit/scripts/queue-latency-audit.sh
```

## Output contract
- Exit `0` in reporting mode (default)
- Exit `1` if `FAIL_ON_CRITICAL=1` and at least one job instance has queue wait `>= QUEUE_CRITICAL_SECONDS`
- In `text` mode: prints summary + top queue hotspots
- In `json` mode: prints summary + grouped hotspot records + raw offending instances
