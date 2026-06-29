# PoYo Happy Horse 1.1 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/happy-horse-1-1>
- Model page: <https://poyo.ai/models/happy-horse-1-1>

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

- `happy-horse-1.1`: text-to-video, image-to-video, and reference-to-video.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required for text-to-video and reference-to-video
- `image_urls` string array, optional for image-to-video, exactly one first-frame image URL
- `reference_image_urls` string array, optional for reference-to-video, one to nine images
- `aspect_ratio` string, optional: `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `4:5`, `5:4`, `9:16`, or `9:21`
- `resolution` string, optional: `720p` or `1080p`
- `duration` integer, optional, three to fifteen seconds
- `seed` integer, optional, zero to 2147483647
- `enable_safety_checker` boolean, optional

Do not combine `image_urls` and `reference_image_urls` in the same request. Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "happy-horse-1.1",
    "input": {
      "prompt": "A compact delivery robot rolls through a bright modern warehouse, smooth cinematic camera movement, realistic lighting",
      "aspect_ratio": "16:9",
      "resolution": "720p",
      "duration": 8
    }
  }'
```

## Image-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "happy-horse-1.1",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Animate the product with a slow push-in camera move, soft studio reflections, and subtle background motion",
      "image_urls": [
        "https://example.com/product-frame.png"
      ],
      "aspect_ratio": "1:1",
      "resolution": "720p",
      "duration": 6
    }
  }'
```

## Reference-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "happy-horse-1.1",
    "input": {
      "prompt": "Create a short lifestyle video that preserves the wardrobe and color palette from the references, natural hand-held camera motion",
      "reference_image_urls": [
        "https://example.com/reference-1.png",
        "https://example.com/reference-2.png"
      ],
      "aspect_ratio": "9:16",
      "resolution": "720p",
      "duration": 8,
      "seed": 12345
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
    "created_time": "2026-06-26T08:00:00"
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

- Use text-to-video when the user has no source image.
- Use image-to-video when the first frame should anchor the output.
- Use reference-to-video only when the references describe the intended subject or visual direction.
- Pick aspect ratio and duration before submission so the payload matches the delivery surface.
- Avoid logging API keys, private prompts, private media URLs, or callback URLs.
