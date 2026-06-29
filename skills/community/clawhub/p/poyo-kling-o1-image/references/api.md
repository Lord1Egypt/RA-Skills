# PoYo Kling O1 Image API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/image-series/kling-o1>
- Model page: <https://poyo.ai/models/kling-o1-image>

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

- `kling-o1-image-edit`: image editing with reference images and optional element guidance.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, required, one to ten images
- `elements` array, optional for subject or object control
- `resolution` string, optional: `1K` or `2K`
- `size` string, optional: `auto`, `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `3:2`, `2:3`, or `21:9`
- `output_format` string, optional: `jpeg`, `png`, or `webp`
- `n` integer, optional, one to nine images

Always verify current field support in the PoYo docs before relying on model-specific options.

## Reference Editing Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-o1-image-edit",
    "input": {
      "prompt": "Keep the product identity from the reference image. Move it into a clean studio scene with soft shadow and neutral background",
      "image_urls": [
        "https://example.com/product-reference.png"
      ],
      "resolution": "2K",
      "size": "1:1",
      "output_format": "png",
      "n": 1
    }
  }'
```

## Element-Guided Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-o1-image-edit",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Place @Element1 in a polished catalog scene with a subtle reflection, crisp edges, and realistic studio light",
      "image_urls": [
        "https://example.com/background-reference.png"
      ],
      "elements": [
        {
          "frontal_image_url": "https://example.com/object-front.png",
          "reference_image_urls": [
            "https://example.com/object-side.png"
          ]
        }
      ],
      "resolution": "2K",
      "size": "16:9",
      "output_format": "png",
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
    "created_time": "2026-06-26T08:00:00"
  }
}
```

## Polling Notes

- Save `data.task_id` immediately after submission.
- Poll the status endpoint for local tests.
- Use `callback_url` for production queues and long-running user workflows.
- Treat terminal success and failure states as the points where the workflow should stop polling.
- Store final image URLs only after the task reaches a terminal success state.

## Practical Guidance

- Use `kling-o1-image-edit` only when reference images are available.
- Use `elements` when the request needs stronger subject or object consistency.
- Match `resolution`, `size`, and `output_format` to the destination workflow before submission.
- Keep the prompt explicit about which references should be preserved and what should change.
- Avoid logging API keys, private prompts, private source image URLs, generated image URLs, or callback URLs.
