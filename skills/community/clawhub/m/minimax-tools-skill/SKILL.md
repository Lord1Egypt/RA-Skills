---
name: minimax-tools
description: "Direct MiniMax API integration for speech synthesis (TTS), voice cloning, image generation, video generation, and music generation using local Python scripts instead of MCP. Use when you want reliable script-based MiniMax workflows inside OpenClaw for: (1) text-to-speech with built-in Chinese/English defaults or explicit voice IDs, (2) voice cloning with upload + preview flows, (3) text-to-image or reference-image generation, (4) text-to-video, image-to-video, or first/last-frame video generation with async polling/download, and (5) music generation from prompts and lyrics."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "env": ["MINIMAX_API_KEY"] },
        "primaryEnv": "MINIMAX_API_KEY",
        "homepage": "https://github.com/cytwyatt/minimax-tools-skill"
      }
  }
---

# MiniMax Tools

Use this skill to call MiniMax multimodal APIs directly through local Python wrappers instead of relying on an external MCP server.

## Overview

This skill currently supports:

- Speech synthesis (TTS)
- Voice cloning
- Image generation
- Video generation
- Music generation

All wrappers are exposed through a single entrypoint script:

```bash
python3 scripts/minimax.py <subcommand> ...
```

Read `references/api-notes.md` only when you need endpoint details or parameter reminders.

## Prerequisites

Expect these environment variables to be available before running the scripts:

- `MINIMAX_API_KEY`

Optional:

- `MINIMAX_BASE_URL` if you need to override the default API host

Python dependency:

- `requests`

## Routing guide

- Use `tts` for speech synthesis
- Use `voice` for uploading clone inputs, creating cloned voices, and optionally downloading preview audio
- Use `image` for text-to-image or reference-image generation
- Use `video` for text-to-video, image-to-video, or first/last-frame video workflows
- Use `music` for song or instrumental generation

## TTS defaults

- Default model: `speech-2.8-turbo`
- Default format: `mp3`
- Default sample rate: `32000`
- Default bitrate: `128000`
- Default Chinese voice: `Chinese (Mandarin)_Lyrical_Voice`
- Default English voice: `English_Graceful_Lady`
- If `--voice` is omitted, the script uses `--voice-lang zh|en` and defaults to `zh`

## Voice cloning notes

- Clone source audio constraints:
  - `mp3`, `m4a`, or `wav`
  - 10 seconds to 5 minutes
  - <= 20 MB
- Optional prompt audio constraints:
  - `mp3`, `m4a`, or `wav`
  - under 8 seconds
  - <= 20 MB
- If cloning succeeds, the returned `voice_id` can be used immediately in TTS
- MiniMax documentation notes cloned voices are temporary unless used in real TTS within 7 days

## Video support

Supported modes:

- text-to-video: `video create`
- image-to-video: `video i2v`
- first/last-frame video: `video fl2v`

Video creation is asynchronous. Use `video query`, `video wait`, and `video download` for task follow-up.

## File handling rules

- Prefer saving outputs locally and returning file paths
- Local image inputs for image/video wrappers can be converted to Data URLs automatically
- Prefer URL-based output when MiniMax returns temporary files, then download immediately
- Avoid tight polling loops for async video jobs

## Resources

- `scripts/minimax.py` - unified CLI entrypoint
- `scripts/minimax_tts.py` - TTS wrapper
- `scripts/minimax_voice.py` - voice cloning wrapper
- `scripts/minimax_image.py` - image generation wrapper
- `scripts/minimax_video.py` - video generation wrapper
- `scripts/minimax_music.py` - music generation wrapper
- `references/api-notes.md` - focused API notes and constraints
