# PoYo Happy Horse API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/video-series/happy-horse>
- Model page: <https://poyo.ai/models/happy-horse>
- Example repository: <https://github.com/PoyoAPI/happy-horse-api>

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

- `happy-horse`: Happy Horse video generation through PoYo.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required
- `image_urls` string array, optional
- `resolution` string, optional
- `duration` number, optional
- `aspect_ratio` string, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-Video Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "happy-horse",
    "input": {
      "prompt": "A flower blooming and wilting over two weeks, one photo per day. Same vase, same window, same angle. Light changes with weather. Quiet domestic ambience",
      "resolution": "720p",
      "duration": 10,
      "aspect_ratio": "16:9"
    }
  }'
```

## Image-to-Video Example

Use `image_urls` when the task should animate a specific product image, character frame, or visual concept.

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "happy-horse",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Animate the source product image into a short studio clip. Add a slow camera push-in, soft reflections, and subtle natural movement while preserving the product shape",
      "image_urls": [
        "https://example.com/source-frame.png"
      ],
      "resolution": "720p",
      "duration": 10,
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
- Download or store generated video files according to the product's retention policy.

## Practical Guidance

- Use text-to-video when the user has only a prompt.
- Use `image_urls` when visual identity, product shape, or opening frame matters.
- Use webhook delivery for production applications where the user may leave the page.
- Avoid logging API keys, private prompts, private media URLs, or callback URLs.
