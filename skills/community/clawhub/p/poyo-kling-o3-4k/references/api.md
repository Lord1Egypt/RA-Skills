# PoYo Kling O3 4K API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/kling-o3-4k>
- Model page: <https://poyo.ai/models/kling-o3-4k>

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

- `kling-o3/4K`: Kling O3 4K video generation.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required when `multi_shots` is false
- `image_urls` string array, optional, up to two primary image anchors
- `reference_image_urls` string array, optional, up to four reference images
- `duration` integer, required, three to fifteen seconds
- `multi_shots` boolean, required
- `multi_prompt` array, required when `multi_shots` is true
- `sound` boolean, required
- `aspect_ratio` string, optional: `1:1`, `16:9`, or `9:16`
- `kling_elements` array, optional for supported reference-to-video workflows

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-o3/4K",
    "input": {
      "prompt": "A high-detail night city product reveal on a rooftop, realistic glass reflections, slow camera glide, clean cinematic lighting",
      "multi_shots": false,
      "duration": 5,
      "sound": true,
      "aspect_ratio": "16:9"
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
    "model": "kling-o3/4K",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Create a smooth high-detail product reveal from the start frame to the end frame with natural reflection changes",
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

## Reference-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kling-o3/4K",
    "input": {
      "prompt": "Use the references for product identity and set styling. Create a premium launch clip with a slow orbit camera move",
      "reference_image_urls": [
        "https://example.com/product-reference.png",
        "https://example.com/set-reference.png"
      ],
      "multi_shots": false,
      "duration": 6,
      "sound": true,
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

- Use `multi_shots: false` with `prompt` for single-shot requests.
- Use `multi_shots: true` with `multi_prompt` for storyboard requests.
- Use `reference_image_urls` only when the request depends on visual references beyond start and end anchors.
- Keep `sound` explicit in payloads because it is part of the documented schema.
- Avoid logging API keys, private prompts, private source media URLs, or callback URLs.
