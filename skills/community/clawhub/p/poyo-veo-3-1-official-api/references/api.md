# PoYo Veo 3.1 Official API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/veo-3-1-official>
- Model page: <https://poyo.ai/models/veo-3-1-official>

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

- `veo3.1-fast-official`: fast official generation.
- `veo3.1-lite-official`: lite official generation.
- `veo3.1-quality-official`: quality official generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, optional
- `generation_type` string, optional: `frame` or `reference`
- `duration` integer, optional
- `aspect_ratio` string, optional: `auto`, `16:9`, or `9:16`
- `resolution` string, optional: `720p`, `1080p`, or `4k` where supported
- `sound` boolean, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "veo3.1-fast-official",
    "input": {
      "prompt": "A cinematic close-up of a paper boat drifting through a neon-lit canal, gentle camera movement, reflective water",
      "duration": 6,
      "aspect_ratio": "16:9",
      "resolution": "1080p",
      "sound": true
    }
  }'
```

## Image-Guided Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "veo3.1-lite-official",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "The product rotates slowly on a clean studio table with soft shadows and restrained camera motion",
      "duration": 8,
      "aspect_ratio": "auto",
      "resolution": "720p",
      "sound": false,
      "image_urls": [
        "https://example.com/product-start.jpg"
      ]
    }
  }'
```

## Reference Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "veo3.1-quality-official",
    "input": {
      "prompt": "A polished campaign video with consistent subject appearance and smooth editorial motion",
      "duration": 8,
      "aspect_ratio": "9:16",
      "resolution": "4k",
      "sound": true,
      "generation_type": "reference",
      "image_urls": [
        "https://example.com/reference-1.jpg",
        "https://example.com/reference-2.jpg",
        "https://example.com/reference-3.jpg"
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
    "created_time": "2026-05-18T10:30:00"
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

- Use no `image_urls` for text-to-video.
- Use one image for image-to-video and two images for first/last-frame workflows.
- Use `generation_type: "reference"` only with supported models and the required image count.
- Use `sound: false` when the user wants silent output.
- Avoid logging API keys, private prompts, private source media URLs, or callback URLs.
