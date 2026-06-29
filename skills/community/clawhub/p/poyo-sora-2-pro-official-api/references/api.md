# PoYo Sora 2 Pro Official API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/sora-2-pro-official>
- Model page: <https://poyo.ai/models/sora-2-pro-official>

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

- `sora-2-pro-official`: text-to-video generation with optional single-image guidance.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, optional, maximum one image
- `aspect_ratio` string, optional: `16:9` or `9:16` for text-to-video; `auto`, `16:9`, or `9:16` for image-guided video
- `duration` integer, optional: `4`, `8`, `12`, `16`, or `20`
- `resolution` string, optional: `720p`, `1024p`, or `1080p`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "sora-2-pro-official",
    "input": {
      "prompt": "A precise macro video of a watch movement assembling itself on a dark workbench, clean reflections, controlled camera glide, realistic metal detail",
      "aspect_ratio": "16:9",
      "duration": 8,
      "resolution": "1080p"
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
    "model": "sora-2-pro-official",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Start from the product photo. Create a slow tabletop reveal with realistic reflections, subtle depth of field, and a clean commercial lighting setup",
      "image_urls": [
        "https://example.com/product-reference.png"
      ],
      "aspect_ratio": "auto",
      "duration": 12,
      "resolution": "1024p"
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
- Use `aspect_ratio: "auto"` only for image-guided workflows where the source image should guide framing.
- Match `duration` and `resolution` to the destination workflow before submission.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
