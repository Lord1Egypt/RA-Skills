# PoYo Hailuo 2.3 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/hailuo-2-3>
- Model page: <https://poyo.ai/models/hailuo-2-3>

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

- `hailuo-2.3`: text-to-video with optional first-frame image guidance.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `duration` integer, optional: `6` or `10`
- `resolution` string, optional: `768p` or `1080p`
- `start_image_url` string URI, optional
- `prompt_optimizer` boolean, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "hailuo-2.3",
    "input": {
      "prompt": "A compact delivery robot gliding through a bright indoor market, smooth handheld camera movement, natural light and subtle reflections",
      "duration": 6,
      "resolution": "768p",
      "prompt_optimizer": true
    }
  }'
```

## First-Frame Guided Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "hailuo-2.3",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Use the source frame as the first frame. Add a slow camera push-in and gentle environmental motion while preserving the subject",
      "duration": 6,
      "resolution": "1080p",
      "start_image_url": "https://example.com/start-frame.png",
      "prompt_optimizer": true
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

- Use prompt-only mode when the user does not provide a source frame.
- Use `start_image_url` only when the request depends on a first frame.
- Check duration and resolution combinations in the current docs before submitting.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
