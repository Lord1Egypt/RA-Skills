# PoYo Kling 2.6 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: use the standard PoYo task status endpoint documented by PoYo.
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-2-6>
- Model page: <https://poyo.ai/models/kling-2-6>

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

- `kling-2.6`: text-to-video and image-to-video video generation with optional native audio.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `sound` boolean, optional
- `aspect_ratio` string, optional
- `duration` integer, optional, commonly `5` or `10`
- `image_urls` array of image URLs, optional for image-to-video

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer $POYO_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-2.6",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "A product founder walks through a bright studio while explaining a new device, with natural camera movement",
      "sound": true,
      "aspect_ratio": "16:9",
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
    "model": "kling-2.6",
    "input": {
      "prompt": "Animate the reference image into a calm cinematic scene with subtle camera drift and matching ambient sound",
      "image_urls": ["https://example.com/reference.png"],
      "sound": true,
      "aspect_ratio": "16:9",
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
