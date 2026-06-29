# PoYo Seedance 2.0 Mini API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/seedance-2-mini>
- Model page: <https://poyo.ai/models/seedance-2-mini>

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

- `seedance-2-mini`: text-to-video, image-to-video, first/last-frame, and multimodal reference video generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, optional for first-frame or first/last-frame workflows, up to two images
- `reference_image_urls` string array, optional for reference-to-video workflows, up to nine images
- `reference_video_urls` string array, optional for reference-to-video workflows, up to three videos
- `reference_audio_urls` string array, optional for reference-to-video workflows, up to three audio files
- `resolution` string, optional: `480p` or `720p`
- `aspect_ratio` string, optional: `auto`, `16:9`, `9:16`, `1:1`, `21:9`, `4:3`, or `3:4`
- `duration` integer, optional, four to fifteen seconds
- `generate_audio` boolean, optional
- `seed` integer, optional

Do not combine `image_urls` with `reference_image_urls`, `reference_video_urls`, or `reference_audio_urls` in the same request. Keep the total reference file count within the documented limit. Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "seedance-2-mini",
    "input": {
      "prompt": "A side tracking shot follows a courier sprinting through a bright market street, dynamic motion, natural daylight, crisp social video pacing",
      "resolution": "720p",
      "aspect_ratio": "9:16",
      "duration": 8,
      "generate_audio": false,
      "seed": 42
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
    "model": "seedance-2-mini",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Create a smooth transition from the first product frame to the final package frame with clean studio lighting",
      "image_urls": [
        "https://example.com/first-frame.png",
        "https://example.com/last-frame.png"
      ],
      "resolution": "720p",
      "aspect_ratio": "1:1",
      "duration": 6,
      "generate_audio": false
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
    "model": "seedance-2-mini",
    "input": {
      "prompt": "Use the reference images for styling and the reference clip for motion rhythm. Produce a concise vertical product teaser",
      "reference_image_urls": [
        "https://example.com/style-reference.png"
      ],
      "reference_video_urls": [
        "https://example.com/motion-reference.mp4"
      ],
      "resolution": "720p",
      "aspect_ratio": "9:16",
      "duration": 8,
      "generate_audio": true
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

- Use text-to-video when no source or reference media is needed.
- Use `image_urls` for first-frame or first/last-frame control.
- Use reference fields when style, character, motion, or audio references should guide the output.
- Pick resolution, aspect ratio, and duration before submission so the payload matches the delivery surface.
- Avoid logging API keys, private prompts, private media URLs, or callback URLs.
