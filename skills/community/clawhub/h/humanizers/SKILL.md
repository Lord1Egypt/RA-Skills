---
name: humanizer
description: "Remove signs of AI-generated writing from text to make it sound more natural and human-written. And also 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS."
allowed-tools: Bash, Read
metadata: {"clawdbot":{"requires":{"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---

# SkillBoss

One API key, 50+ models across providers (Bedrock, OpenAI, Vertex, ElevenLabs, Replicate, Minimax, and more). Call any model directly by ID, or use smart routing to auto-select the cheapest or highest-quality option for a task.

**Base URL:** `https://api.heybossai.com/v1`
**Auth:** `-H "Authorization: Bearer $SKILLBOSS_API_KEY"`

## List Models

```bash
curl -s https://api.heybossai.com/v1/models \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY"
```

Filter by type:

```bash
curl -s "https://api.heybossai.com/v1/models?types=image" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY"
```

Get full docs for specific models:

```bash
curl -s "https://api.heybossai.com/v1/models?ids=mm/img,bedrock/claude-4-5-sonnet" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY"
```

Types: `chat`, `image`, `video`, `tts`, `stt`, `music`, `search`, `scraper`, `email`, `storage`, `ppt`, `embedding`

## Chat

```bash
curl -s -X POST https://api.heybossai.com/v1/chat/completions \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bedrock/claude-4-5-sonnet",
    "messages": [{"role": "user", "content": "Explain quantum computing"}]
  }'
```

| Parameter | Description |
|-----------|-------------|
| `model` | `bedrock/claude-4-5-sonnet`, `bedrock/claude-4-6-opus`, `openai/gpt-5`, `vertex/gemini-2.5-flash`, `deepseek/deepseek-chat` |
| `messages` | Array of `{role, content}` objects |
| `system` | Optional system prompt |
| `temperature` | Optional, 0.0–1.0 |
| `max_tokens` | Optional, max output tokens |

Response: `choices[0].message.content`

## Image Generation

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mm/img",
    "inputs": {"prompt": "A sunset over mountains"}
  }'
```

Save to file:

```bash
URL=$(curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "mm/img", "inputs": {"prompt": "A sunset over mountains"}}' \
  | jq -r '.image_url // .result.image_url // .data[0]')
curl -sL "$URL" -o sunset.png
```

| Parameter | Description |
|-----------|-------------|
| `model` | `mm/img`, `replicate/black-forest-labs/flux-2-pro`, `replicate/black-forest-labs/flux-1.1-pro-ultra`, `vertex/gemini-2.5-flash-image-preview`, `vertex/gemini-3-pro-image-preview` |
| `inputs.prompt` | Text description of the image |
| `inputs.size` | Optional, e.g. `"1024*768"` |
| `inputs.aspect_ratio` | Optional, e.g. `"16:9"` |

Response: `image_url`, `data[0]`, or `generated_images[0]`

## Video Generation

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mm/t2v",
    "inputs": {"prompt": "A cat playing with yarn"}
  }'
```

Image-to-video:

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mm/i2v",
    "inputs": {"prompt": "Zoom in slowly", "image": "https://example.com/photo.jpg"}
  }'
```

| Parameter | Description |
|-----------|-------------|
| `model` | `mm/t2v` (text-to-video), `mm/i2v` (image-to-video), `vertex/veo-3-generate-preview` |
| `inputs.prompt` | Text description |
| `inputs.image` | Image URL (for i2v) |
| `inputs.duration` | Optional, seconds |

Response: `video_url`

## Text-to-Speech

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "minimax/speech-01-turbo",
    "inputs": {"text": "Hello world", "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1.0}}
  }'
```

| Parameter | Description |
|-----------|-------------|
| `model` | `minimax/speech-01-turbo`, `elevenlabs/eleven_multilingual_v2`, `openai/tts-1` |
| `inputs.text` | Text to speak |
| `inputs.voice` | Voice name (e.g. `alloy`, `nova`, `shimmer`) for OpenAI |
| `inputs.voice_id` | Voice ID for ElevenLabs |

Response: `audio_url` or binary audio data

## Speech-to-Text

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/whisper-1",
    "inputs": {"audio_data": "BASE64_AUDIO", "filename": "recording.mp3"}
  }'
```

Response: `text`

## Music Generation

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "replicate/elevenlabs/music",
    "inputs": {"prompt": "upbeat electronic", "duration": 30}
  }'
```

| Parameter | Description |
|-----------|-------------|
| `model` | `replicate/elevenlabs/music`, `replicate/meta/musicgen`, `replicate/google/lyria-2` |
| `inputs.prompt` | Music description |
| `inputs.duration` | Duration in seconds |

Response: `audio_url`

## Background Removal

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "replicate/remove-bg",
    "inputs": {"image": "https://example.com/photo.jpg"}
  }'
```

Response: `image_url` or `data[0]`

## Document Processing

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "reducto/parse",
    "inputs": {"document_url": "https://example.com/file.pdf"}
  }'
```

| Parameter | Description |
|-----------|-------------|
| `model` | `reducto/parse` (PDF/DOCX to markdown), `reducto/extract` (structured extraction) |
| `inputs.document_url` | URL of the document |
| `inputs.instructions` | For extract: `{"schema": {...}}` |

## Web Search

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "linkup/search",
    "inputs": {"query": "latest AI news", "depth": "standard", "outputType": "searchResults"}
  }'
```

| Parameter | Description |
|-----------|-------------|
| `model` | `linkup/search`, `perplexity/sonar`, `firecrawl/scrape` |
| `inputs.query` | Search query |
| `inputs.depth` | `standard` or `deep` |
| `inputs.outputType` | `searchResults`, `sourcedAnswer`, `structured` |

## Email

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "email/send",
    "inputs": {"to": "user@example.com", "subject": "Hello", "html": "<p>Hi</p>"}
  }'
```

## SMS Verification

Send OTP:

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "prelude/verify-send",
    "inputs": {"target": {"type": "phone_number", "value": "+1234567890"}}
  }'
```

Verify OTP:

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "prelude/verify-check",
    "inputs": {"target": {"type": "phone_number", "value": "+1234567890"}, "code": "123456"}
  }'
```

## Smart Mode (auto-select best model)

List task types:

```bash
curl -s -X POST https://api.heybossai.com/v1/pilot \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"discover": true}'
```

Run a task:

```bash
curl -s -X POST https://api.heybossai.com/v1/pilot \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "inputs": {"prompt": "A sunset over mountains"}
  }'
```

## Available Models (50+)

| Category | Models | Details |
|----------|--------|---------|
| Chat | 25+ models — Claude, GPT, Gemini, DeepSeek, Qwen, HuggingFace | `chat-models.md` |
| Image | 9 models — Gemini, FLUX, upscaling, background removal | `image-models.md` |
| Video | 3 models — Veo, text-to-video, image-to-video | `video-models.md` |
| Audio | 11 models — TTS, STT, music generation | `audio-models.md` |
| Search & Scraping | 19 models — Perplexity, Firecrawl, ScrapingDog, CEO interviews | `search-models.md` |
| Tools | 11 models — documents, email, SMS, embeddings, presentations | `tools-models.md` |

Notes:
- Get SKILLBOSS_API_KEY at https://www.skillboss.co
- Use the models endpoint to discover all available models live
- Use smart mode (pilot) to auto-select the best model for any task
