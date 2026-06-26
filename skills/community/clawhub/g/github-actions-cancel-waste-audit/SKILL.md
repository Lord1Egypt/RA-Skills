---
name: github-actions-cancel-waste-audit
description: Audit cancelled and timed-out GitHub Actions runs from JSON exports to surface wasted CI minutes and noisy workflows.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Cancel Waste Audit

Use this skill to quantify wasted GitHub Actions runtime from cancelled or timed-out runs so flaky workflow churn gets fixed before it burns CI budget.

## What this skill does
- Reads one or more GitHub Actions run JSON exports (`gh api` output)
- Estimates wasted runtime minutes per run (`run_started_at`/`created_at` -> `updated_at`)
- Groups waste by repository + workflow + conclusion for fast triage
- Flags warn/critical waste levels using configurable minute thresholds
- Supports text and JSON output for terminal checks or dashboards

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions-runs/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_WASTED_MINUTES` (default: `15`)
- `CRITICAL_WASTED_MINUTES` (default: `45`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `WORKFLOW_MATCH` (regex, optional)
- `WORKFLOW_EXCLUDE` (regex, optional)
- `BRANCH_MATCH` (regex, optional)
- `BRANCH_EXCLUDE` (regex, optional)
- `ACTOR_MATCH` (regex, optional)
- `ACTOR_EXCLUDE` (regex, optional)
- `CONCLUSION_MATCH` (regex, optional, default behavior already includes only cancelled/timed_out)
- `CONCLUSION_EXCLUDE` (regex, optional)

## Collect run JSON

Single repository:

```bash
gh api repos/<owner>/<repo>/actions/runs --paginate \
  > artifacts/github-actions-runs/<owner>-<repo>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions-runs/*.json' \
WARN_WASTED_MINUTES=20 \
CRITICAL_WASTED_MINUTES=60 \
bash skills/github-actions-cancel-waste-audit/scripts/cancel-waste-audit.sh
```

JSON output for automation:

```bash
RUN_GLOB='artifacts/github-actions-runs/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-cancel-waste-audit/scripts/cancel-waste-audit.sh
```

Filter to one repo/workflow family:

```bash
RUN_GLOB='artifacts/github-actions-runs/*.json' \
REPO_MATCH='^flowcreatebot/' \
WORKFLOW_MATCH='(test|build)' \
BRANCH_MATCH='^(main|release)' \
bash skills/github-actions-cancel-waste-audit/scripts/cancel-waste-audit.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-cancel-waste-audit/fixtures/*.json' \
bash skills/github-actions-cancel-waste-audit/scripts/cancel-waste-audit.sh
```

## Output contract
- Exit `0` in reporting mode (default)
- Exit `1` if `FAIL_ON_CRITICAL=1` and at least one run has waste at/above `CRITICAL_WASTED_MINUTES`
- In `text` mode: prints summary and top waste hotspots
- In `json` mode: prints summary, grouped stats, and critical run instances
