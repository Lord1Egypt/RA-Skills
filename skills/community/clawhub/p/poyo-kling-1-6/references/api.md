# PoYo Kling 1.6 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-1-6>
- Model page: <https://poyo.ai/models/kling-1-6>

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

- `kling-1.6/standard`: Standard text-to-video, image-to-video, and element reference workflows.
- `kling-1.6/pro`: Pro text-to-video, image-to-video, first/last-frame, and element reference workflows.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `duration` integer, required: `5` or `10`
- `aspect_ratio` string, optional: `1:1`, `16:9`, or `9:16`
- `negative_prompt` string, optional
- `cfg_scale` number, optional, zero to one, not supported when `image_urls` is provided
- `start_image_url` string, optional for image-to-video
- `end_image_url` string, optional for Pro image-to-video and requires `start_image_url`
- `image_urls` string array, optional for element reference workflows, one to four images

Do not combine `image_urls` with `start_image_url`, `end_image_url`, or `cfg_scale`. Always verify current field support in the PoYo docs before relying on model-specific options.

## Standard Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-1.6/standard",
    "input": {
      "prompt": "A quiet city street after rain, soft reflections on the pavement as the camera slowly moves forward",
      "duration": 5,
      "aspect_ratio": "16:9",
      "negative_prompt": "blur, low quality, flicker",
      "cfg_scale": 0.5
    }
  }'
```

## Pro Image-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-1.6/pro",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "A still indoor scene gently animates as warm afternoon light moves across the room",
      "duration": 10,
      "aspect_ratio": "16:9",
      "start_image_url": "https://example.com/start-frame.png",
      "end_image_url": "https://example.com/end-frame.png",
      "negative_prompt": "warped face, flicker, artifacts",
      "cfg_scale": 0.4
    }
  }'
```

## Element Reference Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-1.6/pro",
    "input": {
      "prompt": "Four reference objects form a calm tabletop scene while their shapes and materials stay consistent",
      "duration": 5,
      "aspect_ratio": "9:16",
      "image_urls": [
        "https://example.com/reference-1.png",
        "https://example.com/reference-2.png"
      ]
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
    "created_time": "2026-06-27T08:00:00"
  }
}
```

## Polling Notes

- Save `data.task_id` immediately after submission.
- Poll the status endpoint for local tests.
- Use `callback_url` for production queues and long-running user workflows.
- Treat terminal success and failure states as the points where the workflow should stop polling.
- Store final media URLs only after the task reaches a terminal success state.

## Practical Guidance

- Use Standard for simpler text, first-frame, or element-reference requests.
- Use Pro when the user needs Pro routing or first/last-frame image-to-video.
- Use `image_urls` only for element reference workflows.
- Use `cfg_scale` only when the selected workflow supports it.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
