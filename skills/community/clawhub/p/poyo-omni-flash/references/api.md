# PoYo Omni Flash API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/omni-flash>
- Model page: <https://poyo.ai/models/omni-flash>

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

- `omni-flash`: text-to-video, image-to-video, reference image fusion, and video-input generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, optional, allowed counts are zero, one, or three
- `video_urls` string array, optional, at most one video
- `resolution` string, optional: `720p`, `1080p`, or `4k`
- `duration` integer, optional: `4`, `6`, `8`, or `10`; omit when `video_urls` is provided
- `aspect_ratio` string, optional: `16:9` or `9:16`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "omni-flash",
    "input": {
      "prompt": "A cinematic macro shot of a glass marble rolling across a wet reflective table, realistic physics, slow camera push-in",
      "resolution": "720p",
      "duration": 6,
      "aspect_ratio": "16:9"
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
    "model": "omni-flash",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Animate this product photo with a slow turntable motion, soft studio highlights, and subtle background parallax",
      "image_urls": [
        "https://example.com/source-image.webp"
      ],
      "resolution": "720p",
      "duration": 6,
      "aspect_ratio": "16:9"
    }
  }'
```

## Three-Image Reference Fusion Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "omni-flash",
    "input": {
      "prompt": "Combine the character, outfit, and set references into a single campaign clip with gentle camera drift",
      "image_urls": [
        "https://example.com/character.webp",
        "https://example.com/outfit.webp",
        "https://example.com/set.webp"
      ],
      "resolution": "1080p",
      "duration": 8,
      "aspect_ratio": "9:16"
    }
  }'
```

## Video-Input Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "omni-flash",
    "input": {
      "prompt": "Use the source video timing and transform the final look into a clean cinematic product reveal",
      "video_urls": [
        "https://example.com/source-video.mp4"
      ],
      "resolution": "720p",
      "aspect_ratio": "16:9"
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

- Omit both `image_urls` and `video_urls` for text-to-video.
- Use exactly one image for image-to-video.
- Use exactly three images for reference fusion.
- Use at most one video in `video_urls`, and omit `duration` when video input is used.
- Avoid logging API keys, private prompts, private source media URLs, or callback URLs.
