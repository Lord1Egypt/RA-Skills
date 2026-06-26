---
name: minimax-media
description: Use MiniMax API for image generation and text-to-speech (TTS). Supports image-01 model for images and speech-2.8-hd for voice synthesis. Install when needed.
homepage: https://platform.minimax.io
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["python"]}}}
---

# MiniMax Media（Image Generation + TTS）

Call via: `python scripts/minimax_media.py`

## Image Generation

```bash
python scripts/minimax_media.py image "A cute cat"
```

Returns: `{"image_path": "...", "url": "...", "size_bytes": ...}`

## Text-to-Speech

```bash
python scripts/minimax_media.py tts "Hello, this is a test." --voice female-tianmei --speed 1.0
```

Available voices:
- `female-tianmei` (default, Chinese female)
- `male-qn-qingse` (Chinese male)
- `male-qn-jianbin` (Chinese male 2)
- `English_expressive_narrator` (English)

Speed: 0.5 ~ 2.0 (default: 1.0)

Returns: `{"audio_path": "...", "size_bytes": ..., "duration_hint": "..."}`

## Environment

- `MINIMAX_API_KEY` — required
- `MINIMAX_BASE_URL` — optional (default: https://api.minimax.io)
