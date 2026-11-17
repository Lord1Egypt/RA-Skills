# PoYo Video Background Removal API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Model page: <https://poyo.ai/models/video-background-removal>

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

- `poyo-ai/video-background-removal`: removes the background from an existing hosted video.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

`input` fields:

- `video_url` string URI, required; must be a public HTTP or HTTPS URL
- `output_container_and_codec` string, optional; examples include WebM, MP4, MOV, MKV, and GIF-oriented outputs
- `preserve_audio` boolean, optional
- `background_color` string, optional; use `Transparent` when transparent compositing is required and the output format supports it

Always verify current field support on the PoYo model page before relying on model-specific options.

## Submit Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "poyo-ai/video-background-removal",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "video_url": "https://example.com/source-video.mp4",
      "output_container_and_codec": "webm_vp9",
      "preserve_audio": true,
      "background_color": "Transparent"
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
    "created_time": "2026-05-09T18:30:00"
  }
}
```

## Status Query Example

```bash
curl --fail-with-body --request GET \
  --url "https://api.poyo.ai/api/generate/status/task_unified_example" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

## Finished Result Shape

Successful tasks return video files in the standard PoYo task result shape:

```json
{
  "code": 200,
  "data": {
    "task_id": "task_unified_example",
    "status": "finished",
    "progress": 100,
    "files": [
      {
        "file_url": "https://cdn.poyo.ai/files/task_unified_example/output.webm",
        "file_type": "video"
      }
    ],
    "error_message": null
  }
}
```

## Practical Guidance

- Use a public source video URL; upload local files to trusted storage before submitting.
- Choose `Transparent` with a compatible output format when the next step is compositing.
- Decide `preserve_audio` before submission so downstream editors receive the intended track behavior.
- Save `data.task_id` immediately after submission.
- Use `callback_url` for production queues and longer user workflows.
- Avoid logging API keys, private video URLs, callback URLs, or generated output URLs.
