# PoYo Seedream 5.0 Pro API Reference

## Endpoints

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/image-series/seedream-5-0-pro>
- Model page: <https://poyo.ai/models/seedream-5-0-pro>

## Authentication

Send `Authorization: Bearer $POYO_API_KEY` and `Content-Type: application/json`. Create or manage a key at <https://poyo.ai/dashboard/api-key>.

## Models

- `seedream-5.0-pro`: text-to-image generation.
- `seedream-5.0-pro-edit`: prompt-guided editing with reference images.

## Request Fields

Top-level fields:

- `model` is required.
- `input` is required.
- `callback_url` is optional.

Supported `input` fields:

- `prompt`: required non-empty string.
- `image_urls`: required for edit mode; 1 to 10 URLs. Do not send it in generation mode.
- `size`: `1K`, `2K`, `1:1`, `3:4`, `4:3`, `16:9`, or `9:16`; defaults to `2K` when omitted.
- `n`: integer from 1 to 6.
- `output_format`: `jpeg` or `png`.
- `enable_safety_checker`: optional boolean.

## Generation Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer $POYO_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "seedream-5.0-pro",
    "input": {
      "prompt": "Editorial product photograph of a translucent glass speaker on a clean studio set",
      "size": "2K",
      "n": 1,
      "output_format": "png"
    }
  }'
```

## Edit Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer $POYO_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "seedream-5.0-pro-edit",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "prompt": "Keep the product shape and replace the background with a bright gallery interior",
      "image_urls": ["https://example.com/product.png"],
      "size": "16:9",
      "n": 1,
      "output_format": "jpeg"
    }
  }'
```

## Result Handling

- Save `data.task_id` immediately after submission.
- Poll the unified status endpoint for local workflows.
- Use `callback_url` for production queues.
- Treat generated image URLs as potentially sensitive and avoid placing them in public logs.
