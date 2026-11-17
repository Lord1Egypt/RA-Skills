# PoYo Convert to WAV API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/convert-to-wav>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/music-series/convert-to-wav.json>
- Model page: <https://poyo.ai/models/convert-to-wav>

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

- `convert-to-wav`: convert a generated PoYo music track to WAV format.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, required by the documented schema
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
    "model": "convert-to-wav",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "task_id": "music_task_example",
      "audio_id": "audio_track_example"
    }
  }'
```

## Typical Submit Response

```json
{
  "code": 200,
  "data": {
    "task_id": "conversion_task_example",
    "status": "not_started",
    "created_time": "2026-07-09T08:00:00"
  }
}
```

## Status Query Example

```bash
curl --fail-with-body --request GET \
  --url "https://api.poyo.ai/api/generate/status/conversion_task_example" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

## Practical Guidance

- Use a completed source music task id and a matching audio identifier.
- Keep the callback endpoint server-side and ready to handle asynchronous completion events.
- If PoYo reports that a WAV export already exists for the same audio, retrieve the existing result instead of resubmitting the same request.
- Save `data.task_id` immediately after submission.
- Keep private prompts, task ids, audio identifiers, callback URLs, and generated file URLs out of logs.
