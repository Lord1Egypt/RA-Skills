---
name: groq-whisper
description: Transcribe audio files using Groq's Whisper API (whisper-large-v3). Fast cloud-based speech-to-text with no local model required. Use when receiving voice messages, audio files, or any speech that needs transcription. Supports all major audio formats (ogg, mp3, wav, m4a, webm, flac).
author: DirectorVector
homepage: https://github.com/DirectorVector
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl", "jq"] },
        "env": [
          {
            "name": "GROQ_API_KEY",
            "description": "Groq API key. Alternatively store in ~/.config/groq/credentials.json as {\"api_key\":\"gsk_...\"}.",
            "required": false
          }
        ]
      }
  }
---

# Groq Whisper

Cloud speech-to-text via Groq's Whisper API. No local model, no GPU, no fan spin.

## Setup

1. Get a free API key at `console.groq.com`
2. Store it:
   ```bash
   mkdir -p ~/.config/groq
   echo '{"api_key":"gsk_your_key_here"}' > ~/.config/groq/credentials.json
   chmod 600 ~/.config/groq/credentials.json
   ```
   Or set `GROQ_API_KEY` env var.

## Usage

```bash
# Transcribe an audio file
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg

# Specify language (default: en)
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg es
```

## When to use

Call this script whenever you receive an audio/voice message attachment. Pass the file path directly — Groq handles ogg, mp3, wav, m4a, webm, and flac natively. No format conversion needed.

## Details

- **Model:** whisper-large-v3 (best accuracy)
- **Speed:** Faster than real-time (typically <2s for a 5-minute clip)
- **Cost:** Free tier available, no credit card required
- **Privacy:** Groq does not retain input data or train on it
- **Requires:** `curl`, `jq`, Groq API key
