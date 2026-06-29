# PoYo Wan Animate API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/wan-animate>
- Model page: <https://poyo.ai/models/wan-animate>

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

- `wan-animate-replace`: character replacement workflow.
- `wan-animate-move`: character animation workflow.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `video_url` string URI, required, source video URL
- `image_urls` string array, required, exactly one target image
- `resolution` string, optional: `480p`, `580p`, or `720p`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Character Replacement Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "wan-animate-replace",
    "input": {
      "video_url": "https://example.com/source-video.mp4",
      "image_urls": [
        "https://example.com/target-character.jpg"
      ],
      "resolution": "480p"
    }
  }'
```

## Character Animation Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "wan-animate-move",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "video_url": "https://example.com/motion-reference.mp4",
      "image_urls": [
        "https://example.com/character-image.jpg"
      ],
      "resolution": "720p"
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
    "created_time": "2026-05-23T08:00:00"
  }
}
```

## Polling Notes

- Save `data.task_id` immediately after submission.
- Poll the status endpoint for local tests.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states.
- Store final video URLs only after the task reaches a terminal success state.

## Practical Guidance

- Use `wan-animate-replace` when the source video should keep the scene while replacing the character.
- Use `wan-animate-move` when the target image should be animated using the source video.
- Provide exactly one target image in `image_urls`.
- Keep private likeness images and private videos out of logs, screenshots, and repositories.
- Avoid logging API keys, private prompts, private source media URLs, or callback URLs.
