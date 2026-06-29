# PoYo Generate Music API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Music detail: `GET https://api.poyo.ai/api/generate/detail/music`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/generate-music>
- Music detail docs: <https://docs.poyo.ai/api-manual/music-series/query-music-detail>
- Webhook docs: <https://docs.poyo.ai/api-manual/music-series/music-webhook>
- Model page: <https://poyo.ai/models/generate-music>

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

- `generate-music`: text-driven music generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required depending on mode
- `custom_mode` boolean, required for mode selection
- `instrumental` boolean, optional
- `style` string, required in custom instrumental mode
- `title` string, required in custom instrumental mode
- `mv` string, optional documented music version
- `negative_tags` string, optional
- `style_weight` number, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Simple Mode Example

Use simple mode when the user wants a fast first test with a compact prompt.

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "generate-music",
    "input": {
      "prompt": "Create a bright 30 second electronic background track for a product launch video, optimistic and polished",
      "custom_mode": false,
      "instrumental": false,
      "mv": "V4"
    }
  }'
```

## Custom Instrumental Example

Use custom mode when the user needs title and style control.

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "generate-music",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "A calm and relaxing piano track with soft melodies",
      "style": "Classical, peaceful, minimal",
      "title": "Quiet Launch",
      "custom_mode": true,
      "instrumental": true,
      "mv": "V5_5",
      "negative_tags": "Heavy metal, aggressive drums",
      "style_weight": 0.65
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
    "created_time": "2026-05-19T08:00:00"
  }
}
```

## Result Retrieval Notes

- Save `data.task_id` immediately after submission.
- Use the music detail endpoint for generated music task results.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states when receiving callbacks.
- Download returned audio and cover image files before relying on them long term.

## Practical Guidance

- Start with `custom_mode: false` for quick tests.
- Use `custom_mode: true` when the user needs title, style, or instrumental control.
- Keep private lyrics and private prompts out of logs unless explicitly allowed by the product policy.
- Do not expose generated audio URLs in public logs or screenshots.
