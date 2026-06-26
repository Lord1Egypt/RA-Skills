---
name: groq-whisper-api
description: Transcribe audio via Groq Automatic Speech Recognition (ASR) Models (Whisper).
homepage: https://console.groq.com/docs/speech-to-text
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["curl"], "env": ["GROQ_API_KEY"] },
        "primaryEnv": "GROQ_API_KEY",
      },
  }
---

# Groq Whisper API (curl)

Transcribe an audio file via Groq’s OpenAI-compatible `/openai/v1/audio/transcriptions` endpoint.

## Quick start

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a
```

Defaults:

- Model: `whisper-large-v3-turbo`
- Output: `<input>.txt`

## Useful flags

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg --model whisper-large-v3 --out /tmp/transcript.txt
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --language en
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --prompt "Speaker names: Peter, Daniel"
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --json --out /tmp/transcript.json
```

## API key

Set `GROQ_API_KEY`, or configure it in `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    "groq-whisper-api": {
      apiKey: "GROQ_KEY_HERE",
    },
  },
}
```
