# PoYo Sora 2 Official API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/sora-2-official>
- Model page: <https://poyo.ai/models/sora-2-official>
- Example repository: <https://github.com/PoyoAPI/sora-2-official-api>

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

- `sora-2-official`: text-to-video with optional single-image guided video.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `duration` integer, optional: `4`, `8`, `12`, `16`, or `20`
- `aspect_ratio` string, optional: `16:9` or `9:16`
- `image_urls` string array, optional, maximum one image

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "sora-2-official",
    "input": {
      "prompt": "A cinematic launch scene for a tiny autonomous delivery robot crossing a quiet city plaza at sunrise, soft reflections on wet pavement, gentle camera tracking",
      "duration": 8,
      "aspect_ratio": "16:9"
    }
  }'
```

## Image-Guided Example

Use `image_urls` when the user wants the video to start from or follow a reference frame.

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "sora-2-official",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Use the reference image as the opening frame. Animate a subtle camera push-in, preserve the main object and lighting, add realistic background movement",
      "duration": 8,
      "aspect_ratio": "16:9",
      "image_urls": [
        "https://example.com/reference-frame.png"
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
- Store final file URLs only after the task reaches a terminal success state.

## Practical Guidance

- Use `16:9` for landscape video and `9:16` for mobile-first output.
- Use `image_urls` only when the request truly depends on one reference image.
- Validate source image URLs before submitting payloads.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
