# PoYo Kling 2.5 Turbo Pro API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-2-5-turbo-pro>
- Model page: <https://poyo.ai/models/kling-2-5-turbo-pro>

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

- `kling-2.5-turbo-pro`: text-to-video and frame-guided video generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `duration` integer, optional: `5` or `10`
- `start_image_url` string, optional
- `end_image_url` string, optional
- `aspect_ratio` string, optional
- `negative_prompt` string, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-2.5-turbo-pro",
    "input": {
      "prompt": "A handheld follow shot of a traveler walking through a rainy neon street at night, reflective pavement, cinematic motion, crisp subject focus",
      "duration": 5,
      "aspect_ratio": "16:9",
      "negative_prompt": "blur, low quality, flicker"
    }
  }'
```

## First-Frame Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-2.5-turbo-pro",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Animate the product hero image with a slow camera push, subtle background parallax, and realistic studio light movement",
      "duration": 5,
      "aspect_ratio": "1:1",
      "start_image_url": "https://example.com/start-frame.png",
      "negative_prompt": "distorted logo, flicker, artifacts"
    }
  }'
```

## First/Last-Frame Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-2.5-turbo-pro",
    "input": {
      "prompt": "Create a smooth cinematic transition from the opening product scene to the final packaging scene",
      "duration": 10,
      "aspect_ratio": "16:9",
      "start_image_url": "https://example.com/start-frame.png",
      "end_image_url": "https://example.com/end-frame.png",
      "negative_prompt": "warped text, low quality"
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

- Use text-only requests when no first frame is needed.
- Use `start_image_url` when the first frame should anchor the output.
- Use both `start_image_url` and `end_image_url` when the final composition matters.
- Keep prompts concise and specific about subject motion, camera movement, and visual change.
- Avoid logging API keys, private prompts, private source image URLs, generated media URLs, or callback URLs.
