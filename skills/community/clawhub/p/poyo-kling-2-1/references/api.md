# PoYo Kling 2.1 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: use the standard PoYo task status endpoint documented by PoYo.
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-2-1>
- Model page: <https://poyo.ai/models/kling-2-1>

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

- `kling-2.1/standard`: start-frame guided image-to-video.
- `kling-2.1/pro`: start-frame guided image-to-video with optional end-frame guidance.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `start_image_url` string URI, required
- `duration` integer, optional: `5` or `10`
- `end_image_url` string URI, optional, only for `kling-2.1/pro`
- `negative_prompt` string, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Standard Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-2.1/standard",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Animate the scene with gentle camera motion, soft rain, and natural subject movement",
      "duration": 5,
      "start_image_url": "https://example.com/start-frame.png",
      "negative_prompt": "blur, low detail"
    }
  }'
```

## Pro End-Frame Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-2.1/pro",
    "input": {
      "prompt": "Create a smooth transition from the first frame to the final pose with cinematic motion",
      "duration": 10,
      "start_image_url": "https://example.com/start-frame.png",
      "end_image_url": "https://example.com/end-frame.png"
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
    "created_time": "2026-07-01T08:00:00"
  }
}
```

## Polling Notes

- Save `data.task_id` immediately after submission.
- Poll the standard PoYo task status endpoint for local tests.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states.
- Store final video URLs only after the task reaches a terminal success state.

## Practical Guidance

- Use Standard when the user only has one start frame.
- Use Pro when the user needs optional end-frame guidance.
- Do not send `end_image_url` with `kling-2.1/standard`.
- Avoid logging API keys, private prompts, private media URLs, task ids, or callback URLs.
