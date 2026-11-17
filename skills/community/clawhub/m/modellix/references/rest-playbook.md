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

2) Poll task:

```http
GET /tasks/{task_id}
```

## cURL Example

Submit:

```bash
curl -X POST "https://api.modellix.ai/api/v1/google/nano-banana-2-lite/async" \
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

Poll:

```bash
curl -X GET "https://api.modellix.ai/api/v1/tasks/<task_id>" \
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
- Default T2I slug when the user omits a model: `google/nano-banana-2-lite`.
- Default T2V slug when the user omits a model: `bytedance/seedance-2.0-mini-t2v`.
- Default TTS slug when the user omits a model: `alibaba/qwen-audio-3.0-tts-flash`.
- Default STT slug when the user omits a model: `openai/whisper-1`.
- Default STS slug when the user omits a model: `alibaba/cosyvoice-clone`.
- See `capability-matrix.md` for the full default-model table and CLI ↔ REST mapping.
