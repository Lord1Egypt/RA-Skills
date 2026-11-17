# REST Playbook

Use this reference when CLI is unavailable, unsuitable, or missing required capability.

When `modellix-cli` is available, prefer the CLI flow in `cli-playbook.md` (`model run --wait` → `task download`) instead of hand-rolled polling.

## Base URL

`https://api.modellix.ai/api/v1`

## Auth

Header:

```http
Authorization: Bearer <MODELLIX_API_KEY>
```

## Core Endpoint Flow

1) Submit async task:

```http
POST /{provider}/{model_id}/async
```

2) Wait for the existing task:

```http
GET /tasks/{task_id}?wait=true&timeout=45
```

## cURL Example

Submit:

```bash
curl -X POST "https://api.modellix.ai/api/v1/<provider>/<model_id>/async" \
  -H "Authorization: Bearer $MODELLIX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A cute cat playing in a garden on a sunny day"}'
```

The submit response includes `get_result` with the polling endpoint:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "pending",
    "task_id": "task-abc123",
    "model_id": "model-123",
    "get_result": {
      "method": "GET",
      "url": "https://api.modellix.ai/api/v1/tasks/task-abc123"
    }
  }
}
```

Wait:

```bash
curl -X GET "https://api.modellix.ai/api/v1/tasks/<task_id>?wait=true&timeout=45" \
  -H "Authorization: Bearer $MODELLIX_API_KEY"
```

## Status Model

- `pending`: queued, not yet started
- `processing`: actively generating, continue polling
- `success`: read output from `data.result.resources`
- `failed`: inspect error payload

## Retry Policy

Create-task `POST`:

- Submit once. Do not automatically repeat a paid POST, including after `429`, `500`, `503`, a timeout, or a network error.
- When the response is ambiguous, inspect `modellix-cli task history`, the Modellix console, or any returned task id before another paid submission.
- The helper rejects redirects on authenticated requests. Invalid JSON, an invalid success envelope, or a missing usable task ID after submission is an unknown outcome. HTTP error bodies are not consumed or echoed.

Safe task-status `GET` reads may retry:

- `408` (request timeout)
- `429` (too many requests)
- `500` (internal server error)
- `502` (bad gateway)
- `503` (service unavailable)
- `504` (gateway timeout)
- transient transport failures

Strategy:
- Exponential backoff (`1s -> 2s -> 4s`) for reads only
- Max 3 retries for transient read failures
- Respect `X-RateLimit-Reset` for `429` when available

Non-retryable reads:
- `400`, `401`, `402`, `404`

## Notes

- Task outputs expire after 7 days — download promptly.
- Parameter shapes vary per model. If CLI is installed, verify with `modellix-cli model get-schema <slug>` even when submitting over REST. If CLI is unavailable, fetch the model `.md` from https://docs.modellix.ai/llms.txt (or `docs_url` from `model describe`).
- The user names the slug. Do not fill one in when they omit it.
- See `capability-matrix.md` for the CLI ↔ REST mapping.

## Server Wait and File Recovery

`wait` accepts only `true`, `false`, `1`, or `0`; it defaults to false. When true, `timeout` defaults to 30 seconds and accepts integers 1–55. A normal deadline returns HTTP 200/code 0 with the task snapshot and `data.wait = {timed_out, elapsed_ms}`. Keep the task ID and wait again. A snapshot GET without wait remains immediate; its timeout query is ignored. Terminal states include `success`, `failed`, and `canceled`.

The helper uses wait hops of at most 45 seconds, a finite transport margin, and one monotonic total deadline. An absolute socket deadline also bounds slow headers, response bodies, proxy CONNECT, and TLS handshakes. System DNS resolution is platform-controlled; if it returns after the deadline, no connection or request starts. `--initial-wait` and `--max-wait` are deprecated compatibility flags and do not add sleeps between valid wait responses. Only transient read errors back off; paid POSTs and uploads are never replayed automatically.

Use `GET /api/v1/media/files?limit=20&offset=0` to reuse uploaded URLs. CLI/MCP uploads accept at most 16 MiB (16777216 bytes); REST has a separate configurable limit. Defaults are 10 files per team, 2 concurrent uploads, and 7-day retention. On 429, list files and explicitly approve deleting an unneeded ID with `DELETE /api/v1/media/files/{file_id}`. Never auto-delete files or retry uploads to clear quota.
