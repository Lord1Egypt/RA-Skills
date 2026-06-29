# PoYo Kling 3.0 4K API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-3-0-4k>
- Model page: <https://poyo.ai/models/kling-3-0-4k>

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

- `kling-3.0/4K`: Kling 3.0 4K video generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required when `multi_shots` is false
- `image_urls` string array, optional, start frame and optional end frame
- `duration` integer, required, three to fifteen seconds
- `multi_shots` boolean, required
- `multi_prompt` array, required when `multi_shots` is true
- `sound` boolean, required
- `kling_elements` array, optional when supported by the workflow

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-3.0/4K",
    "input": {
      "prompt": "A high-detail city sunrise timelapse from a rooftop garden, realistic glass reflections, slow camera glide, cinematic light",
      "multi_shots": false,
      "duration": 5,
      "sound": true
    }
  }'
```

## Image-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-3.0/4K",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Start from the product frame and create a smooth cinematic push-in with realistic reflections and subtle background motion",
      "image_urls": [
        "https://example.com/start-frame.png",
        "https://example.com/end-frame.png"
      ],
      "multi_shots": false,
      "duration": 8,
      "sound": true
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
    "model": "kling-3.0/4K",
    "input": {
      "multi_shots": true,
      "multi_prompt": [
        {
          "prompt": "A camera descends over a quiet coastal road at dawn",
          "duration": 4
        },
        {
          "prompt": "A silver electric car enters the frame and follows the road beside the water",
          "duration": 5
        }
      ],
      "duration": 9,
      "sound": true
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

- Use `multi_shots: false` with `prompt` for single-shot requests.
- Use `multi_shots: true` with `multi_prompt` for storyboard requests.
- Include up to two images in `image_urls` when using start-frame and end-frame workflows.
- Keep `sound` explicit in payloads because it is part of the documented schema.
- Avoid logging API keys, private prompts, private source image URLs, or callback URLs.
