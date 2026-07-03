# PoYo Video Translator API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Model page: <https://poyo.ai/models/video-translator>

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

- `poyo-ai/video-translator`: video translation through PoYo's async generation workflow.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `video_urls` string array, required
- `source_language` string, required
- `target_language` string, required

Always verify current field support on the PoYo model page before relying on model-specific options.

## Submission Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "poyo-ai/video-translator",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "video_urls": [
        "https://example.com/source-video.mp4"
      ],
      "source_language": "en",
      "target_language": "ja"
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
    "created_time": "2026-05-29T08:00:00"
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

- Use a public video or audio URL that PoYo can fetch.
- Set `source_language` explicitly for video translation.
- Set `target_language` explicitly.
- Save `data.task_id` immediately after submission.
- Use `callback_url` for production queues and longer user workflows.
- Finished results may include translated video files and subtitle files.
- Avoid logging API keys, private media, private media URLs, callback URLs, or generated output URLs.
