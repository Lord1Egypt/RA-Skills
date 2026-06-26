---
name: kai-minimax-tts
description: Generate voice audio and transcribe speech using MiniMax TTS API. Use when responding with voice or transcribing audio files.
metadata:
  openclaw:
    requires:
      env:
        - MINIMAX_API_KEY
      bins:
        - whisper
        - curl
        - xxd
---

# Kai MiniMax TTS

Generate voice audio using MiniMax TTS.

## Setup

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "kai-minimax-tts": {
        "enabled": true,
        "env": {
          "MINIMAX_API_KEY": "your_key_here"
        }
      }
    }
  }
}
```

## Usage

Generate voice (English):
```bash
bash {baseDir}/scripts/kai_tts.sh --speak "Hello" en
```

Generate voice (Spanish):
```bash
bash {baseDir}/scripts/kai_tts.sh --speak "Hola" es
```

Transcribe audio:
```bash
bash {baseDir}/scripts/kai_tts.sh --transcribe /path/to/audio.ogg
```

## Output Files

- Voice: `$WORKSPACE/Kai.mp3`
- Transcript: `$WORKSPACE/latest_from_blaze.txt`

## Customization

Set custom workspace:
```json
"env": { "KAI_MINIMAX_WORKSPACE": "/custom/path" }
```

Set custom voice IDs:
```json
"env": { 
  "KAI_ENGLISH_VOICE_ID": "voice_id",
  "KAI_SPANISH_VOICE_ID": "voice_id"
}
```
