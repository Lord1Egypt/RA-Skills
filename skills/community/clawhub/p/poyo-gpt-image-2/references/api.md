# PoYo GPT Image 2 API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/image-series/gpt-image-2>
- Model page: <https://poyo.ai/models/gpt-image-2>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/image-series/gpt-image-2.json>

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

- `gpt-image-2` — text-to-image generation and optional reference-image-guided generation
- `gpt-image-2-edit` — image editing from one or more reference images; requires `image_urls`

## Key input fields

- `model` (string, required) — choose `gpt-image-2` or `gpt-image-2-edit`
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `input.prompt` (string, required, max 4000 chars) — Prompt describing the target image or requested edit
- `input.image_urls` (string[], optional) — Reference image URLs; required for `gpt-image-2-edit`; supports multiple input images
- `input.size` (string, optional, default `auto`) — Output aspect ratio or custom pixel size
- `input.resolution` (string, optional, default `1K`) — Output resolution: `1K`, `2K`, or `4K`

## Size and resolution

Preset `size` values:

- `auto`
- `1:1`, `2:3`, `3:2`, `4:3`, `3:4`, `4:5`, `5:4`
- `16:9`, `9:16`, `21:9`

Custom size:

- Use `WIDTHxHEIGHT`, for example `2304x1536`.
- Custom size requires `resolution` to be `2K` or `4K`.
- `auto` size or omitted `size` always uses `1K` resolution.
- True `4K` billing applies only to `16:9`, `9:16`, `21:9`, or custom sizes with a 3840-pixel edge; other `4K` selections are billed as `2K`.

## Important constraints

- `gpt-image-2-edit` requires `image_urls`.
- Each request returns a single image.
- Public image URLs must be directly downloadable by the upstream provider.

## Text-to-image example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-image-2",
    "callback_url": "https://your-domain.com/callback",
    "input": {
      "prompt": "A premium product photo of a silver espresso machine on a clean white studio background, realistic lighting, high detail",
      "size": "1:1"
    }
  }'
```

## 2K generation example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-image-2",
    "callback_url": "https://your-domain.com/callback",
    "input": {
      "prompt": "A premium product photo of a silver espresso machine on a clean white studio background, realistic lighting, high detail",
      "size": "16:9",
      "resolution": "2K"
    }
  }'
```

## 4K generation example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-image-2",
    "callback_url": "https://your-domain.com/callback",
    "input": {
      "prompt": "A cinematic landscape with dramatic lighting, ultra-high detail",
      "size": "16:9",
      "resolution": "4K"
    }
  }'
```

## Custom size example

```bash
curl -sS https://api.poyo.ai/api/generate/submit \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-image-2",
    "callback_url": "https://your-domain.com/callback",
    "input": {
      "prompt": "A premium product photo of a silver espresso machine on a clean white studio background",
      "size": "2304x1536",
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
    "model": "gpt-image-2-edit",
    "callback_url": "https://your-domain.com/callback",
    "input": {
      "prompt": "Use these reference images together to create a polished product photo: keep the flower subject, use the vase shape from the second image, replace the background with a clean white studio backdrop, and add a soft natural shadow",
      "image_urls": [
        "https://example.com/flower.jpg",
        "https://example.com/vase.jpg"
      ],
      "size": "1:1"
    }
  }'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Use `gpt-image-2` for pure prompt generation; add `image_urls` only when reference-guided generation is needed.
- Use `gpt-image-2-edit` when the prompt asks to modify supplied images.
- Choose `auto` or omit `size` for default 1K output; specify `resolution` when the user needs 2K or 4K.
- Save the returned `task_id` immediately so status polling is straightforward.
