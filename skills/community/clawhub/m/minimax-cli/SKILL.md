---
name: minimax-cli
description: "MiniMax AI platform CLI — text, image, video, speech, music, vision, and web search from terminal or AI agents. Use when generating multimedia content (images, TTS, video, music), doing web searches via MiniMax, or interfacing with the MiniMax API directly. Install with: npm install -g mmx-cli"
---

# MiniMax CLI

Official CLI for MiniMax AI Platform. Full multimodal platform — text, image, video, speech, music, vision, and search.

## Install

```bash
npm install -g mmx-cli
```

## Setup

```bash
# Authenticate (get key from https://platform.minimax.io)
mmx auth login --api-key sk-xxxxx

# Verify
mmx auth status
mmx quota
```

## Core Commands

### Text Chat
```bash
mmx text chat --message "prompt"
mmx text chat --model MiniMax-M2.7 --message "prompt" --stream
mmx text chat --system "You are a helpful assistant" --message "prompt"
mmx text chat --messages-file ./conversation.json --output json
```

### Image Generation
```bash
mmx image "A lobster in space"
mmx image generate --prompt "A cat" --n 3 --aspect-ratio 16:9
mmx image generate --prompt "Logo" --out-dir ./out/
```

### Video Generation
```bash
mmx video generate --prompt "Ocean waves at sunset" --async
mmx video generate --prompt "A robot painting" --download robot.mp4
mmx video task get --task-id <id>
mmx video download --file-id <id> --out video.mp4
```

### Speech (TTS)
```bash
mmx speech synthesize --text "Hello!" --out hello.mp3
mmx speech synthesize --text "Stream test" --stream | mpv -
mmx speech synthesize --text "Hi" --voice English_magnetic_voiced_man --speed 1.2
mmx speech voices  # list all available voices
```

### Music Generation
```bash
mmx music generate --prompt "Upbeat pop" --lyrics "[verse] La da dee" --out song.mp3
mmx music generate --prompt "Indie folk" --lyrics-optimizer --out song.mp3
mmx music generate --prompt "Cinematic orchestral" --instrumental --out bgm.mp3
mmx music cover --prompt "Jazz piano" --audio-file original.mp3 --out cover.mp3
```

### Vision
```bash
mmx vision photo.jpg
mmx vision describe --image https://example.com/img.jpg --prompt "What breed?"
```

### Web Search
```bash
mmx search "MiniMax AI latest news"
mmx search query --q "latest news" --output json
```

## Quotas

| Feature | Command | Quota |
|---------|---------|-------|
| Text/Chat | `mmx text chat` | 4,500 req/5hrs |
| Web Search | `mmx search` | integrated |
| Image Gen | `mmx image` | 50/day |

Check `mmx quota` for current usage.

## Key Reference

For voice list, async video workflow, and API details see `references/api-notes.md`.
