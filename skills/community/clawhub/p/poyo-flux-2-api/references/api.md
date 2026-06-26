# PoYo Flux 2 API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/image-series/flux-2>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/image-series/flux-2.json>

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

- `flux-2-pro` — higher-quality or premium jobs
- `flux-2-pro-edit` — editing or modifying supplied images
- `flux-2-flex` — general generation with this model variant
- `flux-2-flex-edit` — editing or modifying supplied images

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `prompt` (string, required) — Generation prompt describing the desired output
- `image_urls` (string[], optional) — Input reference images (1-8 images). Required for edit models (flux-2-pro-edit, flux-2-flex-edit)
- `size` (string, required) — Image size ratio. Use 'auto' to automatically detect based on first input image options: 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, auto
- `resolution` (string, required) — Output image resolution options: 1K, 2K

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "flux-2-pro",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "The jar in image 1 is filled with capsules exactly same as image 2 with the exact logo",
    "size": "1:1",
    "resolution": "1K"
  }
}'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Respect the documented image count limit: `image_urls` allows up to 8 item(s).
- Use a supported `size`: 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, auto.
- Use a supported `resolution`: 1K, 2K.
- Save the returned `task_id` immediately so status polling is straightforward.
