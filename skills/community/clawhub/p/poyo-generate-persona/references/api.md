# PoYo Generate Persona API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Source docs: <https://docs.poyo.ai/api-manual/music-series/generate-persona>
- Music detail docs: <https://docs.poyo.ai/api-manual/music-series/query-music-detail>
- Model page: <https://poyo.ai/models/generate-persona>

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

- `generate-persona`

## Prerequisites

Persona creation uses a specific track from an eligible completed music task.

- `task_id`: completed music task id from a supported PoYo music workflow
- `audio_id`: track id returned for the selected audio result

The current documentation lists Generate Music, Extend Music, Upload and Cover Audio, and Upload and Extend Audio as eligible source workflows. Verify the current list before submission.

## Request Schema

Top-level fields:

- `model` string, required and must be `generate-persona`
- `callback_url` string URI, optional
- `input` object, required

Required `input` fields:

- `task_id` string
- `audio_id` string
- `name` string
- `description` string

The description should capture useful musical characteristics such as genre, mood, instrumentation, vocal style, and distinctive traits.

## Submit Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "generate-persona",
    "callback_url": "https://example.com/api/poyo/music-webhook",
    "input": {
      "task_id": "completed_music_task_id",
      "audio_id": "selected_audio_track_id",
      "name": "Late Night Jazz Vocal",
      "description": "Intimate late-night jazz with mellow piano, upright bass, brushed drums, and a warm restrained vocal delivery."
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
    "created_time": "2026-07-20T08:00:00"
  }
}
```

## Result Retrieval

- Save `data.task_id` immediately after submission.
- If `callback_url` is present, verify webhook signatures according to current PoYo webhook documentation.
- Otherwise query the unified music detail endpoint documented by PoYo.
- The completed result can include a `persona_id` for supported follow-up music endpoints.

## Conflict Handling

Each audio track can have only one persona. A repeated request can return HTTP/code `409` indicating that a persona already exists for the audio. Do not retry that response blindly; retrieve or reuse the existing persona information when available.

## Practical Guidance

- Confirm the source task is complete before submitting persona creation.
- Match `audio_id` to the intended track when a music task returned multiple tracks.
- Write a specific reusable description rather than a vague label.
- Confirm the user has rights to process and reuse the source audio characteristics.
- Avoid logging API keys, private task ids, private audio ids, source audio URLs, callback URLs, or returned persona ids.
