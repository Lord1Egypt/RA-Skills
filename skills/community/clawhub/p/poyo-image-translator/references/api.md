# PoYo Image Translator API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Model page: <https://poyo.ai/models/image-translator>

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

- `poyo-ai/image-translator`: image text translation through PoYo's async generation workflow.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `image_urls` string array, required
- `source_language` string, optional; use `auto` when detection is desired
- `target_language` string, required

Always verify current field support on the PoYo model page before relying on model-specific options.

## Submission Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "poyo-ai/image-translator",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "image_urls": [
        "https://example.com/source-image.png"
      ],
      "source_language": "auto",
      "target_language": "en"
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
    "created_time": "2026-05-30T08:00:00"
  }
}
```

## Status Query Example

```bash
curl --fail-with-body --request GET \
  --url "https://api.poyo.ai/api/generate/status/task_unified_example" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

## Practical Guidance

- Use a public image URL that PoYo can fetch.
- Use `source_language: auto` when the source language is not known.
- Set `target_language` explicitly.
- Save `data.task_id` immediately after submission.
- Use `callback_url` for production queues and longer user workflows.
- Avoid logging API keys, private images, private image URLs, callback URLs, or generated output URLs.
