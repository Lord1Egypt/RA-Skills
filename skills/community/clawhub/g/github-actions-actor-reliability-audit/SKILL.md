---
name: github-actions-actor-reliability-audit
description: Audit GitHub Actions run reliability by actor to surface high-risk contributors and flaky automation owners.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Actor Reliability Audit

Use this skill to rank which actors (humans or bots) are associated with the least reliable GitHub Actions outcomes.

## What this skill does
- Reads GitHub Actions run JSON exports
- Groups runs by actor (optionally actor + workflow)
- Measures failure rate, failed-run volume, and latest failure streak per actor
- Scores severity (`ok`, `warn`, `critical`) for triage and CI policy gates
- Emits text or JSON output for automation

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `GROUP_BY` (`actor` or `actor-workflow`, default: `actor`)
- `FAILURE_CONCLUSIONS` (comma-separated, default: `failure,cancelled,timed_out,startup_failure`)
- `MIN_RUNS` (minimum runs required, default: `5`)
- `WARN_FAILURE_RATE` (0..1, default: `0.25`)
- `CRITICAL_FAILURE_RATE` (0..1, default: `0.5`)
- `WARN_FAILED_RUNS` (default: `4`)
- `CRITICAL_FAILED_RUNS` (default: `8`)
- `WARN_FAILURE_STREAK` (default: `2`)
- `CRITICAL_FAILURE_STREAK` (default: `4`)
- `ACTOR_MATCH` / `ACTOR_EXCLUDE` (regex, optional)
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` / `BRANCH_EXCLUDE` (regex, optional)
- `EVENT_MATCH` / `EVENT_EXCLUDE` (regex, optional)
- `REPO_MATCH` / `REPO_EXCLUDE` (regex, optional)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,event,headBranch,conclusion,createdAt,updatedAt,url,repository,actor,triggeringActor \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
bash skills/github-actions-actor-reliability-audit/scripts/actor-reliability-audit.sh
```

JSON output + fail gate:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-actor-reliability-audit/scripts/actor-reliability-audit.sh
```

Run against bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-actor-reliability-audit/fixtures/*.json' \
bash skills/github-actions-actor-reliability-audit/scripts/actor-reliability-audit.sh
```

## Output contract
- Exit `0` in report mode (default)
- Exit `1` when `FAIL_ON_CRITICAL=1` and one or more actor groups are critical
- Text mode prints summary + ranked actor groups
- JSON mode prints summary + ranked groups + critical groups
