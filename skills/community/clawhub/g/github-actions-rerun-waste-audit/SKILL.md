---
name: github-actions-rerun-waste-audit
description: Quantify wasted GitHub Actions minutes caused by reruns so flaky workflows can be fixed with data.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Rerun Waste Audit

Use this skill to measure CI waste caused by reruns and repeated attempts in GitHub Actions.

## What this skill does
- Reads one or more run JSON exports (`gh run view --json ...`)
- Groups attempts by repository + workflow + branch + commit + job name
- Estimates rerun waste from all attempts except the latest attempt in each group
- Flags severity using waste-minute thresholds
- Emits text or JSON output for triage dashboards and CI quality reviews

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_MINUTES` (default: `10`)
- `CRITICAL_MINUTES` (default: `30`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `WORKFLOW_MATCH`, `WORKFLOW_EXCLUDE` (regex, optional)
- `JOB_MATCH`, `JOB_EXCLUDE` (regex, optional)
- `REPO_MATCH`, `REPO_EXCLUDE` (regex, optional)
- `BRANCH_MATCH`, `BRANCH_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,headSha,runAttempt,url,repository,jobs \
  > artifacts/github-actions/run-<run-id>.json
```

> If `runAttempt` is missing, this skill also checks `run_attempt` and job-level `attempt`.

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WARN_MINUTES=8 \
CRITICAL_MINUTES=20 \
bash skills/github-actions-rerun-waste-audit/scripts/rerun-waste-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-rerun-waste-audit/scripts/rerun-waste-audit.sh
```

Repo/workflow filter:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
REPO_MATCH='^flowcreatebot/' \
WORKFLOW_MATCH='(CI|Build)' \
bash skills/github-actions-rerun-waste-audit/scripts/rerun-waste-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-rerun-waste-audit/fixtures/*.json' \
bash skills/github-actions-rerun-waste-audit/scripts/rerun-waste-audit.sh
```

## Output contract
- Exit `0` in reporting mode
- Exit `1` when `FAIL_ON_CRITICAL=1` and at least one critical group exists
- Text output includes summary, thresholds, and top rerun-waste groups
- JSON output includes `summary`, ranked `groups`, and `critical_groups`
