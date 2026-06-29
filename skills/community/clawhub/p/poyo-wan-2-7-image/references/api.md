# PoYo Wan 2.7 Image API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/wan-2-7-image>
- Model page: <https://poyo.ai/models/wan-2-7-image>

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

- `wan-2.7-image`: text-to-image generation and image editing.

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

Documented `size` preset strings include:

- `512x512`
- `1024x1024`
- `768x1024`
- `1024x768`
- `576x1024`
- `1024x576`

For custom dimensions, use an object such as:

```json
{
  "width": 1200,
  "height": 800
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
    "model": "wan-2.7-image",
    "input": {
      "prompt": "A clean studio product image of a translucent smart speaker on a brushed aluminum desk, soft side lighting, crisp reflections, white background",
      "size": "1024x1024",
      "n": 2
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
    "model": "wan-2.7-image",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Keep the product shape and logo placement. Change the background to a warm kitchen counter with morning light and add soft natural shadows",
      "image_urls": [
        "https://example.com/product-reference.png"
      ],
      "size": {
        "width": 1024,
        "height": 768
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
