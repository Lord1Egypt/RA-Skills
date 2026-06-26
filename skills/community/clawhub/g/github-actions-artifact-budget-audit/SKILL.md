---
name: github-actions-artifact-budget-audit
description: Audit GitHub Actions artifact storage usage from JSON exports so bloated artifacts are flagged before they inflate CI cost.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Artifact Budget Audit

Use this skill to detect oversized or stale GitHub Actions artifacts across repositories.

## What this skill does
- Reads one or more GitHub artifact JSON exports (`gh api` output)
- Calculates artifact size in MB and totals by repository + artifact name
- Flags warn/critical artifacts by configurable size thresholds
- Highlights soon-to-expire artifact volume to prioritize cleanup
- Supports text and JSON output for terminal or dashboards

## Inputs
Optional:
- `ARTIFACT_GLOB` (default: `artifacts/github-actions-artifacts/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `WARN_MB` (default: `250`)
- `CRITICAL_MB` (default: `750`)
- `SOON_EXPIRES_DAYS` (default: `7`)
- `FAIL_ON_CRITICAL` (`0` or `1`, default: `0`)
- `REPO_MATCH` (regex, optional)
- `REPO_EXCLUDE` (regex, optional)
- `ARTIFACT_MATCH` (regex, optional)
- `ARTIFACT_EXCLUDE` (regex, optional)

## Collect artifact JSON

Single repository:

```bash
gh api repos/<owner>/<repo>/actions/artifacts --paginate \
  > artifacts/github-actions-artifacts/<owner>-<repo>.json
```

Combined multi-repo payloads are also supported as long as each file includes an `artifacts` array.

## Run

Text report:

```bash
ARTIFACT_GLOB='artifacts/github-actions-artifacts/*.json' \
WARN_MB=300 \
CRITICAL_MB=900 \
bash skills/github-actions-artifact-budget-audit/scripts/artifact-budget-audit.sh
```

JSON output for automation:

```bash
ARTIFACT_GLOB='artifacts/github-actions-artifacts/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-artifact-budget-audit/scripts/artifact-budget-audit.sh
```

Filter to one repo and artifact family:

```bash
ARTIFACT_GLOB='artifacts/github-actions-artifacts/*.json' \
REPO_MATCH='^flowcreatebot/' \
ARTIFACT_MATCH='(test-results|coverage)' \
bash skills/github-actions-artifact-budget-audit/scripts/artifact-budget-audit.sh
```

Run with bundled fixtures:

```bash
ARTIFACT_GLOB='skills/github-actions-artifact-budget-audit/fixtures/*.json' \
bash skills/github-actions-artifact-budget-audit/scripts/artifact-budget-audit.sh
```

## Output contract
- Exit `0` in reporting mode (default)
- Exit `1` if `FAIL_ON_CRITICAL=1` and at least one artifact is at/above `CRITICAL_MB`
- In `text` mode: prints summary and top oversized artifact groups
- In `json` mode: prints summary, grouped artifact stats, and critical artifact instances
