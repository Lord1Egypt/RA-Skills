# PoYo Hailuo 02 API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/video-series/hailuo-02>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/video-series/hailuo-02.json>

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

- `hailuo-02` — general generation with this model variant
- `hailuo-02-pro` — higher-quality or premium jobs

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `prompt` (string, required) — Generation prompt describing the desired video
- `image_urls` (string[], optional) — Reference image URLs for image-to-video generation (required for image-to-video)
- `duration` (integer, optional) — Video duration in seconds (hailuo-02 only) options: 6, 10
- `resolution` (string, optional) — Output resolution (hailuo-02 image-to-video only) options: 512P, 768P
- `end_image_url` (string, optional) — Optional URL of the image to use as the last frame (image-to-video only)
- `prompt_optimizer` (boolean, optional) — Enable AI-powered prompt optimization

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "hailuo-02",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "A llama and a raccoon battle in an intense table tennis match inside a roaring Olympic stadium",
    "duration": 6,
    "prompt_optimizer": true
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
- Use a supported `resolution`: 512P, 768P.
- Save the returned `task_id` immediately so status polling is straightforward.
