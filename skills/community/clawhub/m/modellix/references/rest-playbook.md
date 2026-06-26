# REST Playbook

Use this reference when CLI is unavailable, unsuitable, or missing required capability.

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
curl -X POST "https://api.modellix.ai/api/v1/alibaba/qwen-image-plus/async" \
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

Retryable:
- `429` (too many requests)
- `500` (internal server error)
- `503` (service unavailable)

Strategy:
- Exponential backoff (`1s -> 2s -> 4s`)
- Max 3 retries for `500`/`503`
- Respect `X-RateLimit-Reset` for `429` when available

Non-retryable:
- `400`, `401`, `402`, `404`

## Notes

- Task outputs expire after 24 hours.
- Parameter shapes vary per model; always verify model docs before invocation.
