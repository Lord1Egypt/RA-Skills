# PoYo Upload and Extend Audio API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Music detail: `GET https://api.poyo.ai/api/generate/detail/music`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/upload-and-extend-audio>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/upload-and-extend-audio.json>
- Music detail docs: <https://docs.poyo.ai/api-manual/music-series/query-music-detail>
- Music webhook docs: <https://docs.poyo.ai/api-manual/music-series/music-webhook>
- Model page: <https://poyo.ai/models/upload-and-extend-audio>

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

- `upload-and-extend-audio`: extends uploaded audio while preserving the source style.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `upload_url` string URI, required
- `default_param_flag` boolean, required
- `instrumental` boolean, required
- `continue_at` number, required by the current docs
- `mv` string, required by the current docs
- `prompt` string, optional depending on mode
- `style` string, optional depending on mode
- `title` string, optional depending on mode
- `negative_tags` string, optional
- `vocal_gender` string, optional
- `style_weight` number, optional
- `weirdness_constraint` number, optional
- `audio_weight` number, optional
- `persona_id` string, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Simple Extension Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "upload-and-extend-audio",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "upload_url": "https://example.com/audio/source-track.mp3",
      "default_param_flag": false,
      "instrumental": true,
      "continue_at": 60,
      "mv": "V5"
    }
  }'
```

## Custom Extension Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "upload-and-extend-audio",
    "input": {
      "upload_url": "https://example.com/audio/source-track.mp3",
      "default_param_flag": true,
      "instrumental": false,
      "prompt": "Continue with a brighter chorus and clean vocal line",
      "style": "cinematic pop, warm drums, wide chorus",
      "title": "Extended Chorus",
      "continue_at": 60,
      "mv": "V4_5PLUS",
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
    "created_time": "2026-07-07T08:00:00"
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

- Use a public source audio URL; upload local files to trusted storage before submitting.
- Set `continue_at` near the point where new music should begin.
- Use custom parameters when the user needs explicit lyrics, title, or style direction.
- Keep private recordings, lyrics, customer names, callback URLs, and generated audio URLs out of logs.
