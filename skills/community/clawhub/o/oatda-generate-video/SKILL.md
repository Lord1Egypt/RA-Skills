---
name: oatda-generate-video
description: Generate videos from text descriptions using AI models through OATDA's unified API. Triggers when the user wants to generate, create, or produce AI video clips or animations using MiniMax, Google Veo, Alibaba Wan, Bytedance Seedance, ZAI, OpenAI Sora, xAI Grok video, or other video generation models via OATDA. Video generation is asynchronous — submit a request and poll for status.
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "files": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA Video Generation

Generate videos from text descriptions via OATDA. Video generation is **asynchronous** — submit a request, receive a task ID, then poll for completion.

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
| seedance, bytedance (default) | bytedance | seedance-1-5-pro-251215 |
| minimax, hailuo | minimax | T2V-01 |
| veo, google veo | google | veo-3.0-generate-preview |
| wan, alibaba | alibaba | wan2.5-t2v-preview |
| sora | openai | sora-2 |
| grok video | xai | grok-imagine-video |
| cogvideo, glm video | zai | cogvideox-3 |

**Default**: `bytedance` / `seedance-1-5-pro-251215` if no model specified.

> ⚠️ Models update frequently. If a model ID fails, query `oatda-list-models` with `?type=video` for the latest available models.

## Discovering Model-Specific Parameters

Different models support different parameters. Query before generating:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X GET "https://oatda.com/api/v1/llm/models?type=video" \
  -H "Authorization: Bearer $OATDA_API_KEY" | jq '.video_models[] | {id, supported_params}'
```

File-type parameters (like `first_frame_image`, `last_frame_image`) require public URLs.

## API Call

**CRITICAL**: The endpoint URL must include `?async=true`.

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/generate-video?async=true" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "<PROVIDER>",
    "model": "<MODEL>",
    "prompt": "<VIDEO_DESCRIPTION>"
  }'
```

### Optional Parameters (add to body)

- `duration`: Video duration in seconds
- `resolution`: `"720P"` or `"1080P"`
- `aspectRatio`: `"16:9"`, `"9:16"`, `"1:1"`
- `quality`: Quality setting (model-dependent)
- `style`: Style setting (model-dependent)
- `width` / `height`: Explicit pixel dimensions
- `model_params`: Model-specific key-value pairs

### model_params Examples

- Seedance: `{"ratio": "16:9", "duration": "5", "generate_audio": true, "camera_fixed": false}`
- Seedance I2V: `{"first_frame_image": "https://...", "last_frame_image": "https://..."}`
- MiniMax: `{"first_frame_image": "https://...", "resolution": "720P"}`
- xAI: `{"resolution": "720p"}`

## Response Format

```json
{
  "taskId": "minimax-T2V01-abc123def456",
  "status": "pending",
  "provider": "minimax",
  "model": "T2V-01",
  "message": "Video generation task created",
  "pollUrl": "/api/v1/llm/video-status/minimax-T2V01-abc123def456"
}
```

Note the `taskId` — this is needed to check status later.

## After Submitting

Tell the user:
> Video generation started! Task ID: `<taskId>`
> Video generation typically takes 30 seconds to 5 minutes.
> Use `oatda-video-status` to check when your video is ready.

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Tell user to check their key |
| 400 | Bad request / prompt too long | Keep prompt under 4000 chars |
| 429 | Rate limited | Wait and retry |
| 400 + content_policy | Content policy violation | Ask user to adjust description |

## Examples

### Seedance (default)

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/generate-video?async=true" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "bytedance",
    "model": "seedance-1-5-pro-251215",
    "prompt": "Ocean waves crashing on a beach at sunset, golden hour lighting, cinematic",
    "model_params": {"ratio": "16:9", "duration": "5", "generate_audio": true, "camera_fixed": false}
  }'
```

### Seedance Image-to-Video

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/generate-video?async=true" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "bytedance",
    "model": "seedance-1-5-pro-251215",
    "prompt": "Smooth transition from day to night",
    "model_params": {
      "ratio": "16:9",
      "first_frame_image": "https://example.com/daytime.jpg",
      "last_frame_image": "https://example.com/nighttime.jpg"
    }
  }'
```

### MiniMax with Reference Image

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/generate-video?async=true" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "minimax",
    "model": "T2V-01",
    "prompt": "The character starts walking forward slowly",
    "model_params": {"first_frame_image": "https://example.com/character.png", "resolution": "720P"}
  }'
```

### Google Veo

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm/generate-video?async=true" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "google",
    "model": "veo-3.0-generate-preview",
    "prompt": "A drone shot flying over a misty mountain range at sunrise",
    "duration": 5,
    "aspectRatio": "16:9"
  }'
```

## Notes

- Always use `?async=true` in the URL
- Generation takes 30 seconds to 5+ minutes depending on model
- Always give the user the task ID and suggest `oatda-video-status` to check progress
- For image-to-video: provide `first_frame_image` and optionally `last_frame_image` as public URLs
- Max prompt: 4000 characters
- Use `oatda-video-status` to check task completion
- Use `oatda-list-models` for available video models
