# PoYo Grok Imagine API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/video-series/grok-imagine>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/video-series/grok-imagine.json>

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

- `grok-imagine` — general generation with this model variant

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `prompt` (string, required) — Generation prompt describing the desired video motion
- `image_urls` (string[], optional) — Reference image URLs for image-to-video generation (required for image-to-video, max 1 image)
- `duration` (integer, optional) — The duration of the generated video in seconds options: 6, 10
- `aspect_ratio` (string, optional) — Video aspect ratio (text-to-video only) options: 1:1, 2:3, 3:2
- `mode` (string, optional) — Generation style mode options: fun, normal, spicy

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "grok-imagine",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "A couple of doors open sequentially, revealing living rooms, kitchens, bedrooms, and offices with residents inside",
    "aspect_ratio": "16:9",
    "mode": "normal"
  }
}'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Respect the documented image count limit: `image_urls` allows up to 1 item(s).
- Pick duration deliberately: available values are 6, 10.
- Match aspect ratio to the destination surface: 1:1, 2:3, 3:2.
- Save the returned `task_id` immediately so status polling is straightforward.
