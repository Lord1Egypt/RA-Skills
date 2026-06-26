---
name: oatda-list-models
description: List available AI models from OATDA's 10+ providers with optional filtering by type (chat, image, video) or provider name. Triggers when the user wants to see what models are available through OATDA, find the right model for a task, know which providers are supported, discover model-specific parameters (supported_params) for image or video generation, or filter models by capability or provider.
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "📋",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "config": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA List Models

List all available AI models from OATDA's providers with optional filtering.

## API Key Resolution

All commands need the OATDA API key. Resolve it inline for each `exec` call:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}"
```

If the key is empty or `null`, tell the user to get one at https://oatda.com and configure it.

**Security**: Never print the full API key. Only verify existence or show first 8 chars.

## API Calls

All requests are GET. Add query parameters to filter.

### List all models

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X GET "https://oatda.com/api/v1/llm/models" \
  -H "Authorization: Bearer $OATDA_API_KEY"
```

### Filter by type

- `?type=chat` — Text/chat models
- `?type=image` — Image generation models
- `?type=video` — Video generation models

### Filter by provider

- `?provider=openai`
- `?provider=anthropic`
- `?provider=google`
- `?provider=bytedance`
- `?provider=deepseek`
- etc.

### Combine filters

```bash
curl -s -X GET "https://oatda.com/api/v1/llm/models?type=image&provider=openai" \
  -H "Authorization: Bearer $OATDA_API_KEY"
```

### Discover model-specific parameters

Image and video models include `supported_params` describing model-specific options:

```bash
# Image model params
curl -s -X GET "https://oatda.com/api/v1/llm/models?type=image" \
  -H "Authorization: Bearer $OATDA_API_KEY" | jq '.image_models[] | {id, supported_params}'

# Video model params
curl -s -X GET "https://oatda.com/api/v1/llm/models?type=video" \
  -H "Authorization: Bearer $OATDA_API_KEY" | jq '.video_models[] | {id, supported_params}'

# Specific provider's video params
curl -s -X GET "https://oatda.com/api/v1/llm/models?type=video&provider=bytedance" \
  -H "Authorization: Bearer $OATDA_API_KEY" | jq '.video_models[] | select(.model | contains("seedance")) | .supported_params'
```

## Response Format

```json
{
  "total": 42,
  "filter": {"type": "all", "provider": null},
  "chatModels": [
    {"id": "provider/model-name", "provider": "...", "model": "...", "displayName": "..."}
  ],
  "imageModels": [
    {
      "id": "provider/model-name",
      "provider": "...",
      "model": "...",
      "displayName": "...",
      "supported_params": {
        "style": {"type": "string", "values": ["vivid", "natural"], "default": "vivid"}
      }
    }
  ],
  "videoModels": [
    {
      "id": "provider/model-name",
      "provider": "...",
      "model": "...",
      "displayName": "...",
      "supported_params": {
        "ratio": {"type": "string", "values": ["16:9", "9:16", "1:1"], "default": "16:9"},
        "duration": {"type": "string", "values": ["5", "10"], "default": "5"},
        "generate_audio": {"type": "boolean", "default": false, "optional": true},
        "first_frame_image": {"type": "file", "accept": "image/*", "optional": true}
      }
    }
  ]
}
```

## Understanding supported_params

Each parameter has:
- `type`: `string`, `number`, `boolean`, or `file`
- `values`: Allowed values for enums
- `default`: Default value
- `description`: What it does
- `optional`: Whether required
- `accept`: For `file` types — accepted MIME types (e.g., `"image/*"`)
- `min` / `max`: Range constraints for numbers

**File-type params** (e.g., `mask`, `first_frame_image`, `last_frame_image`) require public HTTPS URLs, not local paths.

## Presenting Results

Format models by category. Use the actual data returned by the API — do not hardcode model names.

**Chat Models** (N total):
- `provider/model-name` — Display Name

**Image Models** (N total):
- `provider/model-name` — Display Name

**Video Models** (N total):
- `provider/model-name` — Display Name

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Tell user to check their key |
| 429 | Rate limited | Wait and retry |

## Notes

- This is a GET request — no request body
- The `id` field (e.g., `openai/gpt-4o`) is the model identifier used in other OATDA skills
- Use `supported_params` to discover model-specific parameters before generating
- For file-type params, provide publicly accessible URLs
- Related skills: `oatda-text-completion`, `oatda-generate-image`, `oatda-generate-video`, `oatda-vision-analysis`
