---
name: github-actions-commit-health-audit
description: Audit GitHub Actions reliability by commit SHA to surface risky commits causing repeated workflow failures across branches.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Commit Health Audit

Use this skill to find commits that repeatedly fail CI so teams can prioritize rollback, revert, or targeted fixes.

## What this skill does
- Reads GitHub Actions run JSON exports
- Groups runs by repository + commit SHA
- Scores commit risk using failure rate, failed-run volume, and workflow spread
- Flags warning/critical commit hotspots
- Emits text or JSON output for CI checks and triage dashboards

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `MIN_RUNS` (default: `2`)
- `BRANCH_MATCH` (regex, optional)
- `BRANCH_EXCLUDE` (regex, optional)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `SHA_MATCH` (regex, optional)
- `SHA_EXCLUDE` (regex, optional)
- `FAIL_WARN_PERCENT` (default: `25`)
- `FAIL_CRITICAL_PERCENT` (default: `50`)
- `WARN_SCORE` (default: `35`)
- `CRITICAL_SCORE` (default: `60`)
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
MIN_RUNS=3 \
bash skills/github-actions-commit-health-audit/scripts/commit-health-audit.sh
```

JSON output with fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-commit-health-audit/scripts/commit-health-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-commit-health-audit/fixtures/*.json' \
bash skills/github-actions-commit-health-audit/scripts/commit-health-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more commits are critical
- Text mode prints summary + ranked commit-risk groups
- JSON mode prints summary + scored groups + critical commit details
