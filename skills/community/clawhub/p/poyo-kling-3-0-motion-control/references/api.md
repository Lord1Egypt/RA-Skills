# PoYo Kling 3.0 Motion Control API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-3-0-motion-control>
- Model page: <https://poyo.ai/models/kling-3-0-motion-control>

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

- `kling-3.0-motion-control`: motion-control video generation with one reference image and one reference video.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `image_urls` string array, required, exactly one image
- `video_urls` string array, required, exactly one video
- `character_orientation` string, required: `image` or `video`
- `prompt` string, optional
- `resolution` string, optional: `720p` or `1080p`
- `kling_elements` array, optional for supported element-reference workflows

Media guidance from the PoYo docs:

- Reference images should use supported image formats.
- Reference videos should use supported video formats.
- Video duration limits depend on `character_orientation`.
- For optional `kling_elements`, follow the docs for element image count and prompt references.

Always verify current field support in the PoYo docs before relying on model-specific options.

## Basic Motion-Control Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-3.0-motion-control",
    "input": {
      "image_urls": [
        "https://example.com/character-reference.png"
      ],
      "video_urls": [
        "https://example.com/motion-reference.mp4"
      ],
      "character_orientation": "image",
      "prompt": "Preserve the subject from the image while following the motion rhythm and camera movement from the reference video",
      "resolution": "720p"
    }
  }'
```

## Element Reference Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-3.0-motion-control",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "image_urls": [
        "https://example.com/main-reference.png"
      ],
      "video_urls": [
        "https://example.com/motion-reference.mp4"
      ],
      "character_orientation": "video",
      "prompt": "Use @Element1 as the visible handheld product while keeping the motion from the reference video natural",
      "resolution": "1080p",
      "kling_elements": [
        {
          "frontal_image_url": "https://example.com/product-front.png",
          "reference_image_urls": [
            "https://example.com/product-angle-a.png",
            "https://example.com/product-angle-b.png"
          ]
        }
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

- Confirm that the reference image and reference video are reachable before submission.
- Use `character_orientation: "image"` when the image should define the main character or subject.
- Use `character_orientation: "video"` when the video should define the main character orientation and motion.
- Include `kling_elements` only when the docs support it for the selected orientation.
- Avoid logging API keys, private prompts, private media URLs, or callback URLs.
