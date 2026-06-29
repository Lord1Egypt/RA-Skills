# PoYo Wan 2.7 Image Pro API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/wan-2-7-image-pro>
- Model page: <https://poyo.ai/models/wan-2-7-image-pro>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Model

- `wan-2.7-image-pro`: text-to-image generation and image editing.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, optional, one to four images for editing
- `size` string or object, optional
- `n` integer, optional, one to four images
- `seed` integer, optional

Documented `size` preset strings include `512x512`, `1024x1024`, `768x1024`, `1024x768`, `576x1024`, and `1024x576`.

For custom dimensions, pass:

```json
{
  "width": 1280,
  "height": 720
}
```

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Image Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "wan-2.7-image-pro",
    "input": {
      "prompt": "A refined editorial product image of a matte black camera on a glass desk, soft daylight, precise reflections, minimal background",
      "size": "1024x1024",
      "n": 2,
      "seed": 12345
    }
  }'
```

## Image Editing Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "wan-2.7-image-pro",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Keep the product from image 1. Change the setting to a clean showroom with warm morning light and realistic contact shadows",
      "image_urls": [
        "https://example.com/product-reference.png"
      ],
      "size": {
        "width": 1280,
        "height": 720
      },
      "n": 1
    }
  }'
```

## Typical Submit Response

```json
{
  "code": 200,
  "data": {
    "task_id": "task_unified_example",
    "status": "not_started",
    "created_time": "2026-05-23T08:00:00"
  }
}
```

## Polling Notes

- Save `data.task_id` immediately after submission.
- Poll the status endpoint for local tests.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states.
- Store final image URLs only after the task reaches a terminal success state.

## Practical Guidance

- Omit `image_urls` for pure text-to-image.
- Include one to four `image_urls` only when the request depends on source images.
- Keep reference image order stable because edit instructions can depend on it.
- Match `size` to the destination surface before submission.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
