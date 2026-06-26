# Batch Worker — Implementation Spec

Implement this as: `batch-worker.py`

This document tells your AI exactly how to implement a batch job worker
for the Anthropic Batch API, compatible with the hyperthink pipeline.

---

## What It Does

A single script with three subcommands:

```
python3 batch-worker.py submit --job-file path/to/job.json
python3 batch-worker.py poll
python3 batch-worker.py status
```

- **submit** — sends a batch job to Anthropic, saves state locally
- **poll** — checks all pending jobs, saves results, notifies user when done
- **status** — prints a summary table of all known jobs

---

## Environment Requirements

- Python 3.8+
- No third-party packages — stdlib only (`urllib`, `json`, `pathlib`, `uuid`, `argparse`)
- An Anthropic API key — read from `ANTHROPIC_API_KEY` environment variable
- A writable directory for state files (configurable — see Storage below)

---

## Storage Layout

All state is stored in a local directory. Default: `./batch-jobs/`
Override via `BATCH_JOBS_DIR` environment variable or a constant in the script.

```
batch-jobs/
  registry.json          # Master list of all jobs (array)
  [job_id]/
    state.json           # Full state for this job
    results.jsonl        # Raw JSONL results from Anthropic (one object per line)
```

**job_id** — 8-char hex string, generated at submit time (`uuid4().hex[:8]`)

### state.json schema:
```json
{
  "job_id": "a1b2c3d4",
  "batch_id": "msgbatch_01...",
  "description": "Human-readable label",
  "model": "claude-sonnet-4-6",
  "status": "processing | complete | error",
  "submitted_at": "2026-01-01T00:00:00+00:00",
  "completed_at": "2026-01-01T02:00:00+00:00",
  "succeeded": 36,
  "errored": 0,
  "results_file": "./batch-jobs/a1b2c3d4/results.jsonl",
  "notified": false,
  "extracted": false
}
```

**`notified`** — true once the user has been informed of completion
**`extracted`** — true once output files have been written to disk by the caller (e.g. the pipeline poller)
These are separate flags. A job is fully done only when both are true.

### registry.json schema:
```json
{
  "jobs": [
    {
      "job_id": "a1b2c3d4",
      "batch_id": "msgbatch_01...",
      "description": "...",
      "model": "...",
      "status": "...",
      "submitted_at": "...",
      "notified": false,
      "extracted": false,
      "results_file": "..."
    }
  ]
}
```

---

## Job File Format (input to `submit`)

```json
{
  "description": "Human-readable label for this job",
  "model": "claude-sonnet-4-6",
  "max_tokens": 4000,
  "project": "hyperthink",
  "system": "Optional system prompt applied to all requests",
  "requests": [
    {
      "id": "unique-request-id",
      "messages": [
        {"role": "user", "content": "Your prompt here"}
      ]
    },
    {
      "id": "another-request",
      "model": "claude-haiku-4-5",
      "max_tokens": 1000,
      "system": "Override system prompt for this request only",
      "messages": [
        {"role": "user", "content": "Different prompt"}
      ]
    }
  ]
}
```

Per-request fields (`model`, `max_tokens`, `system`) override the top-level defaults.

---

## Anthropic Batch API

### Submit a batch:
```
POST https://api.anthropic.com/v1/messages/batches
Headers:
  x-api-key: <ANTHROPIC_API_KEY>
  anthropic-version: 2023-06-01
  anthropic-beta: message-batches-2024-09-24
  content-type: application/json

Body:
{
  "requests": [
    {
      "custom_id": "<request.id from job file>",
      "params": {
        "model": "<model>",
        "max_tokens": <max_tokens>,
        "system": "<system prompt>",
        "messages": [{"role": "user", "content": "<prompt>"}]
      }
    }
  ]
}
```

Response contains `id` (the batch_id) and `processing_status`.

### Poll a batch:
```
GET https://api.anthropic.com/v1/messages/batches/<batch_id>
Headers: same as above
```

Response field `processing_status`:
- `"in_progress"` — still running, check again later
- `"ended"` — complete, fetch results

### Fetch results:
```
GET https://api.anthropic.com/v1/messages/batches/<batch_id>/results
Headers: same as above
```

