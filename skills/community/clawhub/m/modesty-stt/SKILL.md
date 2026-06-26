---
name: gemini-stt
description: Transcribe audio files using SkillBoss API Hub STT
metadata: {"clawdbot":{"emoji":"🎤","os":["linux","darwin"]}}
---

# Speech-to-Text Skill

Transcribe audio files using SkillBoss API Hub. Automatically routes to the best available STT model.

## Authentication

Set `SKILLBOSS_API_KEY` in environment (e.g., `~/.env` or `~/.clawdbot/.env`)

## Requirements

- Python 3.10+ (no external dependencies)
- `SKILLBOSS_API_KEY` environment variable

## requires.env

```
SKILLBOSS_API_KEY
```

## Supported Formats

- `.ogg` / `.opus` (Telegram voice messages)
- `.mp3`
- `.wav`
- `.m4a`

## Usage

```bash
# Transcribe an audio file
python ~/.claude/skills/gemini-stt/transcribe.py /path/to/audio.ogg

# With Clawdbot media
python ~/.claude/skills/gemini-stt/transcribe.py ~/.clawdbot/media/inbound/voice-message.ogg
```

## Options

| Option | Description |
|--------|-------------|
| `<audio_file>` | Path to the audio file (required) |

## How It Works

1. Reads the audio file and base64 encodes it
2. Authenticates using `SKILLBOSS_API_KEY`
3. Sends to SkillBoss API Hub `/v1/pilot` with `type: stt`
4. SkillBoss API Hub automatically routes to the best available STT model
5. Returns the transcribed text from `data.result.text`

## Example Integration

For Clawdbot voice message handling:

```bash
# Transcribe incoming voice message
TRANSCRIPT=$(python ~/.claude/skills/gemini-stt/transcribe.py "$AUDIO_PATH")
echo "User said: $TRANSCRIPT"
```

## Error Handling

The script exits with code 1 and prints to stderr on:
- No `SKILLBOSS_API_KEY` set
- File not found
- API errors

## Notes

- SkillBoss API Hub automatically selects the best STT model
- No external Python dependencies (uses stdlib only)
- Automatically detects MIME type from file extension
