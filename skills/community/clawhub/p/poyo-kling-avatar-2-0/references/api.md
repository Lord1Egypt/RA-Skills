# PoYo Kling Avatar 2.0 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-avatar-2-0>
- Model page: <https://poyo.ai/models/kling-avatar-2-0>

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

- `kling-avatar-2.0/standard`
- `kling-avatar-2.0/pro`

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `image_urls` string array, required, exactly one avatar reference image
- `audio_url` string URI, required, driving audio URL
- `prompt` string, optional avatar video guidance

Always verify current field support in the PoYo docs before relying on model-specific options.

## Standard Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-avatar-2.0/standard",
    "input": {
      "image_urls": [
        "https://example.com/avatar.png"
      ],
      "audio_url": "https://example.com/voice.mp3",
      "prompt": "A natural talking avatar facing the camera with calm expression and steady posture"
    }
  }'
```

## Pro Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-avatar-2.0/pro",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "image_urls": [
        "https://example.com/avatar.png"
      ],
      "audio_url": "https://example.com/voice.mp3"
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

- Provide exactly one image in `image_urls`.
- Provide one reachable `audio_url` for the driving audio.
- Keep private likeness images and private audio out of logs, screenshots, and repositories.
- Avoid logging API keys, private prompts, private source media URLs, or callback URLs.
