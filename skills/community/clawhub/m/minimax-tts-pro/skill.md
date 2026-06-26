---
name: minimax-tts
version: 1.0.0
description: "MiniMax Text-to-Speech synthesis using the HTTP REST API. Generates high-quality audio from text in 40+ languages with ultra-realistic voices. Use when the user wants to convert text to speech, create voiceovers, generate narrated audio content, or use MiniMax TTS voices. Supports streaming and non-streaming modes, multiple audio formats (mp3, wav, pcm), and voice effects. Triggered by: text to speech, TTS, text to audio, MiniMax TTS, generate voice, voiceover, read this aloud, text to voice"
---

# MiniMax TTS

MiniMax Text-to-Speech via HTTP REST API. Supports streaming and non-streaming, 40+ languages, 200+ voices.

## API Details

- **Endpoint**: `POST https://api.minimax.io/v1/t2a_v2`
- **Alt endpoint (lower latency)**: `POST https://api-uw.minimax.io/v1/t2a_v2`
- **Auth**: Bearer token via `MINIMAX_API_KEY` env var
- **Content-Type**: `application/json`

## Quick Usage

```bash
uv run python scripts/tts.py --text "Hello world" --voice English_expressive_narrator --model speech-2.8-hd --output hello.mp3
```

## Scripts

- `scripts/tts.py` — Core TTS script. Run with `--help` for full options.

## Models

| Model | Description |
|-------|-------------|
| `speech-2.8-hd` | Ultra-realistic, supports sound tags |
| `speech-2.8-turbo` | Fast + natural flow |
| `speech-2.6-hd` | Low latency, enhanced naturalness |
| `speech-2.6-turbo` | Fast, affordable |
| `speech-02-hd` | Superior rhythm, high similarity |
| `speech-02-turbo` | Superior rhythm, multilingual |

## Output Formats

- `mp3` (default), `wav`, `pcm`
- Sample rates: `32000` (default), `16000`, `24000`, `48000`
- Bitrate: `128000` (default), `64000`, `32000`

## Languages

40+ languages including: English, Chinese (Mandarin/Cantonese), Japanese, Korean, Spanish, French, German, Portuguese, Arabic, Russian, Hindi, Thai, Vietnamese, Turkish, Dutch, Polish, Italian, Indonesian, Malay, Persian, Swedish, Norwegian, Danish, Finnish, Hebrew, Romanian, Greek, Czech, Hungarian, Tamil, Afrikaans, and more.

## Voices

Key English voices:
- `English_expressive_narrator` — Default expressive narrator
- `English_radiant_girl` — Radiant female
- `English_magnetic_voiced_man` — Magnetic male voice
- `English_Aussie_Bloke` — Australian male
- `English_Whispering_girl` — Whispering female
- `English_PlayfulGirl` — Playful female
- `English_Comedian` — Comedic voice
- `English_AnimeCharacter` — Female anime narrator

For full voice list (200+ voices across all languages), see `references/voices.md`.

## Sound Tags (speech-2.8-hd only)

Use XML-like tags for breathing, pauses, expression:
- `(sighs)` — breathing sound
- `(laughs)` — laughter
- `(coughs)` — coughing
- `[laughs]` — laughing
- `...` or `(pause:500)` — pause in ms
- `<emphasis>important</emphasis>` — emphasis
- `<spell-out>A-P-I</spell-out>` — spell out letters

## Script Usage

```
uv run python scripts/tts.py --text "Your text here" [options]

Options:
  --text TEXT              Text to synthesize (required)
  --model MODEL           Model: speech-2.8-hd (default), speech-2.8-turbo, speech-2.6-hd, etc.
  --voice VOICE_ID        Voice ID (default: English_expressive_narrator)
  --speed SPEED           Speed 0.5-2.0 (default: 1.0)
  --pitch PITCH           Pitch -3 to 3 (default: 0)
  --vol VOLUME            Volume 0-10 (default: 1)
  --language_boost LANG   Language boost: auto (default), or specific lang e.g. en, zh
  --output_format FORMAT  hex (default) or raw (mp3/wav bytes returned directly)
  --format AUDIO_FORMAT   mp3 (default), wav, pcm
  --sample_rate RATE      32000 (default), 16000, 24000, 48000
  --bitrate BITRATE       128000 (default), 64000, 32000
  --stream                Enable streaming mode (returns chunks as they generate)
  --output FILE           Output file path (default: minimax_tts_output.mp3)
  --api_url URL           Override API URL
  --api_key KEY           Override API key (reads MINIMAX_API_KEY env if not set)
```

## Streaming Mode

```bash
uv run python scripts/tts.py --text "Hello, streaming audio." --stream --output stream_output.mp3
```

## Examples

```bash
# Basic
uv run python scripts/tts.py --text "The quick brown fox jumps over the lazy dog."

# Different voice
uv run python scripts/tts.py --text "Bonjour le monde" --voice French_Standard_Female --model speech-2.6-turbo

# Streaming
uv run python scripts/tts.py --text "This is streaming audio" --stream --output streaming.mp3

# With sound tags (expressive)
uv run python scripts/tts.py --text "Hello(sighs)... what a beautiful day(laughs)!" --voice English_expressive_narrator --model speech-2.8-hd
```
