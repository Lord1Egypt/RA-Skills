---
name: oatda-vision-analysis
description: Analyze images using vision-capable AI models through OATDA's unified API. Triggers when the user wants to analyze, describe, or understand images; extract text (OCR) from images; understand diagrams, charts, screenshots, or photos; get AI-powered image descriptions using OpenAI GPT-4o, Anthropic Claude, Google Gemini, or other vision models via OATDA.
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "👁️",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "config": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA Vision Analysis

Analyze images using vision-capable AI models through OATDA's unified API.

## API Key Resolution

All commands need the OATDA API key. Resolve it inline for each `exec` call:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}"
```

If the key is empty or `null`, tell the user to get one at https://oatda.com and configure it.

**Security**: Never print the full API key. Only verify existence or show first 8 chars.

## Model Mapping

| User says | Provider | Model |
|-----------|----------|-------|
| gpt-4o (default) | openai | gpt-4o |
| gpt-4o-mini | openai | gpt-4o-mini |
| claude, sonnet | anthropic | claude-3-5-sonnet |
| gemini | google | gemini-2.0-flash |
| gemini-1.5 | google | gemini-1.5-pro |

**Default**: `openai` / `gpt-4o` if no model specified.

> ⚠️ Models update frequently. If a model ID fails, query `oatda-list-models` with `?type=chat` for the latest vision-capable models.

## Image URL Validation

- **Accept**: `https://` URLs or `data:image/` base64 data URIs
- **Reject**: `http://` URLs, local file paths, internal IPs (localhost, 127.0.0.1, 169.254.x.x)
- If user provides a local file, suggest converting to base64 first

## API Call

**CRITICAL**: The endpoint is `/api/v1/llm/image` (NOT `/api/v1/llm/generate-image` — that's for image generation). The body uses a `contents` array, NOT a simple `prompt` string.

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/image" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "<PROVIDER>",
    "model": "<MODEL>",
    "contents": [
      {"type": "text", "text": "<ANALYSIS_PROMPT>"},
      {"type": "image", "image": {"url": "<IMAGE_URL>", "detail": "auto"}}
    ]
  }'
```

### Optional Parameters (add to body)

- `temperature`: 0-2, default 0.7
- `maxTokens`: Max response tokens

### Image Detail Levels

- `"auto"` — Let the model decide (default)
- `"low"` — Faster, cheaper, less detail
- `"high"` — More detail, higher cost (recommended for OCR)

## Response Format

```json
{
  "success": true,
  "provider": "openai",
  "model": "gpt-4o",
  "response": "The image shows a sunset over...",
  "usage": {
    "promptTokens": 800,
    "completionTokens": 200,
    "totalTokens": 1000
  },
  "costs": {
    "inputCost": 0.004,
    "outputCost": 0.006,
    "totalCost": 0.01,
    "currency": "USD"
  }
}
```

Present the `response` field to the user. Optionally mention token usage and cost.

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Tell user to check their key |
| 400 | Bad request | Check image URL is valid HTTPS, model supports vision |
| 429 | Rate limited | Wait 5 seconds and retry once |

## Example

User: "Describe this image: https://example.com/photo.jpg"

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/image" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "openai",
    "model": "gpt-4o",
    "contents": [
      {"type": "text", "text": "Describe this image in detail"},
      {"type": "image", "image": {"url": "https://example.com/photo.jpg", "detail": "auto"}}
    ]
  }'
```

## Notes

- Endpoint is `/api/v1/llm/image` — NOT `/api/v1/llm/generate-image` (that's for generation)
- Body uses `contents` array format, NOT a simple prompt string
- Only HTTPS image URLs accepted — no HTTP, no local paths
- Image tokens are included in prompt token count and affect cost
- For OCR tasks, use `"detail": "high"`
- Use `oatda-generate-image` for creating images
- Use `oatda-list-models` for available vision models
