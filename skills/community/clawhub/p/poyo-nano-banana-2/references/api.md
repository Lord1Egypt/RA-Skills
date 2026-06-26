# PoYo Nano Banana 2 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: see PoYo unified task status docs at <https://docs.poyo.ai/api-manual/task-management/status>
- Model page: <https://poyo.ai/models/nano-banana-2>
- Source docs: <https://docs.poyo.ai/api-manual/image-series/nano-banana-2-new>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Models

- `nano-banana-2-new`: text-to-image and image-to-image generation
- `nano-banana-2-new-edit`: advanced image editing

## Request schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object

`input` fields:

- `prompt` string, required, max 1000 chars
- `image_urls` string[] URI, optional, supports up to 14 reference images
- `size` enum, optional: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`
- `resolution` enum, optional: `1K`, `2K`, `4K` (default `1K`)
- `google_search` boolean, optional

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "nano-banana-2-new",
    "input": {
      "prompt": "A cyberpunk street scene with neon signs and rain",
      "size": "16:9",
      "resolution": "2K"
    }
  }'
```

## Edit example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "nano-banana-2-new-edit",
    "input": {
      "prompt": "Add colorful flowers in the foreground",
      "image_urls": ["https://example.com/landscape.jpg"],
      "size": "16:9",
      "resolution": "2K"
    }
  }'
```

## Typical response

```json
{
  "code": 200,
  "data": {
    "task_id": "task-unified-1757165031-uyujaw3d",
    "status": "not_started",
    "created_time": "2025-11-12T10:30:00"
  }
}
```

## Polling notes

- Save `task_id` immediately.
- If `callback_url` is provided, PoYo sends a POST callback when status becomes `finished` or `failed`.
- Even with callbacks, the user can still query unified task status directly.

## Error patterns

### 400

```json
{
  "code": 400,
  "error": {
    "message": "Invalid request parameters",
    "type": "invalid_request_error"
  }
}
```

### 401

```json
{
  "code": 401,
  "error": {
    "message": "Unauthorized - Invalid API key",
    "type": "authentication_error"
  }
}
```

## Practical guidance

- Use `nano-banana-2-new-edit` whenever the user explicitly wants to modify a supplied image.
- Use `image_urls` only when the request truly depends on source/reference images.
- Prefer `2K` for a balance of quality and cost unless the user explicitly asks for `4K`.
- Prefer `16:9` for banners/screens, `1:1` for avatars/posts, and `9:16` for stories/mobile.
- If a user asks for factual real-world grounding, consider `google_search: true`.
