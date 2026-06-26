---
name: neomano-tts
description: Text-to-speech (TTS) via ElevenLabs. Use when the user asks to reply with voice/audio, generate a spoken version of some text, or asks for “voz”, “nota de voz”, or TTS.
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["python3"],"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

## Human setup (one-time)

1. Create or edit `~/.openclaw/.env` on the machine running OpenClaw.
2. Add your credentials (do **not** commit these):

```bash
ELEVENLABS_API_KEY=your_elevenlabs_key
# Optional (recommended): default voice
ELEVENLABS_VOICE_ID=your_voice_id
```

3. Restart the OpenClaw gateway (so the service environment picks up changes).

## Inputs to collect (if missing)

- Text to speak.
- Optional: `voiceId` (ElevenLabs voice id). If not provided, use the default.
- Optional: output format (`mp3` default).

## Requirements (credentials)

This skill does **not** embed secrets. Credentials must be provided at runtime:

- `ELEVENLABS_API_KEY` (required)
  - Recommended: put it in `~/.openclaw/.env` on the machine running the gateway.
- `ELEVENLABS_VOICE_ID` (optional but recommended)
  - If omitted, you must pass `--voice-id` when calling the script.

## Example user prompts (to trigger this skill)

- "Reply with a voice note saying: …"
- "Generate audio (ElevenLabs) for: …"
- "Envíame una nota de voz que diga: …"

## Workflow

1. Choose output path under the workspace, e.g. `./media/elevenlabs-tts/<timestamp>.mp3`.
2. Run:

```bash
python3 {baseDir}/scripts/tts.py --text "..." --out "/abs/path/to/file.mp3" [--voice-id "..."]
```

3. Confirm with a short message including the output file path.

## Defaults

- No voice is hardcoded. Set `ELEVENLABS_VOICE_ID` (recommended) or pass `--voice-id`.
- Model: `eleven_multilingual_v2`.
