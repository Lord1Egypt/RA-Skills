# PoYo Upload and Cover Audio API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Music detail: `GET https://api.poyo.ai/api/generate/detail/music`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/upload-and-cover-audio>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/upload-and-cover-audio.json>
- Music detail docs: <https://docs.poyo.ai/api-manual/music-series/query-music-detail>
- Music webhook docs: <https://docs.poyo.ai/api-manual/music-series/music-webhook>
- Model page: <https://poyo.ai/models/upload-and-cover-audio>

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

- `upload-and-cover-audio`: transforms uploaded audio into a new music style.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `upload_url` string URI, required
- `prompt` string, required depending on mode
- `custom_mode` boolean, required
- `instrumental` boolean, required
- `mv` string, required by the current docs
- `style` string, required in custom mode
- `title` string, required in custom mode
- `negative_tags` string, optional
- `vocal_gender` string, optional
- `style_weight` number, optional
- `weirdness_constraint` number, optional
- `audio_weight` number, optional
- `persona_id` string, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Simple Mode Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "upload-and-cover-audio",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "upload_url": "https://example.com/audio/source-track.mp3",
      "prompt": "Create a bright jazz version of this track",
      "custom_mode": false,
      "instrumental": false,
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
    "model": "upload-and-cover-audio",
    "input": {
      "upload_url": "https://example.com/audio/source-track.mp3",
      "prompt": "Transform the song into a clean electronic version",
      "style": "electronic, polished, bright",
      "title": "Neon Cover",
      "custom_mode": true,
      "instrumental": false,
      "mv": "V5",
      "negative_tags": "harsh noise, muddy mix",
      "style_weight": 0.7
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
- Use simple mode for quick transformations and custom mode when title and style control matter.
- Keep private recordings, lyrics, customer names, callback URLs, and generated audio URLs out of logs.
