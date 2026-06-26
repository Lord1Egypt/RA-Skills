---
name: pollinations-ai
description: Generate images, music, and video using Pollinations AI API. Use when: (1) User wants to create images from text prompts, (2) User wants to generate music/audio, (3) User wants to create videos from text, (4) Using AI image generation with models like flux, zimage, nanobanana.
---

# Pollinations AI - Image, Music & Video Generation

A comprehensive skill for generating images, music, and video using the Pollinations AI API.

## Overview

Pollinations.ai provides free AI generation with API key support. This skill enables:
- **Image Generation** - Create images from text prompts using state-of-the-art models
- **Music/Audio Generation** - Generate background music and audio tracks
- **Video Generation** - Create videos from text descriptions

## Prerequisites

### 1. Get an API Key

Visit [pollinations.ai](https://pollinations.ai/) to get your free API key.

### 2. Set Environment Variable

Add to your shell profile (`~/.bashrc` or `~/.zshrc`):

```bash
export POLLINATIONS_API_KEY="your_api_key_here"
```

Then reload:
```bash
source ~/.bashrc
```

### 3. Install Dependencies

```bash
pip install requests Pillow
```

## Security Configuration

### Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `POLLINATIONS_API_KEY` | Yes | Your API key from pollinations.ai |

### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_CHAT_ID` | (none) | Chat ID for Telegram sending. If not set, --telegram flag is disabled |
| `ALLOWED_OUTPUT_DIRS` | `.`, `/tmp` | Comma-separated list of allowed output directories |
| `OPENCLAW_WORKSPACE` | `~/.openclaw/workspace` | Workspace directory for output files |

**Note:** The `--telegram` flag requires `TELEGRAM_CHAT_ID` to be explicitly set. If not set, the feature is disabled for security.

## Available Scripts

| Script | Purpose |
|--------|---------|
| `pollinations_image_gen.py` | Generate images from text prompts |
| `pollinations_audio_gen.py` | Generate music and audio |
| `pollinations_video_gen.py` | Generate videos from text |

## Usage

### Image Generation

```bash
# Basic usage
python pollinations_image_gen.py "a cute cat" --output cat.jpg

# With specific model and enhancements
python pollinations_image_gen.py "cyberpunk city at night" --model flux --enhance --width 1920 --height 1080 --output city.jpg

# Using different models
python pollinations_image_gen.py "your prompt" --model zimage
python pollinations_image_gen.py "your prompt" --model flux-2-dev  # Free tier
```

**Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `prompt` | Text description of desired image | (required) |
| `--model` | AI model to use | flux |
| `--width` | Image width in pixels | 1024 |
| `--height` | Image height in pixels | 1024 |
| `--enhance` | Enable AI prompt enhancement | false |
| `--seed` | Fixed random seed for reproducibility | random |
| `--safe` | Enable safe mode | false |
| `--output` | Output filename | output.jpg |
| `--telegram` | Send result via Telegram (requires TELEGRAM_CHAT_ID) | false |

### Music/Audio Generation

```bash
# Generate music from prompt
python pollinations_audio_gen.py "upbeat electronic dance music" --output music.mp3

# With custom duration
python pollinations_audio_gen.py "calm piano melody" --duration 60 --output piano.mp3
```

**Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `prompt` | Description of desired music | (required) |
| `--model` | Audio model | suno-4 |
| `--duration` | Length in seconds | 30 |
| `--output` | Output filename | output.mp3 |

### Video Generation

```bash
# Generate video
python pollinations_video_gen.py "a cat playing with a ball" --output video.mp4

# Custom duration and aspect ratio
python pollinations_video_gen.py "ocean waves" --duration 30 --aspectRatio 16:9 --output ocean.mp4
```

**Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `prompt` | Description of desired video | (required) |
| `--model` | Video model | suno-4 |
| `--duration` | Length in seconds | 10 |
| `--aspectRatio` | Video aspect ratio (16:9 or 9:16) | 16:9 |
| `--output` | Output filename | output.mp4 |

## Supported Models

### Image Models

| Model | Description | Quality |
|-------|-------------|---------|
| `flux` | Default high-quality model | ⭐⭐⭐⭐⭐ |
| `flux-2-dev` | Latest flux (FREE) | ⭐⭐⭐⭐⭐ |
| `zimage` | Fast generation | ⭐⭐⭐⭐ |
| `nanobanana` | Creative/artistic | ⭐⭐⭐⭐ |
| `gptimage` | OpenAI-based | ⭐⭐⭐⭐ |
| `seedream` | High detail | ⭐⭐⭐⭐ |

### Audio Models

| Model | Description |
|-------|-------------|
| `suno-4` | Latest (recommended) ⭐ |
| `suno-3.5` | Previous version |
| `suno-3` | Legacy model |

### Video Models

| Model | Description |
|-------|-------------|
| `suno` | Music video generation ⭐ |
| `veo-3.1` | Google video AI |
| `seedance` | High quality |
| `wan` | Open source option |
| `ltx-2` | Fast generation |

## Security Features

This skill includes several security measures:

1. **Path Traversal Protection** - All output paths are validated against allowed directories
2. **Environment Variable Validation** - Telegram sending requires explicit opt-in
3. **No Hardcoded Credentials** - All credentials come from environment variables
4. **File Access Whitelist** - Only configured directories can be written to

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Missing or invalid API key | Set `POLLINATIONS_API_KEY` correctly |
| 403 Forbidden | API key lacks permission | Check your key permissions at pollinations.ai |
| 429 Too Many Requests | Rate limit exceeded | Wait before making more requests |
| 402 Payment Required | Insufficient balance | Add credits at pollinations.ai |

## References

- API Documentation: https://gen.pollinations.ai/api/docs
- Pollinations Website: https://pollinations.ai/
