# PoYo Nano Banana 2 Lite API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: use the PoYo unified task status API after saving `data.task_id`
- Model page: <https://poyo.ai/models/nano-banana-2-lite>

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

- `nano-banana-2-lite`: fast text-to-image generation
- `nano-banana-2-lite-edit`: lightweight image editing

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, required for `nano-banana-2-lite-edit`
- `size` string, optional

Always verify current field support on the PoYo model page before relying on model-specific options.

## Generate Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "nano-banana-2-lite",
    "input": {
      "prompt": "A clean isometric product concept image of a compact desk garden, natural daylight, simple background, crisp detail",
      "size": "1:1"
    }
  }'
```

## Edit Example

Use `nano-banana-2-lite-edit` when the request includes source images.

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "nano-banana-2-lite-edit",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Keep the main object recognizable, simplify the background, and make the lighting softer",
      "image_urls": [
        "https://example.com/source-image.png"
      ],
      "size": "1:1"
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
    "created_time": "2026-07-01T08:00:00"
  }
}
```

## Polling Notes

- Save `data.task_id` immediately after submission.
- Poll the unified status endpoint for local tests.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states.
- Store final image URLs only after the task reaches a terminal success state.

## Practical Guidance

- Use `nano-banana-2-lite` for fast prompt-only image drafts.
- Use `nano-banana-2-lite-edit` when the user asks to modify supplied images.
- Keep prompts concise and specific for fast iteration.
- Use source images only when they are necessary to the edit request.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
