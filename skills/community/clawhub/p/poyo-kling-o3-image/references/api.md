# PoYo Kling O3 Image API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/kling-o3>
- Model page: <https://poyo.ai/models/kling-o3-image>

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

- `kling-o3-image`: prompt-only image generation.
- `kling-o3-image-edit`: image editing with reference images.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, optional for edit workflows, one to ten images
- `elements` array, optional for subject or object control
- `resolution` string, optional: `1K`, `2K`, or `4K`
- `size` string, optional: `auto`, `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `3:2`, `2:3`, or `21:9`
- `output_format` string, optional: `jpeg`, `png`, or `webp`
- `n` integer, optional, one to nine images

Always verify current field support in the PoYo docs before relying on model-specific options.

## Prompt-Only Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-o3-image",
    "input": {
      "prompt": "A cinematic futuristic alley with rain and neon reflections, detailed storefronts, realistic wet pavement, dramatic night lighting",
      "resolution": "4K",
      "size": "16:9",
      "output_format": "png",
      "n": 2
    }
  }'
```

## Image Editing Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-o3-image-edit",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Keep the product identity from the reference image. Change the setting to a luxury night interior with dramatic window light",
      "image_urls": [
        "https://example.com/reference1.png"
      ],
      "resolution": "4K",
      "size": "auto",
      "output_format": "png",
      "n": 1
    }
  }'
```

## Element Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-o3-image-edit",
    "input": {
      "prompt": "Place @Element1 in a polished studio scene with soft reflection and a clean product backdrop",
      "image_urls": [
        "https://example.com/background-reference.png"
      ],
      "elements": [
        {
          "frontal_image_url": "https://example.com/product-front.png",
          "reference_image_urls": [
            "https://example.com/product-side.png"
          ]
        }
      ],
      "resolution": "2K",
      "size": "1:1",
      "output_format": "webp",
      "n": 1
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
- Store final image URLs only after the task reaches a terminal success state.

## Practical Guidance

- Use `kling-o3-image` when no reference image is needed.
- Use `kling-o3-image-edit` when source images guide the result.
- Use `elements` only when the request needs stronger subject or object consistency.
- Match `resolution`, `size`, and `output_format` to the destination workflow before submission.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
