# PoYo Flux Kontext API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/flux-kontext>
- Model page: <https://poyo.ai/models/flux-kontext>

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

- `flux-kontext-pro`: Pro text-to-image generation.
- `flux-kontext-pro-edit`: Pro image editing with one source image.
- `flux-kontext-max`: Max text-to-image generation.
- `flux-kontext-max-edit`: Max image editing with one source image.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, required for edit models, maximum one image
- `size` string, optional: `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `21:9`, or `9:21`
- `output_format` string, optional: `png` or `jpg`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Generate Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "flux-kontext-pro",
    "input": {
      "prompt": "A premium product photograph of a compact glass perfume bottle on a reflective marble surface, clean studio lighting, soft shadows",
      "size": "16:9",
      "output_format": "png"
    }
  }'
```

## Edit Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "flux-kontext-max-edit",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Replace the background with a minimal warm studio backdrop while preserving the product shape and lighting direction",
      "image_urls": [
        "https://example.com/source-product.jpg"
      ],
      "size": "1:1",
      "output_format": "jpg"
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

- Use generation models when the request starts from text only.
- Use edit models when the user provides exactly one source image.
- Match `size` to the destination format before submitting.
- Use `output_format` when the downstream workflow requires a specific image format.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
