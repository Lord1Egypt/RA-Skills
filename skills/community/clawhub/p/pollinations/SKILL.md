---
name: pollinations
version: 1.1.1
description: "Pollinations.ai API for AI generation and analysis - text, images, videos, audio, vision, and transcription. Use when user requests AI-powered content (text completion, image generation/editing, video generation, audio/TTS, image/video analysis, audio transcription) or mentions Pollinations. Supports 25+ models with OpenAI-compatible endpoints."
metadata: {"openclaw":{"emoji":"🧬","homepage":"https://pollinations.ai","os":["darwin","linux","win32"],"requires":{"bins":["curl","jq","base64"],"env":["POLLINATIONS_API_KEY"]},"primaryEnv":"POLLINATIONS_API_KEY","install":[{"id":"jq-brew","kind":"brew","formula":"jq","bins":["jq"],"label":"Install jq via Homebrew","os":["darwin"]},{"id":"jq-apt","kind":"shell","command":"sudo apt-get install -y jq","bins":["jq"],"label":"Install jq via apt","os":["linux"]}]}}
---

# Pollinations v1.1.1

Unified AI platform for generating and analyzing text, images, videos, and audio with 250+ text, 75+ image, 25 video and 40 audio models.

## API Key

Get free or paid keys at https://enter.pollinations.ai
- Secret Keys (`sk_`): Server-side, no rate limits (recommended)
- Optional for many operations (free tier available)

### Runtime Requirements

| Type | Name | Required |
|------|------|----------|
| Env | `POLLINATIONS_API_KEY` | Optional (free tier works without) |
| Bin | `curl` | Yes |
| Bin | `jq` | Yes |
| Bin | `base64` | Yes |

## Operations & Scripts

### 1. Text/Chat Generation (`scripts/chat.sh`)

Generate text using 250+ LLM models with OpenAI-compatible API.

**Usage:**
```bash
scripts/chat.sh "your message"
scripts/chat.sh "your message" --model claude --temp 0.7
scripts/chat.sh "explain quantum physics" --model openai --max-tokens 500
scripts/chat.sh "list 3 colors" --json --model openai
scripts/chat.sh "solve this step by step" --model openai-reasoning --reasoning-effort high
scripts/chat.sh "translate to French" --system "You are a translator" --model gemini
```

**Options:**
- `--model MODEL` — Model name (default: openai)
- `--temp N` — Temperature 0-2 (default: 1)
- `--max-tokens N` — Max response length
- `--top-p N` — Nucleus sampling 0-1
- `--seed N` — Reproducibility (-1 = random)
- `--system "PROMPT"` — System prompt
- `--json` — Force structured JSON response
- `--reasoning-effort LVL` — For reasoning models (e.g. openai-reasoning, grok-reasoning, kimi-thinking): high/medium/low/minimal/none
- `--thinking-budget N` — Token budget for reasoning models

**Models:** short aliases such as `openai` (free, default), `deepseek`, `grok`, `kimi`, `llama`, `minimax` (free) and `claude`, `gemini`, `gemini-large`, `gemini-search`, `mistral`, `perplexity` (paid), or a full id like `openai/gpt-5.5`. Ids are now `provider/name`; old aliases may change, so check `scripts/models.sh text [--free]` (shows aliases and free/paid).

**Simple text (no script needed):**
```bash
curl "https://gen.pollinations.ai/text/Hello%20world"
```

### 2. Image Generation (`scripts/image.sh`)

Generate images from text prompts with multiple models and options.

**Usage:**
```bash
scripts/image.sh "a sunset over mountains"
scripts/image.sh "a portrait" --model flux --width 1024 --height 1024
scripts/image.sh "logo design" --model gptimage --quality hd --transparent
scripts/image.sh "photo" --enhance --nologo --private
scripts/image.sh "art" --negative "blurry, low quality" --seed 42
```

**Options:**
- `--model MODEL` — Model (default: flux)
- `--width N` — Width 16-2048px (default: 1024)
- `--height N` — Height 16-2048px (default: 1024)
- `--seed N` — Reproducibility
- `--output FILE` — Output filename
- `--enhance` — AI prompt improvement
- `--negative "TEXT"` — Negative prompt (what to avoid)
- `--nologo` — Remove watermark
- `--private` — Private generation
- `--safe` — Enable NSFW filter
- `--quality LEVEL` — low/medium/high/hd (gptimage only)
- `--transparent` — Transparent background PNG (gptimage only)
- `--image-url URL` — Source image for image-to-image

**Models:** free: `flux` (default), `kontext`, `klein`, `z-image`; paid: `gptimage`, `seedream`, `nanobanana`, `nanobanana-pro`, `flux-2-pro`, and more. Use `scripts/models.sh image [--free]` to list all.

