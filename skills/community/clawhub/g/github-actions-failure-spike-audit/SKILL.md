---
name: github-actions-failure-spike-audit
description: Detect sudden GitHub Actions failure-rate spikes by workflow group using recent-vs-baseline run windows.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Failure Spike Audit

Use this skill to catch workflows that recently degraded (new flaky tests, broken deploy gates, bad dependency updates, or infra outages) before they become long-running incidents.

## What this skill does
- Reads GitHub Actions run JSON exports
- Groups by repository + workflow + branch + event
- Splits each group into **recent** runs and **baseline** history
- Compares recent failure rate to baseline failure rate
- Scores severity (`ok`, `warn`, `critical`) using spike + recent failure rate gates
- Emits text or JSON output for CI automation

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `RECENT_RUNS` (default: `4`)
- `MIN_RECENT_RUNS` (default: `3`)
- `MIN_BASELINE_RUNS` (default: `4`)
- `WARN_SPIKE_PCT` (default: `15`)
- `CRITICAL_SPIKE_PCT` (default: `30`)
- `WARN_RECENT_FAILURE_RATE` (default: `25`)
- `CRITICAL_RECENT_FAILURE_RATE` (default: `45`)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` (regex, optional)
- `BRANCH_EXCLUDE` (regex, optional)
- `EVENT_MATCH` (regex, optional)
- `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
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
RECENT_RUNS=8 \
WARN_SPIKE_PCT=12 \
bash skills/github-actions-failure-spike-audit/scripts/failure-spike-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-failure-spike-audit/scripts/failure-spike-audit.sh
```

Run against bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-failure-spike-audit/fixtures/*.json' \
bash skills/github-actions-failure-spike-audit/scripts/failure-spike-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked failure-rate spike groups
- JSON mode prints summary + ranked groups + critical groups
