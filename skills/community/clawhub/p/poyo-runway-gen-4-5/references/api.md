# PoYo Runway Gen-4.5 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/runway-gen-4-5>
- Model page: <https://poyo.ai/models/runway-gen-4-5>

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

- `runway-gen-4.5`: text-to-video generation with optional single-image guidance.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `duration` integer, optional: `5` or `10`
- `aspect_ratio` string, optional: `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, or `21:9`
- `image_urls` string array, optional, maximum one image
- `seed` integer, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "runway-gen-4.5",
    "input": {
      "prompt": "A dense miniature jungle made of tiny colorful building blocks, a bright chameleon moves through the scene, shallow depth of field, smooth cinematic camera",
      "duration": 5,
      "aspect_ratio": "16:9"
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
    "model": "runway-gen-4.5",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Use the product photo as the opening frame. Add a slow orbit camera move, soft reflections, and subtle studio lighting changes",
      "duration": 10,
      "aspect_ratio": "16:9",
      "image_urls": [
        "https://example.com/product-reference.png"
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

- Use no `image_urls` for pure text-to-video.
- Use a single reference image only when the request depends on a source frame or product image.
- Match `aspect_ratio` to the destination surface.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