### 3. Image Editing / Image-to-Image (`scripts/image-edit.sh`)

Transform or edit existing images using AI.

**Usage:**
```bash
scripts/image-edit.sh "make it blue" --source "https://example.com/photo.jpg"
scripts/image-edit.sh "add sunglasses" --source photo.jpg --model kontext
scripts/image-edit.sh "convert to watercolor" --source input.png --output watercolor.jpg
```

**Options:**
- `--source URL/FILE` — Source image (URL or local file, required)
- `--model MODEL` — Model (default: kontext)
- `--seed N` — Reproducibility
- `--negative "TEXT"` — Negative prompt
- `--output FILE` — Output filename

### 4. Video Generation (`scripts/image.sh` with video models)

Generate videos from text prompts or images.

**Usage:**
```bash
scripts/image.sh "a cat playing piano" --model veo --duration 6
scripts/image.sh "ocean waves" --model seedance-2.0 --duration 8 --aspect-ratio 16:9
scripts/image.sh "timelapse" --model veo --duration 4 --audio
scripts/image.sh "animate this" --model seedance-2.0 --image-url "https://example.com/photo.jpg"
```

**Options (in addition to image options):**
- `--model MODEL` — Video model (required)
- `--duration N` — Length in seconds (veo: 4/6/8; others vary, see the model)
- `--aspect-ratio RATIO` — 16:9 or 9:16
- `--audio` — Enable audio generation (veo only)
- `--image-url URL` — Source image for image-to-video

**Frame interpolation (veo):** Pass two images for first/last frame interpolation using the API directly:
```
https://gen.pollinations.ai/image/prompt?model=veo&image[0]=first_frame_url&image[1]=last_frame_url
```

**Models:** all video models are paid (need a funded key): `veo` (4-8s, audio, frame interpolation), `seedance-2.0` / `seedance-2.5`, `wan` / `wan-2.7`, `kwaivgi/kling-v3.0-std`, `grok-imagine-video`, `happyhorse`. Run `scripts/models.sh video`.

### 5. Text-to-Speech / Audio (`scripts/tts.sh`)

Convert text to speech via the OpenAI-compatible `/v1/audio/speech` endpoint.

**Usage:**
```bash
scripts/tts.sh "Hello world"
scripts/tts.sh "Bonjour le monde" --voice nova --format mp3
scripts/tts.sh "Welcome" --model eleven --voice rachel --format wav --output welcome.wav
scripts/tts.sh "Speak warmly" --model qwen-tts-instruct --instruct "soft and gentle"
scripts/tts.sh "upbeat jazz" --model elevenmusic --output music.mp3
```

**Options:**
- `--voice VOICE` — Voice (default: nova)
- `--format FORMAT` — Output format (default: mp3)
- `--model MODEL` — Model (default: tts-1)
- `--speed N` — Speech speed 0.25–4.0
- `--seed N` — Deterministic output
- `--instruct TEXT` — Emotion/style hint (qwen-tts-instruct only)
- `--output FILE` — Output filename

**Voices:** depend on the model. `tts-1` / `tts-1-hd` (default, free): alloy, echo, fable, onyx, nova, shimmer. ElevenLabs models (`--model eleven`): 35 voices such as rachel, domi, bella, adam, antoni, josh, sam, daniel, george, brian (or a custom voice UUID). Other models (kokoro, qwen3-tts, grok-tts, gemini TTS, mai-voice) have their own lists: `scripts/models.sh audio --json | jq` shows the model and its voices.

**Formats (6):** mp3, opus, aac, flac, wav, pcm

**Models:** `tts-1` (default, free), `tts-1-hd` (free), `eleven` (ElevenLabs v3, paid), `qwen-tts-instruct` (instructable speech, paid), `kokoro` (paid), `music` (ElevenLabs music, paid). Run `scripts/models.sh audio [--free]`.

### 6. Image Analysis / Vision (`scripts/analyze-image.sh`)

Analyze and describe images using vision-capable AI models.

**Usage:**
```bash
scripts/analyze-image.sh "https://example.com/photo.jpg"
scripts/analyze-image.sh photo.jpg --prompt "What objects are in this image?"
scripts/analyze-image.sh image.png --model claude --prompt "Extract all text from this image"
```

**Options:**
- `--prompt "TEXT"` — Analysis question (default: "Describe this image in detail")
- `--model MODEL` — Vision model (default: openai, free)

**Input:** URL or local file (jpg, png, gif, webp)

