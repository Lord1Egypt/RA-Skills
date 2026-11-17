# PoYo MiniMax Music 2.6 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/minimax-music-2.6>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/minimax-music-2.6.json>
- Model page: <https://poyo.ai/models/minimax-music-2-6>

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

- `minimax-music-2.6`: complete music generation with lyrics, optimized lyrics, or instrumental mode.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Required `input` fields:

- `prompt` string, required

Optional `input` fields:

- `lyrics` string
- `lyrics_optimizer` boolean
- `is_instrumental` boolean
- `audio_setting` object
- `audio_setting.sample_rate` number; documented values include `16000`, `24000`, `32000`, and `44100`
- `audio_setting.bitrate` number; documented values include `32000`, `64000`, `128000`, and `256000`
- `audio_setting.format` string; documented values include `mp3`, `wav`, and `pcm`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Vocal Track Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "minimax-music-2.6",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "City pop, warm synth bass, nostalgic night drive, clear vocal hook",
      "lyrics": "[Verse]\\nNeon lights fade behind the glass\\n[Chorus]\\nWe keep moving through the midnight",
      "is_instrumental": false,
      "audio_setting": {
        "sample_rate": 44100,
        "bitrate": 256000,
        "format": "mp3"
      }
    }
  }'
```

## Instrumental Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "minimax-music-2.6",
    "input": {
      "prompt": "Minimal piano and soft strings for a quiet sunrise over the ocean",
      "is_instrumental": true,
      "audio_setting": {
        "sample_rate": 32000,
        "bitrate": 128000,
        "format": "wav"
      }
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

## Status Query Example

```bash
curl --fail-with-body --request GET \
  --url "https://api.poyo.ai/api/generate/status/task_unified_example" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

## Practical Guidance

- Use `is_instrumental: true` for music without vocals.
- Use `lyrics_optimizer: true` only when the user wants a vocal track without exact lyrics.
- Provide `lyrics` when the user needs specific words in the vocal result.
- Save `data.task_id` immediately after submission.
- Use `callback_url` for production queues and longer user workflows.
- Keep private lyrics, customer prompts, callback URLs, and generated audio URLs out of logs.
