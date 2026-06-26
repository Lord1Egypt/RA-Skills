# PoYo Sora 2 Pro API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/video-series/sora-2-pro>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/video-series/sora-2-pro.json>

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

- `sora-2-pro` — higher-quality or premium jobs
- `sora-2-pro-private` — private deployment or account-specific private variants

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `prompt` (string, required) — Generation prompt describing the desired output
- `image_urls` (string[], optional) — Reference image URL (for image-to-video). Only one image is supported. Maximum file size: 10MB. Supported formats: .jpeg, .jpg, .png, .webp
- `duration` (integer, optional) — Video duration in seconds (15 or 25) options: 15, 25
- `aspect_ratio` (string, optional) — Video aspect ratio options: 16:9, 9:16
- `style` (string, optional) — Video style options: thanksgiving, comic, news, selfie, nostalgic, anime
- `storyboard` (boolean, optional) — Whether to use storyboard for finer control over video generation details. true: Enable storyboard feature, false: Do not use storyboard

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "sora-2-pro",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "A cinematic drone shot flying through a misty forest at dawn",
    "duration": 25,
    "aspect_ratio": "16:9"
  }
}'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Respect the documented image count limit: `image_urls` allows up to 1 item(s).
- Pick duration deliberately: available values are 15, 25.
- Match aspect ratio to the destination surface: 16:9, 9:16.
- `style` is constrained to: thanksgiving, comic, news, selfie, nostalgic, anime.
- Save the returned `task_id` immediately so status polling is straightforward.
