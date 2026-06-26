---
name: mmx
description: Full multimodal generation via MiniMax CLI (mmx). Covers text chat, image generation, video synthesis, TTS speech, music composition, vision analysis, and web search. Activates when Arif wants to generate content or analyze images. Prerequisites: mmx auth login with API key. NOT for deep research loops (use mmx-text-researcher skill instead).
metadata: {"openclaw": {"emoji": "🎨", "requires": {"bins": ["mmx"]}}}
---

# MMX — MiniMax Multimodal CLI

Full reference for `mmx` CLI. For deep research workflows, use `mmx-text-researcher` skill instead.

## Auth Check (First)

```bash
mmx auth status
# If not authenticated:
mmx auth login --api-key <your-api-key>
# Check region:
mmx config show
```

## Text Chat

```bash
# Basic
mmx text chat --message "What is MiniMax?"

# Streaming
mmx text chat --model MiniMax-M2.7-highspeed --message "Hello" --stream

# With system prompt
mmx text chat --system "You are a coding assistant" --message "Fizzbuzz in Go"

# Multi-turn (conversation history)
mmx text chat --message "user:Hi" --message "assistant:Hey!" --message "How are you?"

# JSON output
mmx text chat --message "Extract key facts as JSON" --output json

# From file
cat messages.json | mmx text chat --messages-file - --output json
```

### Models
- `MiniMax-M2.7` — standard
- `MiniMax-M2.7-highspeed` — faster response
- `MiniMax-Text-01` — best for research/synthesis

## Image Generation

```bash
# Simple
mmx image "A cat in a spacesuit"

# With options
mmx image generate --prompt "A cat" --n 3 --aspect-ratio 16:9

# Output to directory
mmx image generate --prompt "Logo" --out-dir ./out/

# Available aspect ratios: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
```

## Video Generation

```bash
# Async (start and track)
mmx video generate --prompt "Ocean waves at sunset"

# Async with progress tracking
mmx video generate --prompt "A robot painting" --async

# Get task status
mmx video task get --task-id <task-id>

# Download completed video
mmx video download --file-id <file-id> --out video.mp4
mmx video generate --prompt "Ocean waves at sunset" --download sunset.mp4
```

## Speech / TTS

```bash
# Basic synthesis
mmx speech synthesize --text "Hello!" --out hello.mp3

# Streaming playback (pipe to mpv)
mmx speech synthesize --text "Stream me" --stream | mpv -

# Voice selection + speed
mmx speech synthesize --text "Hi" --voice English_magnetic_voiced_man --speed 1.2

# List available voices
mmx voices

# From stdin
echo "Breaking news" | mmx speech synthesize --text-file - --out news.mp3
```

## Music Generation

```bash
# With lyrics
mmx music generate --prompt "Upbeat pop" --lyrics "[verse] La da dee, sunny day" --out song.mp3

# Auto-generate lyrics from prompt
mmx music generate --prompt "Indie folk, melancholic, rainy night" --lyrics-optimizer --out song.mp3

# Instrumental (no vocals)
mmx music generate --prompt "Cinematic orchestral" --instrumental --out bgm.mp3

# Cover (generate cover from reference audio)
mmx music cover --prompt "Jazz, piano, warm female vocal" --audio-file original.mp3 --out cover.mp3

# Cover from URL
mmx music cover --prompt "Indie folk" --audio https://example.com/song.mp3 --out cover.mp3
```

## Vision / Image Understanding

```bash
# Local file
mmx vision photo.jpg

# Describe with custom prompt
mmx vision describe --image https://example.com/img.jpg --prompt "What breed?"

# From file-id
mmx vision describe --file-id file-123
```

## Web Search

```bash
# Basic
mmx search "MiniMax AI"

# Structured JSON output
mmx search query --q "latest news" --output json
```

## Utility

```bash
# Check quota
mmx quota

# Show config
mmx config show

# Set region (global or cn)
mmx config set --key region --value cn

# Set default model
mmx config set --key default-text-model --value MiniMax-M2.7-highspeed

# Export schema
mmx config export-schema | jq .

# Update CLI
mmx update
mmx update latest
```

## Common Use Cases

| Task | Command |
|---|---|
| Generate image for Arif's geology viz | `mmx image generate --prompt "<description>" --aspect-ratio 16:9 --out-dir ./output/` |
| Create video clip | `mmx video generate --prompt "<scene>" --async` |
| TTS voice message | `mmx speech synthesize --text "<message>" --voice <voice> --out voice.mp3` |
| Compose background music | `mmx music generate --prompt "<mood>" --instrumental --out bgm.mp3` |
| Analyze geology photo | `mmx vision <path-to-image>` |
| Quick fact check | `mmx search "<query>"` |
| Research synthesis | Use `mmx-text-researcher` skill instead |