**Models:** any text model that accepts images: `openai` (free), `grok`, `kimi` (free); `gemini`, `gemini-large`, `claude` (paid). Use `scripts/models.sh vision [--free]`.

### 7. Video Analysis (`scripts/analyze-video.sh`)

Analyze video content using AI vision models.

**Usage:**
```bash
scripts/analyze-video.sh "https://example.com/video.mp4"
scripts/analyze-video.sh recording.mp4 --prompt "Summarize the key moments"
scripts/analyze-video.sh clip.mov --model gemini-large --prompt "Count the people"
```

**Options:**
- `--prompt "TEXT"` — Analysis question (default: "Describe this video in detail")
- `--model MODEL` — Video-capable model (default: gemini)

**Input:** URL or local file (mp4, mov, avi)

**Models:** needs a model with video input: `gemini` (default, paid), `gemini-large`; community models (see `scripts/models.sh text`) with video input may be free but unreliable.

### 8. Audio Transcription (`scripts/transcribe.sh`)

Transcribe audio files to text via the Whisper-compatible `/v1/audio/transcriptions` endpoint.

**Usage:**
```bash
scripts/transcribe.sh recording.mp3
scripts/transcribe.sh podcast.wav --model scribe --language en
scripts/transcribe.sh "https://example.com/audio.mp3" --language fr --format srt
scripts/transcribe.sh meeting.m4a --format verbose_json --temperature 0
```

**Options:**
- `--model MODEL` — whisper-large-v3 (default), whisper-1, scribe (ElevenLabs)
- `--language CODE` — ISO-639-1 hint (e.g. en, fr, ja) for better accuracy
- `--prompt TEXT` — Optional context/style prompt
- `--format FORMAT` — json (default), text, srt, vtt, verbose_json
- `--temperature N` — Sampling temperature 0–1

**Input:** Local file or URL (mp3, mp4, mpeg, mpga, m4a, wav, webm)

### 9. List Available Models (`scripts/models.sh`)

Dynamically list all available models from the API.

**Usage:**
```bash
scripts/models.sh              # List all models: category, id, [aliases], free|paid
scripts/models.sh text --free  # Only free models (any category; add --json for raw data)
scripts/models.sh text         # Text/chat models only
scripts/models.sh image        # Image generation models
scripts/models.sh video        # Video generation models
scripts/models.sh vision       # Vision/analysis models
scripts/models.sh audio        # Audio/TTS models
```

## API Endpoints Reference

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Simple Text | `/text/{prompt}` | GET |
| Chat Completion | `/v1/chat/completions` | POST |
| Image Generation | `/image/{prompt}?{params}` | GET |
| Image-to-Image | `/image/{prompt}?image={url}&{params}` | GET |
| Video Generation | `/video/{prompt}?{params}` | GET |
| Image Analysis | `/v1/chat/completions` (with image_url) | POST |
| Video Analysis | `/v1/chat/completions` (with video_url) | POST |
| Text-to-Speech | `/v1/audio/speech` | POST |
| Audio Transcription | `/v1/audio/transcriptions` (multipart) | POST |
| Media Upload | `https://media.pollinations.ai/upload` | POST |
| List Text Models | `/v1/models` | GET |
| List Image Models | `/image/models` | GET |
| List Audio Models | `/audio/models` | GET |
| List Vision Models | `/text/models` | GET |

## Tips

1. **Free tier available**: Many operations work without an API key (rate limited)
2. **OpenAI-compatible**: Chat endpoint works with existing OpenAI integrations
3. **Reproducibility**: Use `seed` parameter for consistent outputs across all operations
4. **Image enhancement**: Use `--enhance` for AI-improved prompts on image generation
5. **JSON mode**: Use `--json` flag on chat for structured data extraction
6. **Reasoning models**: Use `--reasoning-effort` with reasoning models (openai-reasoning, grok-reasoning, kimi-thinking) for controlled thinking depth
7. **Video from images**: Use `--image-url` with seedance-2.0 for image-to-video, or veo frame interpolation
8. **Audio on video**: Use `--audio` with veo model for videos with sound
9. **Local files**: Analysis scripts (image, video, transcription) accept both URLs and local files
10. **Data leaves your machine**: prompts, images, video and audio are sent to gen.pollinations.ai (and local images for editing are uploaded to media.pollinations.ai). Selecting a model such as claude, gemini or openai routes the content to that vendor through Pollinations. Do not send anything you would not share with a third party.
11. **Transcription inputs**: only local files and http(s) URLs are accepted; other URL schemes (file://, ftp://) are rejected.
10. **Private mode**: Use `--private` to keep generations off public feed

## API Documentation

Full docs: https://enter.pollinations.ai/api/docs
