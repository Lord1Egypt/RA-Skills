# PoYo Sora 2 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/video-series/sora-2>

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

- `sora-2`: standard quality video generation
- `sora-2-private`: private standard-quality variant

## Request schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object

`input` fields:

- `prompt` string, required
- `image_urls` string[] URI, optional, for image-to-video only, max 1 image
- `duration` enum integer, optional: `10`, `15`
- `aspect_ratio` enum string, optional: `16:9`, `9:16`
- `style` enum string, optional: `thanksgiving`, `comic`, `news`, `selfie`, `nostalgic`, `anime`
- `storyboard` boolean, optional

Reference-image notes from PoYo docs:

- only one image is supported
- maximum file size: 10 MB
- supported formats: `.jpeg`, `.jpg`, `.png`, `.webp`

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "sora-2",
    "input": {
      "prompt": "A cinematic drone shot over a futuristic city at sunset",
      "duration": 15,
      "aspect_ratio": "16:9"
    }
  }'
```

## Image-to-video example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "sora-2",
    "input": {
      "prompt": "Animate this concept art into a smooth cinematic shot",
      "image_urls": ["https://example.com/frame.png"],
      "duration": 10,
      "aspect_ratio": "16:9",
      "style": "anime"
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

- Prefer `sora-2` unless the user explicitly requests the private variant.
- Use `10s` for quick tests and `15s` for fuller motion sequences.
- Use `16:9` for landscape scenes and `9:16` for mobile-first output.
- Use `storyboard: true` only when the user wants finer control over generation details.
- For sensitive images, do not upload them to public URLs casually before passing them in `image_urls`.
