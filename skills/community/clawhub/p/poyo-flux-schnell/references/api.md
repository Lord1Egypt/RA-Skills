# PoYo FLUX Schnell API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/flux-schnell>
- Model page: <https://poyo.ai/models/flux-schnell>

## Auth

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>. Use the server-side `POYO_API_KEY` environment variable.

## Model

- `flux-schnell`

## Request Schema

Top-level fields:

- `model` string, required
- `input` object, required
- `callback_url` string URI, optional

`input` fields:

- `prompt` string, required
- `size` string, optional; documented presets and supported custom `WIDTHxHEIGHT` values
- `n` integer, optional, minimum one
- `output_format` string, optional: `png` or `jpeg`

`image_urls` is not supported. Always verify current size support in the PoYo documentation before production use.

## Text-to-Image Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "flux-schnell",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "A bright editorial photograph of a compact electric bicycle on a modern city street",
      "size": "4:3",
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

- Use this model only for prompt-based generation.
- Choose the destination size before submission; do not assume every arbitrary dimension is accepted.
- Select `png` for lossless output or `jpeg` when that documented format better fits the downstream workflow.
- Avoid logging API keys, private prompts, result URLs, or callback URLs.
