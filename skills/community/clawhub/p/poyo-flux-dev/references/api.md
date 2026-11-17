# PoYo FLUX Dev API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/flux-dev>
- Model page: <https://poyo.ai/models/flux-dev>

## Auth

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>. Use the server-side `POYO_API_KEY` environment variable.

## Model

- `flux-dev`

## Request Schema

Top-level fields:

- `model` string, required
- `input` object, required
- `callback_url` string URI, optional

`input` fields:

- `prompt` string, required
- `image_urls` string array, optional, exactly one item when editing
- `size` string, optional; documented presets and supported custom `WIDTHxHEIGHT` values
- `n` integer, optional, minimum one
- `output_format` string, optional: `png` or `jpeg`

Always verify current size support in the PoYo documentation before production use.

## Text-to-Image Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "flux-dev",
    "input": {
      "prompt": "A cinematic product photograph of a matte black smart speaker on a marble table, soft studio lighting",
      "size": "4:3",
      "n": 1,
      "output_format": "png"
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
    "model": "flux-dev",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Turn the scene into a clean studio product shot while preserving the subject shape",
      "image_urls": [
        "https://example.com/source-product.png"
      ],
      "n": 1,
      "output_format": "png"
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

- Omit `image_urls` for text-to-image generation.
- Provide exactly one accessible source URL for editing.
- Choose the destination size before submission; do not assume every arbitrary dimension is accepted.
- Avoid logging API keys, private prompts, source URLs, result URLs, or callback URLs.
