# IMINI Nano Banana API Reference

Source docs:
- [Nano Banana](https://nexuslinelimited-1d434f54.mintlify.app/zh/api-reference/images/nano-banana)
- [Task Query](https://nexuslinelimited-1d434f54.mintlify.app/zh/api-reference/images/task-query)

## Base URL

Default base URL:

```text
https://openapi.imini.ai/imini/router
```

## Authentication

Use Bearer auth:

```http
Authorization: Bearer <token>
```

The token should come from `IMINI_IMAGE_API_KEY`.

## Create Generation Task

Endpoint:

```text
POST /v1/images/generate
```

Required JSON fields:

```json
{
  "model": "google/nano-banana",
  "prompt": "..."
}
```

Supported model values:
- `google/nano-banana`
- `google/nano-banana-pro`
- `google/nano-banana-2`

Optional fields:

```json
{
  "images": [
    {
      "url": "https://example.com/input.jpg",
      "reference_type": "asset"
    }
  ],
  "aspect_ratio": "1:1",
  "resolution": "1K"
}
```

Notes:
- `images[].url` must be a public URL.
- `images[].reference_type` supports:
  - `asset`: content reference
  - `style`: style reference
- `images` max length depends on model:
  - `google/nano-banana`: up to 3
  - `google/nano-banana-pro`: up to 14
  - `google/nano-banana-2`: up to 14
- `aspect_ratio` values supported by all three models:
  - `1:1`
  - `2:3`
  - `3:2`
  - `3:4`
  - `4:3`
  - `4:5`
  - `5:4`
  - `9:16`
  - `16:9`
  - `21:9`
- additional aspect ratios supported by `google/nano-banana-2`:
  - `1:4`
  - `1:8`
  - `4:1`
  - `8:1`
- `resolution` depends on model:
  - `google/nano-banana`: `1K`
  - `google/nano-banana-pro`: `1K`, `2K`, `4K`
  - `google/nano-banana-2`: `512`, `1K`, `2K`, `4K`

Success response:

```json
{
  "task_id": "task_2041350318103396352",
  "model": "google/nano-banana",
  "created_at": "2026-04-07T03:00:17.062Z",
  "request_id": "285f20ce-8158-401b-945c-7bc6a7ef6ead"
}
```

Validation error shape:

```json
{
  "error": {
    "code": "INVALID_PROMPT",
    "message": "Prompt contains disallowed content",
    "status": 400,
    "request_id": "req_abc123"
  }
}
```

## Query Task Status

Endpoint:

```text
GET /v1/images/tasks/{task_id}
```

Task status enum:
- `queued` (observed in live API, waiting in queue)
- `pending`
- `processing`
- `succeeded`
- `failed`

Success response example:

```json
{
  "task_id": "task_8f3a2c1b9d4e",
  "status": "succeeded",
  "model": "google/nano-banana-2",
  "created_at": "2026-03-30T10:00:00Z",
  "completed_at": "2026-03-30T10:00:12Z",
  "images": [
    {
      "url": "https://file.iminicdn.com/file/2026/04/06/2041350421116751872.png",
      "width": 1920,
      "height": 1080
    }
  ],
  "error": null,
  "request_id": "req_abc123"
}
```

Failure response still returns task details, with:
- `status: "failed"`
- `error` populated

## Implementation Expectations

The bundled script should:

1. Submit the create-task request.
2. Extract `task_id`.
3. Poll until status becomes `succeeded` or `failed`.
4. Fail on timeout.
5. Download every URL in `images[]` when successful.
6. Print saved file paths, `task_id`, and `request_id`.
