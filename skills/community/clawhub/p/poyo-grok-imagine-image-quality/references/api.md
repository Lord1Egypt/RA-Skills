# PoYo Grok Imagine Image Quality API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/grok-imagine-image-quality>
- Model page: <https://poyo.ai/models/grok-imagine-image-quality>

## Auth

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>. Use the server-side `POYO_API_KEY` environment variable.

## Model

- `grok-imagine-image-quality`

## Request Schema

Top-level fields:

- `model` string, required
- `input` object, required
- `callback_url` string URI, optional

`input` fields:

- `prompt` string, required
- `image_urls` string array, optional, maximum three; including references selects editing behavior
- `n` integer, optional, minimum one
- `aspect_ratio` string, optional: `1:1`, `2:3`, `3:2`, `9:16`, or `16:9`
- `resolution` string, optional: `1K` or `2K`
- `output_format` string, optional: `png`, `jpeg`, `jpg`, or `webp`
- `sync_mode` boolean, optional when supported by the current service

Always verify current field support in the PoYo documentation before production use.

## Text-to-Image Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "grok-imagine-image-quality",
    "input": {
      "prompt": "A premium product photograph of a compact matte black speaker on a marble table, soft studio lighting",
      "aspect_ratio": "1:1",
      "resolution": "1K",
      "output_format": "png",
      "n": 1
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
    "model": "grok-imagine-image-quality",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Replace the background with a warm modern studio while preserving the product shape",
      "image_urls": [
        "https://example.com/source-product.png"
      ],
      "aspect_ratio": "1:1",
      "resolution": "2K",
      "output_format": "webp",
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
    "created_time": "2026-07-21T08:00:00"
  }
}
```

## Polling Notes

- Save `data.task_id` immediately after submission.
- Poll the status endpoint for local tests or provide `callback_url` for production queues.
- Treat documented success and failure states as terminal.
- Persist generated image URLs only after a successful terminal state.

## Practical Guidance

- Omit `image_urls` when starting from text only.
- Keep all reference URLs accessible to the generation service for the duration of the task.
- Match aspect ratio and resolution to the destination before submission.
- Avoid logging API keys, private prompts, reference URLs, result URLs, or callback URLs.
