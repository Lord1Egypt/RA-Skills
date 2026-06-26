---
name: openrouter-vision-agent
description: Analyze images using OpenRouter's vision API with x-ai/grok-4.1-fast. Requires OPENROUTER_API_KEY env var or user-provided key. Use when the user asks to describe, explain, or interpret an image, or when image analysis is needed. Triggered by phrases like "analyze this image", "what's in this photo", "describe this picture", "use openrouter vision". ⚠️ Images are sent to openrouter.ai — avoid sending sensitive/untrusted images.
---

# OpenRouter Vision Agent

Analyzes images via OpenRouter using `x-ai/grok-4.1-fast`.

## API Details

- **Model**: `x-ai/grok-4.1-fast`
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Auth**: `OPENROUTER_API_KEY` env var — required
- **Max Tokens**: 500–2000 (adjust depending on needed detail)

## Image Analysis

### Via curl

```bash
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "x-ai/grok-4.1-fast",
    "max_tokens": 800,
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "<prompt>"},
        {"type": "image_url", "image_url": {"url": "<image_url>"}}
      ]
    }]
  }'
```

### Parameters

| Field | Value |
|-------|-------|
| `model` | `x-ai/grok-4.1-fast` |
| `messages[].content[].type` | `text` + `image_url` |
| `image_url.url` | Direct image URL (http/https) |
| `max_tokens` | 500–2000 |

### Output

Parse `choices[0].message.content` from the JSON response.

## Notes

- **Credential required**: `OPENROUTER_API_KEY` env var must be set. If not available, ask the user for their OpenRouter API key before proceeding.
- **Privacy**: Images (including URLs and uploaded files) are sent to openrouter.ai. Do not use this skill with sensitive or private images.
- Image URLs must be publicly accessible HTTP/HTTPS URLs
- Supports JPEG, PNG, WebP, and other common formats
- For local files, upload to a public URL first