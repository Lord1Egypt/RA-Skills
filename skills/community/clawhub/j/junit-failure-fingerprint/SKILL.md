---
name: junit-failure-fingerprint
description: Cluster JUnit failures into stable fingerprints so CI triage focuses on root causes, not noisy one-off logs.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# JUnit Failure Fingerprint

Use this skill to compress noisy JUnit failures/errors into repeatable fingerprints.

## What this skill does
- Scans one or more JUnit XML files
- Extracts only failing/error test cases
- Normalizes volatile tokens (IDs, numbers, line numbers, addresses, UUIDs)
- Generates stable fingerprint hashes for similar root-cause failures
- Emits grouped triage output (`text` or `json`)

## Inputs
Optional:
- `JUNIT_GLOB` (default: `test-results/**/*.xml`)
- `TOP_N` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `STACK_LINES` (default: `3`) — number of normalized stack lines to include in fingerprint seed
- `FAIL_ON_FAILURES` (`0` or `1`, default: `0`) — exit non-zero when any failures/errors are found

## Run

Text report:

```bash
JUNIT_GLOB='artifacts/junit/**/*.xml' \
TOP_N=15 \
bash skills/junit-failure-fingerprint/scripts/fingerprint-junit.sh
```

JSON output for CI annotation/upload:

```bash
JUNIT_GLOB='artifacts/junit/**/*.xml' \
OUTPUT_FORMAT=json \
FAIL_ON_FAILURES=1 \
bash skills/junit-failure-fingerprint/scripts/fingerprint-junit.sh
```

Run with bundled fixtures:

```bash
JUNIT_GLOB='skills/junit-failure-fingerprint/fixtures/*.xml' \
bash skills/junit-failure-fingerprint/scripts/fingerprint-junit.sh
```

## Output contract
- Exit `0` by default (reporting mode)
- Exit `1` if `FAIL_ON_FAILURES=1` and at least one failure/error is found
- In `text` mode, prints summary + top fingerprints
- In `json` mode, prints machine-readable groups and per-case detail