Response: JSONL — one JSON object per line:
```jsonl
{"custom_id": "req-id", "result": {"type": "succeeded", "message": {"content": [{"type": "text", "text": "..."}]}}}
{"custom_id": "req-id2", "result": {"type": "errored", "error": {"type": "...", "message": "..."}}}
```

Extract text from a succeeded result:
```python
result["result"]["message"]["content"][0]["text"]
```

---

## `submit` Command — Behaviour

1. Read and validate the job file
2. Generate a `job_id` (8-char hex)
3. Build the Anthropic request body from `requests` array, applying per-request overrides
4. POST to `/v1/messages/batches`
5. Save `state.json` with status `"processing"`, `notified: false`, `extracted: false`
6. Update `registry.json`
7. Print to stdout:
   ```
   Job submitted.
   Job ID: a1b2c3d4
   Batch ID: msgbatch_01...
   ```

---

## `poll` Command — Behaviour

For each job in `batch-jobs/*/state.json` where status is `"processing"` OR
where status is `"complete"` but `notified` or `extracted` is false:

1. Skip if both `notified` and `extracted` are already true
2. If status is `"processing"`: GET `/v1/messages/batches/<batch_id>`
   - If `processing_status != "ended"` → print "still running", skip
   - If `processing_status == "ended"` → fetch results, save to `results.jsonl`, update state
3. If status is `"complete"` and `notified` is false:
   - Notify user (see Notification below)
   - Set `notified: true` in state.json and registry.json
4. Print a summary line per job checked

**Important:** `poll` only sets `notified`. It does NOT set `extracted`.
`extracted` is set by the pipeline poller after it writes output files to disk.

---

## Notification

How to notify the user when a job completes is intentionally left to the implementer.
Options ranked by simplicity:

1. **Print to stdout** — always do this regardless of other methods
2. **Write to a delivery queue** — if your platform has one (e.g. OpenClaw writes a JSON file to a watched directory)
3. **Send an HTTP request** — POST to a webhook URL from `NOTIFY_WEBHOOK_URL` env var
4. **Send a Telegram message** — if `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` env vars are set
5. **Write to a log file** — `NOTIFY_LOG_FILE` env var

Implement at least option 1. Add others based on your environment.

Notification message should include:
- Job description
- Number of succeeded / errored requests
- Path to results file

---

## `status` Command — Behaviour

Print a table of all jobs in registry.json:

```
JOB ID    STATUS      NOTIFIED  EXTRACTED  DESCRIPTION
------------------------------------------------------------------------
a1b2c3d4  complete    yes       yes        Hyperthink Stage 2 — my topic
b2c3d4e5  processing  no        no         Hyperthink Stage 3a — my topic
```

---

## Error Handling

- If Anthropic returns a non-2xx response: print the error body and exit with code 1
- If `ANTHROPIC_API_KEY` is not set: print a clear error and exit with code 1
- If the job file doesn't exist or is invalid JSON: print a clear error and exit with code 1
- If a result has `type: "errored"`: log it, count it, but don't crash — other results may be fine
- On any network timeout: print the error, leave state as-is, exit 0 (will retry on next poll)

---

## Implementation Notes for Your AI

- Use only Python stdlib — no `requests`, no `httpx`, no `boto3`
- Use `urllib.request.Request` for all HTTP calls
- All timestamps in ISO 8601 UTC: `datetime.now(timezone.utc).isoformat()`
- Atomic writes: write to a temp file, then `os.replace()` to avoid partial writes on crash
- The `batch-jobs/` directory and subdirectories must be created automatically if they don't exist
- Print progress to stdout as you go — the poller cron needs to see output to confirm success
- Exit code 0 = success or nothing to do; exit code 1 = unrecoverable error

---

## Minimal Implementation Checklist

File to create: `batch-worker.py`

- [ ] `submit` command reads job file, hits Anthropic API, saves state
- [ ] `poll` command checks all pending jobs, fetches results when done, notifies
- [ ] `status` command prints table
- [ ] `state.json` written with all required fields
- [ ] `registry.json` kept in sync
- [ ] `notified` and `extracted` are separate flags
- [ ] Notification implemented (at minimum: stdout)
- [ ] No third-party packages
- [ ] Handles errors gracefully (no silent failures)
