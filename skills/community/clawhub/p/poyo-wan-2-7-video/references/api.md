# PoYo Wan 2.7 Video API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/wan-2-7-video>
- Model page: <https://poyo.ai/models/wan-2-7-video>

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

- `wan2.7-text-to-video`: text prompt to video.
- `wan2.7-image-to-video`: animate one or two input images.
- `wan2.7-reference-to-video`: reference-guided video from image or video references.
- `wan2.7-edit-video`: edit an existing video.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required for text, reference, and edit workflows
- `image_urls` string array, required for image-to-video
- `reference_image_urls` string array, optional for reference-to-video
- `reference_video_urls` string array, optional for reference-to-video
- `video_url` string, required for edit-video
- `reference_image_url` string, optional for edit-video
- `audio_url` string, optional
- `aspect_ratio` string, optional: `16:9`, `9:16`, `1:1`, `4:3`, or `3:4`
- `resolution` string, optional: `720p` or `1080p`
- `duration` integer, optional and workflow-dependent
- `multi_shots` boolean, optional
- `audio_setting` string, optional for edit-video
- `seed` integer, optional
- `enable_safety_checker` boolean, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "wan2.7-text-to-video",
    "input": {
      "prompt": "A cinematic tracking shot of a glass greenhouse at sunrise, soft light, slow camera movement",
      "aspect_ratio": "16:9",
      "resolution": "720p",
      "duration": 5
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
    "model": "wan2.7-image-to-video",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "image_urls": [
        "https://example.com/start-frame.png"
      ],
      "prompt": "Animate the frame with gentle wind and a slow push-in camera movement",
      "resolution": "1080p",
      "duration": 5
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
    "model": "wan2.7-reference-to-video",
    "input": {
      "prompt": "A product reveal video using the reference object, clean studio lighting, smooth motion",
      "reference_image_urls": [
        "https://example.com/reference.png"
      ],
      "aspect_ratio": "1:1",
      "resolution": "720p",
      "duration": 5,
      "multi_shots": false
    }
  }'
```

## Edit Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "wan2.7-edit-video",
    "input": {
      "prompt": "Change the scene into a rainy neon street while preserving the subject motion",
      "video_url": "https://example.com/source-video.mp4",
      "reference_image_url": "https://example.com/style-reference.png",
      "aspect_ratio": "16:9",
      "resolution": "720p",
      "duration": 0
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

- Choose the model id from the user's actual workflow rather than treating all Wan 2.7 requests as text-to-video.
- Use `image_urls` for first-frame or first/last-frame animation.
- Use reference media fields only when the user provides or requests reference-guided generation.
- Use edit-video only when a source `video_url` is available.
- Avoid logging API keys, private prompts, private source media URLs, or callback URLs.
