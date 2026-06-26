# PoYo Seedream 5 0 Lite API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/image-series/seedream-5-0-lite>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/image-series/seedream-5-0-lite.json>

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

- `seedream-5.0-lite` — general generation with this model variant
- `seedream-5.0-lite-edit` — editing or modifying supplied images

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `prompt` (string, required) — Generation prompt describing the desired output
- `image_urls` (string[], optional) — Reference image URLs for image-to-image or editing (1-10 images). Required for seedream-5.0-lite-edit model. Supported formats: JPEG, PNG
- `size` (string, optional) — Specify the output image dimensions. Two methods are available, but they cannot be used at the same time.  Method 1: Specify the resolution of the generated image, and describe its aspect ratio, shape, or purpose in the prompt using natural language. You let the model determine the width and height. Optional values: 2K, 3K  Method 2: Specify the aspect ratio of the generated image. Optional values: 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9 options: 2K, 3K, 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9
- `n` (integer, optional) — Number of images to generate (1-15). Credits are pre-deducted based on this count

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "seedream-5.0-lite",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "A serene Japanese garden with cherry blossoms and a koi pond",
    "size": "16:9",
    "n": 1
  }
}'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Respect the documented image count limit: `image_urls` allows up to 10 item(s).
- Use a supported `size`: 2K, 3K, 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9.
- Save the returned `task_id` immediately so status polling is straightforward.
