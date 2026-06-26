---
name: github-actions-step-flake-audit
description: Detect flaky GitHub Actions job steps by finding mixed success/failure conclusions across runs.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Step Flake Audit

Use this skill to catch flaky CI steps that alternate between passing and failing across workflow runs.

## What this skill does
- Reads GitHub Actions run JSON exports (`gh run view --json ...`)
- Groups step outcomes by repository + workflow + job + step name
- Scores each step for flake risk when both success and failure outcomes are present
- Ranks the most unstable steps by failure rate and failed-run volume
- Supports text/json outputs and optional fail gate for CI enforcement

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_OCCURRENCES` (default: `3`) — minimum observed step runs before scoring
- `WARN_FAILURE_RATE` (default: `0.20`) — flaky failure-rate threshold
- `CRITICAL_FAILURE_RATE` (default: `0.40`) — critical flaky failure-rate threshold
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `REPO_MATCH` / `REPO_EXCLUDE` (regex, optional)
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` (regex, optional)
- `JOB_MATCH` / `JOB_EXCLUDE` (regex, optional)
- `STEP_MATCH` / `STEP_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,headSha,url,repository,jobs \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
MIN_OCCURRENCES=5 \
WARN_FAILURE_RATE=0.15 \
CRITICAL_FAILURE_RATE=0.35 \
bash skills/github-actions-step-flake-audit/scripts/step-flake-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-step-flake-audit/scripts/step-flake-audit.sh
```

Run against bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-step-flake-audit/fixtures/*.json' \
bash skills/github-actions-step-flake-audit/scripts/step-flake-audit.sh
```

## Output contract
- Exit `0` in reporting mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more flaky step groups are critical
- Text mode prints summary + top flaky steps
- JSON mode prints summary + ranked groups + critical groups
