---
name: github-actions-rerun-effectiveness-audit
description: Audit GitHub Actions rerun dependency and success-after-rerun effectiveness to highlight workflows wasting CI time.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Rerun Effectiveness Audit

Use this skill to measure how often workflows require reruns and whether reruns are actually recovering failures.

## What this skill does
- Reads GitHub Actions run JSON exports
- Tracks rerun episodes using workflow run id + attempt history
- Measures rerun rate, rerun success rate, and extra rerun attempts
- Estimates wasted rerun minutes from attempt durations
- Emits severity (`ok`, `warn`, `critical`) for CI policy gates

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `GROUP_BY` (`workflow` or `workflow-branch`, default: `workflow`)
- `FAILURE_CONCLUSIONS` (comma-separated, default: `failure,cancelled,timed_out,startup_failure,action_required`)
- `SUCCESS_CONCLUSIONS` (comma-separated, default: `success`)
- `MIN_RUNS` (minimum workflow runs required, default: `4`)
- `WARN_RERUN_RATE` (0..1, default: `0.2`)
- `CRITICAL_RERUN_RATE` (0..1, default: `0.35`)
- `WARN_RERUN_SUCCESS_RATE` (0..1, default: `0.5`)
- `CRITICAL_RERUN_SUCCESS_RATE` (0..1, default: `0.25`)
- `WARN_WASTED_MINUTES` (default: `20`)
- `CRITICAL_WASTED_MINUTES` (default: `60`)
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` / `BRANCH_EXCLUDE` (regex, optional)
- `EVENT_MATCH` / `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` / `REPO_EXCLUDE` (regex, optional)
- `ACTOR_MATCH` / `ACTOR_EXCLUDE` (regex, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Collect run JSON

```bash
gh run view <run-id> --attempt <attempt> \
  --json databaseId,runAttempt,workflowName,event,headBranch,headSha,conclusion,createdAt,updatedAt,runStartedAt,url,repository,actor,triggeringActor \
  > artifacts/github-actions/run-<run-id>-attempt-<attempt>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
bash skills/github-actions-rerun-effectiveness-audit/scripts/rerun-effectiveness-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-rerun-effectiveness-audit/scripts/rerun-effectiveness-audit.sh
```

Run against bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-rerun-effectiveness-audit/fixtures/*.json' \
bash skills/github-actions-rerun-effectiveness-audit/scripts/rerun-effectiveness-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more groups are critical
- Text mode prints summary + ranked workflow groups
- JSON mode prints summary + ranked groups + critical groups
