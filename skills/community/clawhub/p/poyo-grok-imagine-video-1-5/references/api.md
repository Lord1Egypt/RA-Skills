# PoYo Grok Imagine Video 1.5 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/grok-imagine-video-1-5>
- Model page: <https://poyo.ai/models/grok-imagine-video-1-5>

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

- `grok-imagine-video-1.5`: image-to-video generation from one source image.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, required, exactly one image
- `resolution` string, optional: `480p` or `720p`
- `duration` integer, optional, one to fifteen seconds

Always verify current field support in the PoYo docs before relying on model-specific options.

## Image-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "grok-imagine-video-1.5",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Turn the product photo into a smooth commercial clip with a slow camera push-in, soft studio lighting, and subtle reflection changes",
      "image_urls": [
        "https://example.com/source-image.png"
      ],
      "resolution": "720p",
      "duration": 6
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

- Provide exactly one source image in `image_urls`.
- Use public HTTPS image URLs or uploaded media URLs that PoYo can fetch.
- Match `resolution` and `duration` to the destination workflow before submission.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
