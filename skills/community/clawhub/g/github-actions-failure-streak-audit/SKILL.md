---
name: github-actions-failure-streak-audit
description: Detect consecutive GitHub Actions failure streaks by repo/workflow/branch to prioritize unstable pipelines.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Failure Streak Audit

Use this skill to find repeated CI failures before they become delivery bottlenecks.

## What this skill does
- Reads GitHub Actions run JSON exports (`gh run view --json ...`)
- Groups runs by repo + workflow + branch
- Detects consecutive failure streaks (`failure`, `cancelled`, `timed_out`)
- Scores severity by streak length and impacted runtime minutes
- Surfaces longest unresolved streaks first

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_STREAK` (default: `2`)
- `CRITICAL_STREAK` (default: `4`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `WORKFLOW_MATCH`, `WORKFLOW_EXCLUDE` (regex, optional)
- `REPO_MATCH`, `REPO_EXCLUDE` (regex, optional)
- `BRANCH_MATCH`, `BRANCH_EXCLUDE` (regex, optional)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,headSha,createdAt,updatedAt,conclusion,url,repository,jobs \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WARN_STREAK=2 \
CRITICAL_STREAK=4 \
bash skills/github-actions-failure-streak-audit/scripts/failure-streak-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-failure-streak-audit/scripts/failure-streak-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-failure-streak-audit/fixtures/*.json' \
bash skills/github-actions-failure-streak-audit/scripts/failure-streak-audit.sh
```

## Output contract
- Exit `0` in reporting mode
- Exit `1` when `FAIL_ON_CRITICAL=1` and critical streaks exist
- Text output includes grouped streak totals and ranked hotspots
- JSON output includes `summary`, `streaks`, and `critical_streaks`
