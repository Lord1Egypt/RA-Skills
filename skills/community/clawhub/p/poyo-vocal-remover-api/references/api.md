# PoYo Vocal Remover API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Music detail: `GET https://api.poyo.ai/api/generate/detail/music`
- Separate vocals docs: <https://docs.poyo.ai/api-manual/music-series/vocal-remover/separate-vocals>
- Stem split docs: <https://docs.poyo.ai/api-manual/music-series/vocal-remover/stem-split>
- Upload and separate docs: <https://docs.poyo.ai/api-manual/music-series/vocal-remover/upload-and-separate-vocals>
- Music detail docs: <https://docs.poyo.ai/api-manual/music-series/query-music-detail>
- Music webhook docs: <https://docs.poyo.ai/api-manual/music-series/music-webhook>
- Model page: <https://poyo.ai/models/vocal-remover-api>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Models

- `separate-vocals`: split vocals and accompaniment from a completed PoYo music result.
- `stem-split`: split a completed PoYo music result into multiple instrument stems.
- `upload-and-separate-vocals`: upload a public audio URL and separate it into stems.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional for upload-based separation and required by some existing-result separation docs
- `input` object, required

For `separate-vocals` and `stem-split`:

- `task_id` string, required; completed PoYo music task id
- `audio_id` string, required; specific audio track id from the music result

For `upload-and-separate-vocals`:

- `audio_url` string URI, required; public audio URL
- `title` string, optional
- `model_name` string, optional; supported values include `base`, `enhanced`, and `instrumental`
- `output_type` string, optional; supported values include `general`, `bass`, `drums`, `other`, `piano`, `guitar`, and `vocals`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Upload and Separate Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "upload-and-separate-vocals",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "title": "Demo Track Separation",
      "audio_url": "https://example.com/audio/demo-track.mp3",
      "model_name": "base",
      "output_type": "general"
    }
  }'
```

## Existing Music Result Example

Use this when the user already has a completed PoYo music result with both `task_id` and `audio_id`.

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "separate-vocals",
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
    "task_id": "task_unified_example",
    "status": "not_started",
    "created_time": "2026-07-06T08:00:00"
  }
}
```

## Result Retrieval Notes

- Save `data.task_id` immediately after submission.
- Use the music detail endpoint for task results and returned stem URLs.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states when receiving callbacks.
- Download returned audio files before relying on them long term.

## Practical Guidance

- Use `upload-and-separate-vocals` when the user only has a source audio URL.
- Use `separate-vocals` or `stem-split` when the user is continuing from a completed PoYo music task.
- Choose a narrow `output_type` if the user only needs one stem.
- Keep private recordings, customer names, callback URLs, task ids, audio ids, and generated stem URLs out of logs.
