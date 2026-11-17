# PoYo Create Music Video API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/create-music-video>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/create-music-video.json>
- Model page: <https://poyo.ai/models/create-music-video>

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

- `create-music-video`: generate a visualized music video from an existing music task and audio track.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, required by the documented schema
- `input` object, required

Required `input` fields:

- `task_id` string
- `audio_id` string

Optional `input` fields:

- `author` string
- `domain_name` string

Always verify current field support in the PoYo docs before relying on model-specific options.

## Submit Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "create-music-video",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "task_id": "music_task_example",
      "audio_id": "audio_track_example",
      "author": "Studio Demo",
      "domain_name": "music.example.com"
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

- Use a completed source music task id and a matching audio identifier.
- Keep the callback endpoint server-side and ready to handle asynchronous completion events.
- If PoYo reports that a video already exists for the same source, retrieve the existing result instead of resubmitting the same request.
- Save `data.task_id` immediately after submission.
- Keep private prompts, task ids, audio identifiers, callback URLs, and generated media URLs out of logs.
