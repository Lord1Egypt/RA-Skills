---
name: github-actions-failure-owner-audit
description: Audit failing GitHub Actions runs by actor ownership to expose who/workflow combinations generate the most CI noise and wasted minutes.
version: 1.1.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Failure Owner Audit

Use this skill to attribute GitHub Actions failures to owners (actors) so teams can route CI stabilization work by impact instead of guesswork.

## What this skill does
- Reads one or more GitHub Actions run JSON exports (`gh api` output or per-run JSON files)
- Focuses on failure-like conclusions by default (`failure`, `cancelled`, `timed_out`, `action_required`, `startup_failure`)
- Groups by repository + actor (or repository + actor + workflow)
- Scores hotspots by failed run counts and total failed runtime minutes
- Supports text and JSON output for triage meetings and automation

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions-runs/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `GROUP_BY` (`actor`, `actor-workflow`, `owner`, or `owner-workflow`, default: `actor`)
- `OWNER_MAP_FILE` (optional JSON mapping file to map actor regex → owner/team)
- `WARN_FAILURE_RUNS` (default: `3`)
- `CRITICAL_FAILURE_RUNS` (default: `6`)
- `WARN_FAILURE_MINUTES` (default: `30`)
- `CRITICAL_FAILURE_MINUTES` (default: `90`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `REPO_MATCH` / `REPO_EXCLUDE` (regex, optional)
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` / `BRANCH_EXCLUDE` (regex, optional)
- `ACTOR_MATCH` / `ACTOR_EXCLUDE` (regex, optional)
- `CONCLUSION_MATCH` / `CONCLUSION_EXCLUDE` (regex, optional)

## Collect run JSON

Single repository paginated export:

```bash
gh api repos/<owner>/<repo>/actions/runs --paginate \
  > artifacts/github-actions-runs/<owner>-<repo>.json
```

## Run

Default ownership triage:

```bash
RUN_GLOB='artifacts/github-actions-runs/*.json' \
bash skills/github-actions-failure-owner-audit/scripts/failure-owner-audit.sh
```

Workflow-scoped ownership triage with stricter thresholds:

```bash
RUN_GLOB='artifacts/github-actions-runs/*.json' \
GROUP_BY='actor-workflow' \
WARN_FAILURE_RUNS=2 \
CRITICAL_FAILURE_RUNS=4 \
WARN_FAILURE_MINUTES=20 \
CRITICAL_FAILURE_MINUTES=60 \
bash skills/github-actions-failure-owner-audit/scripts/failure-owner-audit.sh
```

JSON output for dashboards/alerts:

```bash
RUN_GLOB='artifacts/github-actions-runs/*.json' \
OUTPUT_FORMAT='json' \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-failure-owner-audit/scripts/failure-owner-audit.sh
```

Filter to a repo and release branches only:

```bash
RUN_GLOB='artifacts/github-actions-runs/*.json' \
REPO_MATCH='^flowcreatebot/' \
BRANCH_MATCH='^(main|release/)' \
ACTOR_EXCLUDE='(dependabot|renovate)' \
bash skills/github-actions-failure-owner-audit/scripts/failure-owner-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-failure-owner-audit/fixtures/*.json' \
bash skills/github-actions-failure-owner-audit/scripts/failure-owner-audit.sh
```

Owner/team mapping (first matching regex wins):

```json
{
  "^dependabot\\[bot]$": "automation",
  "^renovate\\[bot]$": "automation",
  "^alice$": "platform"
}
```

```bash
RUN_GLOB='artifacts/github-actions-runs/*.json' \
GROUP_BY='owner-workflow' \
OWNER_MAP_FILE='skills/github-actions-failure-owner-audit/examples/owner-map.sample.json' \
bash skills/github-actions-failure-owner-audit/scripts/failure-owner-audit.sh
```

## Output contract
- Exit `0` in reporting mode (default)
- Exit `1` if `FAIL_ON_CRITICAL=1` and at least one ownership group is critical
- In `text` mode: prints summary and top ownership hotspots
- In `json` mode: prints summary, top groups, all groups, and critical groups
