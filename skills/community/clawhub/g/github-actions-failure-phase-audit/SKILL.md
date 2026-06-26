---
name: github-actions-failure-phase-audit
description: Group GitHub Actions failures by pipeline phase (setup/build/test/lint/deploy/security) with minute impact to prioritize fixes.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Failure Phase Audit

Use this skill to identify which CI/CD phase is burning the most minutes when jobs fail.

## What this skill does
- Reads one or more GitHub Actions run JSON exports (`gh run view --json ...`)
- Detects the first non-success step per failed/cancelled/timed-out job
- Maps failures to phases: `setup`, `build`, `test`, `lint`, `deploy`, `security`, `other`
- Aggregates failures by repo + workflow + phase + failed step
- Ranks hotspots by impacted minutes and failure count

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_MINUTES` (default: `20`)
- `CRITICAL_MINUTES` (default: `45`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `WORKFLOW_MATCH`, `WORKFLOW_EXCLUDE` (regex, optional)
- `REPO_MATCH`, `REPO_EXCLUDE` (regex, optional)
- `BRANCH_MATCH`, `BRANCH_EXCLUDE` (regex, optional)
- `PHASE_MATCH`, `PHASE_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,headSha,url,repository,jobs \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WARN_MINUTES=15 \
CRITICAL_MINUTES=35 \
bash skills/github-actions-failure-phase-audit/scripts/failure-phase-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-failure-phase-audit/scripts/failure-phase-audit.sh
```

Phase filtered report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
PHASE_MATCH='^(test|deploy)$' \
bash skills/github-actions-failure-phase-audit/scripts/failure-phase-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-failure-phase-audit/fixtures/*.json' \
bash skills/github-actions-failure-phase-audit/scripts/failure-phase-audit.sh
```

## Output contract
- Exit `0` in reporting mode
- Exit `1` when `FAIL_ON_CRITICAL=1` and critical hotspots exist
- Text output includes totals and ranked phase hotspots
- JSON output includes `summary`, `hotspots`, and `critical_hotspots`
