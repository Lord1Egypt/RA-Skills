# PoYo Wan 2 6 API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/video-series/wan-2-6>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/video-series/wan-2-6.json>

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

- `wan2.6-text-to-video` — general generation with this model variant
- `wan2.6-image-to-video` — general generation with this model variant
- `wan2.6-video-to-video` — general generation with this model variant

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `prompt` (string, required) — Text prompt for video generation
- `image_urls` (string[], optional) — Reference image URLs for image-to-video (wan2.6-image-to-video only). Max 1 image; supported formats: .jpeg, .jpg, .png, .webp; max size 10MB
- `duration` (integer, optional) — Video duration in seconds (15 seconds supported for text-to-video and image-to-video) options: 5, 10, 15
- `resolution` (string, optional) — Output video resolution options: 720p, 1080p
- `video_urls` (string[], optional) — Reference video URLs for video-to-video (wan2.6-video-to-video only). Max 3 videos; supported formats: .mp4, .mov, .mkv; max size 10MB
- `multi_shots` (boolean, optional) — Enable multi-shot composition (single continuous shot when false)

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "wan2.6-text-to-video",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "A cinematic time-lapse of a bustling city street transitioning from day to night.",
    "duration": 5,
    "resolution": "1080p",
    "multi_shots": false
  }
}'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Respect the documented image count limit: `image_urls` allows up to 1 item(s).
- Pick duration deliberately: available values are 5, 10, 15.
- Use a supported `resolution`: 720p, 1080p.
- Save the returned `task_id` immediately so status polling is straightforward.
