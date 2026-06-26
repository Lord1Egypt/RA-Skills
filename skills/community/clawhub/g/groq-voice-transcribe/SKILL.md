---
name: groq-voice-transcribe
description: Transcribe audio files via Groq's OpenAI-compatible speech-to-text API. Use when the user sends voice messages or audio files and you need fast cloud speech-to-text through Groq instead of local Whisper.
---

# Groq Voice Transcribe

Fast speech-to-text for voice notes and audio files through Groq's OpenAI-compatible transcription endpoint.
Use it when you want cloud transcription via Groq instead of running Whisper locally.

Best for:
- Telegram / Signal voice notes
- short audio clips
- Chinese, English, or mixed daily speech
- fast transcript generation for follow-up summarization or chat replies

## What you need

You need a **Groq API key**.
Groq often provides a free developer tier / trial credits for new users.
Get one from:

- https://console.groq.com/
- Sign in, open **API Keys**, then create a key

## Easiest setup in OpenClaw

If OpenClaw is already running and configured, you can simply ask your assistant:

- **"Configure Groq Voice Transcribe for me"**
- **"Here is my Groq API key, set up Groq Voice Transcribe"**

The assistant can place the key into `~/.openclaw/openclaw.json` for you.

## Manual setup

Set `GROQ_API_KEY`, or configure it in `~/.openclaw/openclaw.json` under:

```json
{
  "skills": {
    "entries": {
      "groq-voice-transcribe": {
        "apiKey": "GROQ_KEY_HERE"
      }
    }
  }
}
```

## Quick start

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg
```

Defaults:
- Model: `whisper-large-v3-turbo`
- Output: `<input>.txt`
- Format: plain text

## Common examples

```bash
# Basic transcript
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg

# Chinese voice message
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg --language zh --prompt "中文普通话，日常聊天"

# Save to a custom file
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg --out /tmp/transcript.txt

# Verbose JSON output
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg --json --out /tmp/transcript.json
```

## Flags

- `--model <name>`: transcription model (default `whisper-large-v3-turbo`)
- `--out <path>`: output file path
- `--language <code>`: hint the spoken language, for example `zh`, `en`, `ja`
- `--prompt <text>`: optional context or spelling hint
- `--json`: write verbose JSON instead of plain text

## Notes

- Audio is sent to Groq for transcription.
- This skill is meant for transcription, not text-to-speech.
- If language is omitted, Groq can usually auto-detect it, but passing `--language zh` often helps for Chinese voice notes.
