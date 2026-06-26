---
name: minimax-tts
description: Use MiniMax speech-2.8-hd model for high-quality text-to-speech synthesis. Supports multiple Chinese and English voices. Install when needed.
homepage: https://platform.minimax.io
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["python"]}}}
---

# MiniMax Text-to-Speech

Call via: `python scripts/minimax_media.py tts "<text>" [options]`

## Usage

```bash
python scripts/minimax_media.py tts "你好，這是語音測試。" --voice female-tianmei --speed 1.0
```

## Options

- `--voice`: Voice ID (see below)
- `--speed`: Speech speed 0.5 ~ 2.0 (default: 1.0)
- `--output`: Output MP3 file path

## Available Voices

| Voice ID | Language | Gender |
|----------|----------|--------|
| female-tianmei | Chinese | Female |
| male-qn-qingse | Chinese | Male |
| male-qn-jianbin | Chinese | Male |
| English_expressive_narrator | English | Male |

Returns: `{"audio_path": "...", "size_bytes": ..., "duration_hint": "..."}`

## Environment

- `MINIMAX_API_KEY` — required
- `MINIMAX_BASE_URL` — optional (default: https://api.minimax.io)
