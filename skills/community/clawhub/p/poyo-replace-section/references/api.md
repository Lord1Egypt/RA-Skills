# PoYo Replace Section API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/replace-section>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/replace-section.json>
- Model page: <https://poyo.ai/models/replace-section>

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

- `replace-section`: replace a specific time range of an existing generated music track with new content.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Required `input` fields:

- `task_id` string
- `audio_id` string
- `prompt` string
- `tags` string
- `title` string
- `infill_start_s` number
- `infill_end_s` number
- `full_lyrics` string

Optional `input` fields:

- `negative_tags` string

Always verify current field support in the PoYo docs before relying on model-specific options.

## Submit Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "replace-section",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "task_id": "music_task_example",
      "audio_id": "audio_track_example",
      "prompt": "A brighter chorus with a clean vocal hook",
      "tags": "pop, upbeat",
      "title": "Edited Chorus",
      "infill_start_s": 30.0,
      "infill_end_s": 60.0,
      "full_lyrics": "Complete lyrics for the edited track"
    }
  }'
```

## Typical Submit Response

```json
{
  "code": 200,
  "data": {
    "task_id": "replacement_task_example",
    "status": "not_started",
    "created_time": "2026-07-09T08:00:00"
  }
}
```

## Status Query Example

```bash
curl --fail-with-body --request GET \
  --url "https://api.poyo.ai/api/generate/status/replacement_task_example" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

## Practical Guidance

- Use a completed source music task id and a matching audio identifier.
- Ensure `infill_end_s` is greater than `infill_start_s`.
- Keep the replacement range narrow enough for the intended edit.
- Save `data.task_id` immediately after submission.
- Use `callback_url` for production queues and longer user workflows.
- Keep private prompts, lyrics, task ids, audio identifiers, callback URLs, and generated file URLs out of logs.
