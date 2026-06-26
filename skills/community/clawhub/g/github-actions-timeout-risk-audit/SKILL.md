---
name: github-actions-timeout-risk-audit
description: Audit GitHub Actions job runtime risk against timeout thresholds so near-timeout jobs get fixed before they fail CI.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Timeout Risk Audit

Use this skill to find GitHub Actions jobs that are timing out or trending dangerously close to timeout limits.

## What this skill does
- Reads one or more run JSON exports (`gh run view --json ...`)
- Calculates per-job runtime (`completedAt - startedAt`)
- Flags risk severity by configured timeout threshold:
  - `warn` when runtime exceeds `WARN_RATIO * JOB_TIMEOUT_SECONDS`
  - `critical` when runtime exceeds `CRITICAL_RATIO * JOB_TIMEOUT_SECONDS`
  - always `critical` for jobs with `conclusion=timed_out`
- Groups repeated jobs by repository + workflow + job name
- Emits text or JSON output for CI gates / dashboards

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `JOB_TIMEOUT_SECONDS` (default: `3600`)
- `WARN_RATIO` (default: `0.80`)
- `CRITICAL_RATIO` (default: `0.95`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `WORKFLOW_MATCH`, `WORKFLOW_EXCLUDE` (regex, optional)
- `JOB_MATCH`, `JOB_EXCLUDE` (regex, optional)
- `REPO_MATCH`, `REPO_EXCLUDE` (regex, optional)
- `BRANCH_MATCH`, `BRANCH_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,url,repository,jobs \
  > artifacts/github-actions/run-<run-id>.json
```

> Ensure `jobs` includes `startedAt`, `completedAt`, and `conclusion`.

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
JOB_TIMEOUT_SECONDS=3600 \
WARN_RATIO=0.85 \
CRITICAL_RATIO=0.95 \
bash skills/github-actions-timeout-risk-audit/scripts/timeout-risk-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-timeout-risk-audit/scripts/timeout-risk-audit.sh
```

Repo/workflow filter:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
REPO_MATCH='^flowcreatebot/' \
WORKFLOW_MATCH='(CI|Build)' \
bash skills/github-actions-timeout-risk-audit/scripts/timeout-risk-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-timeout-risk-audit/fixtures/*.json' \
bash skills/github-actions-timeout-risk-audit/scripts/timeout-risk-audit.sh
```

## Output contract
- Exit `0` in reporting mode
- Exit `1` when `FAIL_ON_CRITICAL=1` and at least one critical instance exists
- Text output includes summary, thresholds, and top timeout-risk jobs
- JSON output includes `summary`, ranked `groups`, and `critical_instances`
