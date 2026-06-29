# PoYo Kling 3.0 Turbo API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-3-0-turbo>
- Model page: <https://poyo.ai/models/kling-3-0-turbo>

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

- `kling-3.0-turbo/standard`
- `kling-3.0-turbo/pro`

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, optional when `multi_prompt` is used
- `multi_prompt` array, optional storyboard mode
- `image_urls` string array, optional, maximum one first-frame image
- `duration` integer, optional, three to fifteen seconds
- `aspect_ratio` string, optional for text-to-video: `16:9`, `9:16`, or `1:1`

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-3.0-turbo/standard",
    "input": {
      "prompt": "A precise tabletop video of a compact drone unfolding its arms, soft studio lighting, slow camera push-in, clean background",
      "duration": 5,
      "aspect_ratio": "16:9"
    }
  }'
```

## First-Frame Image-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-3.0-turbo/pro",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Start from the product photo. Add a smooth orbit camera move and natural reflection changes without changing the product identity",
      "image_urls": [
        "https://example.com/product-frame.png"
      ],
      "duration": 6
    }
  }'
```

## Multi-Shot Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-3.0-turbo/standard",
    "input": {
      "multi_prompt": [
        {
          "prompt": "A delivery robot rolls through a quiet lobby toward an elevator",
          "duration": 4
        },
        {
          "prompt": "The elevator doors open and warm light reflects on the robot shell",
          "duration": 4
        }
      ],
      "duration": 8,
      "aspect_ratio": "16:9"
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

- Use `prompt` for a single-shot request.
- Use `multi_prompt` when the user wants multiple shots or a compact storyboard.
- Include at most one `image_urls` item for a first-frame image-to-video request.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
