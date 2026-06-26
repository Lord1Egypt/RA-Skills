# Kimi Troubleshooting Guide

## 401 Unauthorized

Symptoms:
- `/models` fails immediately
- Kimi requests return `401`

Checks:
1. Confirm `MOONSHOT_API_KEY` is set in the current shell.
2. Remove stray quotes or whitespace from the env var.
3. Re-run the `/models` health check before changing anything else.

## 404 or Model Not Found

Symptoms:
- request reaches the API but the model is rejected

Checks:
1. Fetch `/models` and copy the exact live model ID.
2. Remove stale defaults from scripts and notes.
3. Re-test with a minimal prompt before changing parsers.

## 429 Rate Limited

Symptoms:
- bursts of `429` during batch or parallel runs

Checks:
1. Add exponential backoff with jitter.
2. Lower concurrency and shrink prompt size.
3. Route overflow to a smaller or fallback model if approved.

## Timeout or 5xx

Symptoms:
- intermittent server errors
- long-tail latency on large prompts

Checks:
1. Retry capped attempts before failing hard.
2. Split the task into smaller chunks or summaries.
3. Save a sanitized repro payload only if the workflow is recurring.

## JSON Parse Failures

Symptoms:
- output mixes prose with machine-readable fields

Checks:
1. Force strict output contract in the system message.
2. Use low temperature for the normalization pass.
3. Validate output before downstream writes or automation.

## Hidden Cost Drift

Symptoms:
- batch usage becomes much more expensive than expected

Checks:
1. Cap retries and total batch size.
2. Switch to metadata-first or smaller-route triage.
3. Compare the saved primary route against the actual workload now running.
