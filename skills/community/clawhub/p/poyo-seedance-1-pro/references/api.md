# PoYo Seedance 1.0 Pro API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: use the standard PoYo task status endpoint documented by PoYo.
- Source docs: <https://docs.poyo.ai/api-manual/video-series/seedance-1.0-pro>
- Model page: <https://poyo.ai/models/seedance-1-pro>

## External Sharing Notice

Submitting a request sends the reviewed JSON payload to PoYo. That payload can include prompts, source image URLs, callback URLs, and generation settings. Do not include secrets, personal data, internal-only URLs, proprietary media, or confidential prompts unless the user accepts PoYo as the external processor.

Use only HTTPS callback URLs that the user controls. Do not submit private network URLs, localhost URLs, or callback endpoints that expose internal systems.

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

- `seedance-1.0-pro`: text-to-video and image-to-video video generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` array of image URLs, optional for image-to-video
- `resolution` string, optional, commonly `720p` or `1080p`
- `duration` integer, optional, commonly `5` or `10`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer $POYO_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "seedance-1.0-pro",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Slow zoom over a glowing mountain temple at dawn with soft mist and cinematic camera motion",
      "resolution": "720p",
      "duration": 5
    }
  }'
```

## Image-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer $POYO_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "seedance-1.0-pro",
    "input": {
      "prompt": "Animate the product with a smooth turntable camera move and gentle studio reflections",
      "image_urls": ["https://example.com/product.png"],
      "resolution": "1080p",
      "duration": 5
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
