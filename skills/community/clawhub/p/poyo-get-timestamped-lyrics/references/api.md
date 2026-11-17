# PoYo Get Timestamped Lyrics API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/get-timestamped-lyrics>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/get-timestamped-lyrics.json>
- Model page: <https://poyo.ai/models/get-timestamped-lyrics>

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

- `get-timestamped-lyrics`: retrieve synchronized lyrics and timing data for a generated music track.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Required `input` fields:

- `task_id` string
- `audio_id` string

Always verify current field support in the PoYo docs before relying on model-specific options.

## Submit Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "get-timestamped-lyrics",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "task_id": "music_task_example",
      "audio_id": "audio_track_example"
    }
  }'
```

## Typical Timing Response

```json
{
  "code": 200,
  "data": {
    "aligned_words": [
      {
        "word": "[Verse]",
        "success": true,
        "start_s": 1.36,
        "end_s": 1.79
      }
    ],
    "waveform_data": [0, 1, 0.5, 0.75],
    "is_streamed": false
  }
}
```

## Status Query Example

```bash
curl --fail-with-body --request GET \
  --url "https://api.poyo.ai/api/generate/status/music_task_example" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

## Practical Guidance

- Use a completed source music task id and a matching audio identifier.
- Preserve lyric timing output exactly when the user needs subtitle, karaoke, or audio visualization workflows.
- Use `callback_url` for production queues and longer user workflows.
- Keep private lyrics, task ids, audio identifiers, callback URLs, and waveform data out of logs.
