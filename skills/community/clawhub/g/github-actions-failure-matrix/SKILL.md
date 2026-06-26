---
name: github-actions-failure-matrix
description: Summarize GitHub Actions matrix job failures across runs so you can spot unstable OS/runtime axes fast.
version: 1.7.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# GitHub Actions Failure Matrix

Use this skill to turn noisy GitHub Actions run JSON into a matrix-focused failure report.

## What this skill does
- Reads one or more JSON exports from GitHub Actions runs (via `gh run view --json`)
- Detects failure-like matrix jobs (`failure`, `timed_out`, `cancelled`, etc.)
- Extracts matrix axes from common job-name patterns (`name (a, b)`, `name [a, b]`, `name / a / b`)
- Groups repeated failures by workflow + job + matrix axis signature
- Emits ranked triage output in `text` or `json`

## Inputs
Optional:
- `RUN_GLOB` (default: `artifacts/github-actions/*.json`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `FAIL_ON_FAILURES` (`0` or `1`, default: `0`) — exit non-zero when failure groups exist
- `MIN_OCCURRENCES` (default: `1`) — hide groups below this repeat count
- `WORKFLOW_MATCH` (regex, optional) — include only workflows whose names match
- `WORKFLOW_EXCLUDE` (regex, optional) — drop workflows whose names match
- `BRANCH_MATCH` (regex, optional) — include only runs whose branch names match
- `BRANCH_EXCLUDE` (regex, optional) — drop runs whose branch names match
- `JOB_MATCH` (regex, optional) — include only base job names that match
- `JOB_EXCLUDE` (regex, optional) — drop base job names that match
- `AXIS_MATCH` (regex, optional) — include only parsed matrix-axis strings that match
- `AXIS_EXCLUDE` (regex, optional) — drop parsed matrix-axis strings that match
- `CONCLUSION_MATCH` (regex, optional) — include only specific failure conclusions (`failure`, `timed_out`, `cancelled`, etc.)
- `CONCLUSION_EXCLUDE` (regex, optional) — drop specific failure conclusions
- `FAILED_STEP_MATCH` (regex, optional) — include only jobs whose terminal failed step matches
- `FAILED_STEP_EXCLUDE` (regex, optional) — drop jobs whose terminal failed step matches
- `RUN_ID_MATCH` (regex, optional) — include only runs whose run id matches
- `RUN_ID_EXCLUDE` (regex, optional) — drop runs whose run id matches
- `RUN_URL_MATCH` (regex, optional) — include only runs whose URL matches
- `RUN_URL_EXCLUDE` (regex, optional) — drop runs whose URL matches
- `HEAD_SHA_MATCH` (regex, optional) — include only runs whose `headSha` matches
- `HEAD_SHA_EXCLUDE` (regex, optional) — drop runs whose `headSha` matches
- `REPO_MATCH` (regex, optional) — include only runs whose repository matches (`repository.nameWithOwner`/`full_name`/`name`)
- `REPO_EXCLUDE` (regex, optional) — drop runs whose repository matches

## Collect run JSON

```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,headSha,url,repository,jobs \
  > artifacts/github-actions/run-<run-id>.json
```

## Run

Text report:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
TOP_N=15 \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

JSON output for CI annotation/upload:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_FAILURES=1 \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

Filter to a specific workflow + branch + matrix axis (for targeted triage):

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WORKFLOW_MATCH='(CI|Test)' \
BRANCH_MATCH='^(main|release/)' \
AXIS_MATCH='ubuntu-latest \| python-3\.12' \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

Isolate timeout-only matrix failures:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
CONCLUSION_MATCH='^timed_out$' \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

Exclude noisy flaky suites while keeping the rest of the matrix view:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WORKFLOW_EXCLUDE='nightly|experimental' \
JOB_EXCLUDE='lint|docs' \
AXIS_EXCLUDE='windows-latest' \
CONCLUSION_EXCLUDE='^cancelled$' \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

Focus only on setup/toolchain breakages by failed step name:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
FAILED_STEP_MATCH='setup|install|dependency' \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

Limit triage to a specific run range or workflow URL pattern:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
RUN_ID_MATCH='^(28419|28420)' \
RUN_URL_MATCH='example/repo/actions/runs' \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

Scope triage to a commit range by `headSha`:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
HEAD_SHA_MATCH='^(abc123|def456)' \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

Scope triage to specific repositories when aggregating exports from multiple repos:

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
REPO_MATCH='^flowcreatebot/(yf-api-saas|conspiracy-canvas)$' \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

Run with bundled fixtures:

```bash
RUN_GLOB='skills/github-actions-failure-matrix/fixtures/*.json' \
bash skills/github-actions-failure-matrix/scripts/failure-matrix.sh
```

## Output contract
- Exit `0` by default (reporting mode)
- Exit `1` if `FAIL_ON_FAILURES=1` and at least one failure group is found
- In `text` mode, prints summary + top failure matrix groups
- In `json` mode, prints machine-readable summary and grouped failures
