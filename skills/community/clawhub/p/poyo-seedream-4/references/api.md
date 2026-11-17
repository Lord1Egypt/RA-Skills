# PoYo Seedream 4 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/seedream-4>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/image-series/seedream-4.json>
- Model page: <https://poyo.ai/models/seedream-4>

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

- `seedream-4`: text-to-image generation and optional reference-guided generation
- `seedream-4-edit`: image editing with one or more source images

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, required for `seedream-4-edit`
- `size` string, optional; supported aspect ratios include `1:1`, `3:4`, `4:3`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9`
- `resolution` string, optional; supported presets include `1K`, `2K`, `4K`
- `n` integer, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Generate Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "seedream-4",
    "input": {
      "prompt": "A minimalist product photo of a ceramic mug on a clean studio background",
      "size": "1:1",
      "resolution": "1K",
      "n": 1
    }
  }'
```

## Edit Example

Use `seedream-4-edit` when the request includes source images.

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "seedream-4-edit",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Transform this scene into a polished ecommerce product photo with clean studio lighting",
      "image_urls": [
        "https://example.com/source-image.jpg"
      ],
      "size": "1:1",
      "resolution": "1K",
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
    "created_time": "2026-05-03T08:00:00"
  }
}
```

## Status Query Example

```bash
curl --fail-with-body --request GET \
  --url "https://api.poyo.ai/api/generate/status/task_unified_example" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

## Practical Guidance

- Use `seedream-4` for prompt-first image generation.
- Use `seedream-4-edit` when the user asks to modify supplied images.
- Use `image_urls` only when the request depends on source or reference images.
- Save `data.task_id` immediately after submission.
- Use `callback_url` for production queues and longer user workflows.
- Avoid logging API keys, private prompts, private source image URLs, callback URLs, or generated output URLs.
