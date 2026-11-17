# PoYo Extend Music API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/extend-music>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/extend-music.json>
- Model page: <https://poyo.ai/models/extend-music>

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

- `extend-music`: extend or modify existing music by creating a continuation from a source audio track.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Required `input` fields:

- `default_param_flag` boolean
- `audio_id` string
- `mv` string

Additional required fields when `default_param_flag` is `true`:

- `prompt` string
- `style` string
- `title` string
- `continue_at` number

Optional `input` fields:

- `negative_tags` string
- `vocal_gender` string
- `style_weight` number
- `weirdness_constraint` number
- `audio_weight` number
- `persona_id` string

Always verify current field support in the PoYo docs before relying on model-specific options.

## Simple Mode Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "extend-music",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "default_param_flag": false,
      "audio_id": "audio_track_example",
      "mv": "V4_5PLUS"
    }
  }'
```

## Custom Mode Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "extend-music",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "default_param_flag": true,
      "audio_id": "audio_track_example",
      "prompt": "Continue with a brighter chorus and clean vocal line",
      "style": "cinematic pop, warm drums, wide chorus",
      "title": "Extended Chorus",
      "continue_at": 60,
      "mv": "V5",
      "negative_tags": "harsh noise, muddy mix",
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
    "created_time": "2026-07-08T08:00:00"
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

- Use simple mode when the user wants a straightforward continuation from the existing track.
- Use custom mode when the user needs a specific continuation point, title, style, or creative direction.
- Save `data.task_id` immediately after submission.
- Use `callback_url` for production queues and longer user workflows.
- Keep private prompts, source audio identifiers, callback URLs, and generated audio URLs out of logs.
