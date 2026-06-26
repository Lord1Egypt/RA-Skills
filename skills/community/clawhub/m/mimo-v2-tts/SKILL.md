# Xiaomi MiMo-V2-TTS Skill

Text-to-speech using Xiaomi's MiMo-V2-TTS model. Supports emotional style control, Chinese dialects (Northeastern/Sichuan/Cantonese/Taiwanese), role-playing voices, and singing synthesis.

## When to Use
- User asks to convert text to speech / audio
- User mentions "read aloud", "TTS", "voice synthesis", "narrate"
- User wants specific voice styles, emotions, or dialects

## API Details
- **Platform**: https://platform.xiaomimimo.com
- **Base URL**: `https://api.xiaomimimo.com/v1`
- **Endpoint**: `/v1/chat/completions` (NOT `/audio/speech`)
- **Model**: `mimo-v2-tts`
- **Auth**: Bearer Token via `MIMO_API_KEY` env var

### Important: API Format
MiMo TTS uses the Chat Completions endpoint with special requirements:
- ❌ No `system` role allowed (returns error)
- ✅ Must include `assistant` role message (the text to synthesize)
- `user` message = style/voice instructions
- `assistant` message = text to be spoken
- Response: `choices[0].message.audio.data` contains base64-encoded audio

## Usage

```bash
python3 <skill_dir>/scripts/mimo_tts.py \
  --text "Hello, world!" \
  --output /tmp/openclaw/tts_output.mp3 \
  [--style "cheerful tone"] \
  [--speed 1.0] \
  [--format mp3] \
  [--api-key YOUR_KEY]
```

Set `MIMO_API_KEY` environment variable or pass `--api-key`.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| --text | ✅ | Text to synthesize (recommended < 5000 chars) |
| --output | ✅ | Output audio file path |
| --style | ❌ | Natural language style description |
| --speed | ❌ | Speech rate 0.5–2.0 (default 1.0) |
| --format | ❌ | mp3/wav/pcm/opus/flac (default mp3) |
| --api-key | ❌ | API Key (overrides env var) |

## Style Control Examples
- **Dialects**: `--style "speak in Cantonese"` / `"Sichuan dialect"` / `"Taiwanese accent"`
- **Emotions**: `--style "happy and excited"` / `"sad and gentle"` / `"start happy then turn melancholic"`
- **Characters**: `--style "news anchor"` / `"gentle older sister"`
- **Singing**: `--style "sing it"`
- **Combined**: `--style "Northeastern dialect, enthusiastic and bold"`

## Notes
- Pricing: Free during launch period (March 2026), may charge later
- Supports Chinese and English text
- Best results with Chinese text and style descriptions in Chinese
- Get API key at https://platform.xiaomimimo.com
