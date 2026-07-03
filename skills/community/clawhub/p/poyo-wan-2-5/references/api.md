# PoYo Wan 2.5 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: use the standard PoYo task status endpoint documented by PoYo.
- Text-to-video docs: <https://docs.poyo.ai/api-manual/video-series/wan2.5-text-to-video>
- Image-to-video docs: <https://docs.poyo.ai/api-manual/video-series/wan2.5-image-to-video>
- Model page: <https://poyo.ai/models/wan-2-5>

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

- `wan2.5-text-to-video`: text prompt to video.
- `wan2.5-image-to-video`: animate one input image.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `aspect_ratio` string, optional for text-to-video: `832*480`, `480*832`, `1280*720`, `720*1280`, `1920*1080`, or `1080*1920`
- `image_urls` string array, required for image-to-video, exactly one URL
- `resolution` string, optional for image-to-video: `480p`, `720p`, or `1080p`
- `duration` integer, optional: `5` or `10`
- `audio` string, optional
- `negative_prompt` string, optional
- `seed` integer, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "wan2.5-text-to-video",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "A cinematic time-lapse of a city street transitioning from day to night",
      "aspect_ratio": "1280*720",
      "duration": 5,
      "negative_prompt": "blur, low detail",
      "seed": 426
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
    "model": "wan2.5-image-to-video",
    "input": {
      "prompt": "A warm cinematic zoom-in with gentle background motion",
      "image_urls": [
        "https://example.com/image.jpg"
      ],
      "resolution": "720p",
      "duration": 5,
      "seed": 225
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

- Use `wan2.5-text-to-video` when the user has only a prompt.
- Use `wan2.5-image-to-video` when exactly one source image is available.
- Keep `audio` as a string if used; do not send a boolean.
- Avoid logging API keys, private prompts, private media URLs, task ids, or callback URLs.
