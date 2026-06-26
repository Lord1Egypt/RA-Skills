---
name: oatda-generate-image
description: Generate images from text descriptions using AI models through OATDA's unified API. Triggers when the user wants to generate, create, or produce AI images, artwork, illustrations, designs, mockups, or concept art using DALL-E 3, GPT-Image-1, Google Imagen, Bytedance Seedream, Alibaba Wan, MiniMax, xAI Grok image models, or other image generation models via OATDA.
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "config": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA Image Generation

Generate images from text descriptions using AI models through OATDA's unified API.

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
| dall-e, dall-e-3 (default) | openai | dall-e-3 |
| gpt-image | openai | gpt-image-1 |
| imagen | google | imagen-4.0-generate-001 |
| seedream | bytedance | seedream-4-5-251128 |
| wan | alibaba | wan2.6-t2i |
| minimax image | minimax | image-01 |
| grok image | xai | grok-imagine-image |

**Default**: `openai` / `dall-e-3` if no model specified.

> ⚠️ Models update frequently. If a model ID fails, query `oatda-list-models` with `?type=image` for the latest available models.

## Discovering Model-Specific Parameters

Different models support different parameters (sizes, quality, styles, masks, watermarks, negative prompts, etc.). Query before generating:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X GET "https://oatda.com/api/v1/llm/models?type=image" \
  -H "Authorization: Bearer $OATDA_API_KEY" | jq '.image_models[] | {id, supported_params}'
```

This returns each model's `supported_params` with type, allowed values, defaults, and descriptions. File-type parameters (like `mask`) require public URLs.

## API Call

**CRITICAL**: The endpoint is `/api/v1/llm/generate-image` (NOT `/api/v1/llm/image` — that's vision analysis).

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/generate-image" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "<PROVIDER>",
    "model": "<MODEL>",
    "prompt": "<IMAGE_DESCRIPTION>",
    "size": "1024x1024",
    "quality": "standard",
    "n": 1,
    "numberOfImages": 1
  }'
```

### Common Parameters

- `prompt`: Image description (1-4000 characters)
- `size`: `"1024x1024"`, `"1792x1024"`, `"1024x1792"`, `"2K"`, `"4K"` (model-dependent)
- `quality`: `"standard"`, `"hd"`, `"auto"`, `"low"`, `"medium"`, `"high"`
- `n` and `numberOfImages`: Number of images (1-10) — set both to same value
- `aspectRatio`: `"1:1"`, `"16:9"`, `"9:16"`, `"3:2"`, `"2:3"`, `"4:3"`, `"3:4"`
- `style`: `"vivid"` (dramatic) or `"natural"` (realistic)
- `background`: `"auto"`, `"transparent"`, `"opaque"`
- `outputFormat`: `"png"`, `"jpeg"`, `"webp"`
- `model_params`: Model-specific key-value pairs (see discovery above)

### model_params Examples

- DALL-E 3: `{"style": "vivid", "quality": "hd"}`
- GPT-Image-1: `{"quality": "high", "background": "transparent", "outputFormat": "png"}`
- Imagen 4: `{"sampleImageSize": "2K", "personGeneration": "allow_adult"}`
- Seedream: `{"size": "4K", "watermark": false}`
- Wan 2.6: `{"seed": "42", "negative_prompt": "blurry", "prompt_extend": true}`

## Response Format

```json
{
  "success": true,
  "url": "https://cdn.example.com/generated-image.png",
  "all_images": [
    {"url": "https://cdn.example.com/image-1.png"},
    {"url": "https://cdn.example.com/image-2.png"}
  ],
  "revised_prompt": "A detailed cyberpunk cityscape at night..."
}
```

Show image URL(s) from `all_images` array (or `url` field if single). Mention `revised_prompt` if present.

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Tell user to check their key |
| 400 | Bad request / prompt too long | Keep prompt under 4000 chars |
| 429 | Rate limited | Wait 5 seconds and retry once |
| 400 + content_policy | Content policy violation | Ask user to adjust description |

## Examples

### DALL-E 3 HD

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/generate-image" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "openai",
    "model": "dall-e-3",
    "prompt": "A cyberpunk city at night with neon lights reflecting on wet streets",
    "size": "1024x1024",
    "quality": "hd",
    "n": 1,
    "numberOfImages": 1,
    "model_params": {"style": "vivid"}
  }'
```

### GPT-Image-1 Transparent PNG

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/generate-image" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "openai",
    "model": "gpt-image-1",
    "prompt": "A sleek minimalist logo of a mountain, clean vector style",
    "n": 1,
    "model_params": {"quality": "high", "background": "transparent", "outputFormat": "png"}
  }'
```

### Seedream 4K No Watermark

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/generate-image" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "bytedance",
    "model": "seedream-4-5-251128",
    "prompt": "A majestic dragon flying over a fantasy kingdom at sunset",
    "model_params": {"size": "4K", "watermark": false}
  }'
```

## Notes

- Endpoint is `/api/v1/llm/generate-image` — NOT `/api/v1/llm/image` (vision analysis)
- Set both `n` and `numberOfImages` to the same value for compatibility
- Image URLs may be temporary — recommend downloading promptly
- Max prompt length: 4000 characters
- Use `oatda-vision-analysis` for analyzing images
- Use `oatda-list-models` for available image models
- **In Telegram/chat**: Extract only the image URL from the response (`jq -r '.url'`), do NOT dump raw JSON. Present as clickable link or describe the image.
