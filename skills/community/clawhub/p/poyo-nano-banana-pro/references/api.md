# PoYo Nano Banana Pro API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/nano-banana-2>
- Model page: <https://poyo.ai/models/nano-banana-2-api>
- Example repository: <https://github.com/PoyoAPI/nano-banana-pro-api>

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

- `nano-banana-pro`: image generation and reference-guided generation
- `nano-banana-pro-edit`: image editing with one or more source images

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, optional
- `size` string, optional
- `resolution` string, optional
- `output_format` string, optional
- `enable_web_search` boolean, optional
- `n` number, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Generate Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "nano-banana-pro",
    "input": {
      "prompt": "A premium campaign visual for a modular desk lamp, warm interior scene, accurate product geometry, soft shadows, tasteful negative space for headline text",
      "size": "auto",
      "resolution": "2K",
      "output_format": "png",
      "enable_web_search": false,
      "n": 1
    }
  }'
```

## Edit Example

Use `nano-banana-pro-edit` when the request includes one or more source images.

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "nano-banana-pro-edit",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Preserve the source subject, improve the scene composition, and keep the result realistic and production-ready",
      "size": "auto",
      "resolution": "2K",
      "output_format": "png",
      "enable_web_search": false,
      "n": 1,
      "image_urls": [
        "https://example.com/source-product.png"
      ]
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

- Use `nano-banana-pro` when the task starts from a prompt or needs reference-guided generation.
- Use `nano-banana-pro-edit` when the user asks to modify supplied images.
- Use `image_urls` only when the request truly depends on source or reference images.
- Use web search only for tasks that benefit from current real-world grounding.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
