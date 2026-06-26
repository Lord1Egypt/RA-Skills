# PoYo Kling 3.0 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-3-0>
- Model page: <https://poyo.ai/models/kling-3-0>

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

- `kling-3.0/standard`: standard Kling 3.0 video generation.
- `kling-3.0/pro`: higher-detail Kling 3.0 video generation when the user explicitly asks for the pro model.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required when `multi_shots` is `false`
- `sound` boolean, required
- `multi_shots` boolean, required
- `duration` integer, required, normally 3 to 15 seconds
- `aspect_ratio` string, optional: `1:1`, `16:9`, or `9:16`
- `image_urls` string array, optional for image-to-video and required when `kling_elements` is used
- `multi_prompt` object array, required when `multi_shots` is `true`
- `kling_elements` object array, optional for reusable element references in prompts

Always verify current field support in the PoYo docs before relying on model-specific options.

## Single-Shot Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-3.0/standard",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "A chef carefully plating a gourmet dish in a modern kitchen, steam rising from the food under warm lighting",
      "multi_shots": false,
      "duration": 5,
      "sound": true,
      "aspect_ratio": "16:9"
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
    "model": "kling-3.0/pro",
    "input": {
      "multi_shots": true,
      "sound": true,
      "duration": 10,
      "aspect_ratio": "16:9",
      "multi_prompt": [
        {
          "prompt": "A wide establishing shot of a compact electric car entering a clean studio set",
          "duration": 5
        },
        {
          "prompt": "A smooth close-up tracking shot across the dashboard and ambient lighting",
          "duration": 5
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

- Use `image_urls` only when the task genuinely depends on reference imagery.
- Match aspect ratio to the destination surface: `1:1`, `16:9`, or `9:16`.
- When `multi_shots` is true, use `multi_prompt` and keep `sound` enabled.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
