---
name: github-actions-sha-rerun-debt-audit
description: Audit rerun debt by commit SHA to find commits that repeatedly burn CI minutes across workflows.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions SHA Rerun Debt Audit

Use this skill to detect commits that trigger repeated GitHub Actions reruns and failed outcomes across multiple workflows.

## What this skill does
- Reads GitHub Actions run JSON exports
- Correlates attempt history by run id and latest outcome per run
- Aggregates rerun debt by repository + commit SHA
- Scores risk using rerun rate, failed-run count, workflow spread, and wasted rerun minutes
- Emits severity (`ok`, `warn`, `critical`) for CI gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS` (minimum runs per SHA, default: `3`)
- `WARN_RERUN_RATE` (0..1, default: `0.25`)
- `CRITICAL_RERUN_RATE` (0..1, default: `0.45`)
- `WARN_FAILED_RUNS` (default: `2`)
- `CRITICAL_FAILED_RUNS` (default: `4`)
- `WARN_WASTED_MINUTES` (default: `25`)
- `CRITICAL_WASTED_MINUTES` (default: `75`)
- `WARN_WORKFLOWS` (distinct workflows affected, default: `2`)
- `CRITICAL_WORKFLOWS` (default: `4`)
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` / `BRANCH_EXCLUDE` (regex, optional)
- `EVENT_MATCH` / `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` / `REPO_EXCLUDE` (regex, optional)
- `HEAD_SHA_MATCH` / `HEAD_SHA_EXCLUDE` (regex, optional)
- `FAILURE_CONCLUSIONS` (comma-separated, default: `failure,cancelled,timed_out,startup_failure,action_required`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Collect run JSON

```bash
gh run view <run-id> --attempt <attempt> \
  --json databaseId,runAttempt,workflowName,event,headBranch,headSha,conclusion,createdAt,updatedAt,runStartedAt,url,repository \
  > artifacts/github-actions/run-<run-id>-attempt-<attempt>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
bash skills/github-actions-sha-rerun-debt-audit/scripts/sha-rerun-debt-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-sha-rerun-debt-audit/scripts/sha-rerun-debt-audit.sh
```

Run against bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-sha-rerun-debt-audit/fixtures/*.json' \
bash skills/github-actions-sha-rerun-debt-audit/scripts/sha-rerun-debt-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more SHA groups are critical
- Text mode prints summary + ranked SHA risk groups
- JSON mode prints summary + ranked groups + critical groups
