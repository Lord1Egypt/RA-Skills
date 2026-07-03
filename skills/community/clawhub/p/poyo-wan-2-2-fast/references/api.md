# PoYo Wan 2.2 Fast API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: use the standard PoYo task status endpoint documented by PoYo.
- Text-to-video docs: <https://docs.poyo.ai/api-manual/video-series/wan2.2-text-to-video-fast>
- Image-to-video docs: <https://docs.poyo.ai/api-manual/video-series/wan2.2-image-to-video-fast>
- Model page: <https://poyo.ai/models/wan-2-2-fast>

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

- `wan2.2-text-to-video-fast`: text prompt to video.
- `wan2.2-image-to-video-fast`: animate one required image and optionally use a second image as the last frame.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `aspect_ratio` string, optional for text-to-video: `16:9` or `9:16`
- `image_urls` string array, required for image-to-video, one or two URLs
- `resolution` string, optional: `480p` or `720p`
- `seed` integer, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "wan2.2-text-to-video-fast",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "A cinematic product reveal with rain reflections and slow camera movement",
      "aspect_ratio": "16:9",
      "resolution": "720p",
      "seed": 123
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
    "model": "wan2.2-image-to-video-fast",
    "input": {
      "prompt": "Animate the image with a gentle push-in and natural background motion",
      "image_urls": [
        "https://example.com/start-image.jpg"
      ],
      "resolution": "480p",
      "seed": 224
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

- Use `wan2.2-text-to-video-fast` when the user has only a prompt.
- Use `wan2.2-image-to-video-fast` when one or two source images are available.
- Use two `image_urls` only when the user wants last-frame guidance.
- Avoid logging API keys, private prompts, private media URLs, task ids, or callback URLs.
