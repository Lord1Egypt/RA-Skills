---
name: local-tts
description: Local text-to-speech using Qwen3-TTS with mlx_audio (macOS Apple Silicon) or qwen-tts (Linux/Windows). Privacy-first offline TTS with natural, realistic voice cloning and voice design. Use for local, secure, high-quality multilingual speech synthesis.
license: MIT
---

# Local TTS with Qwen3-TTS

**Privacy-First | Offline | High-Quality | Natural Real Voices**

Local text-to-speech synthesis using Qwen3-TTS models. Your text never leaves your machine.

## Why Local TTS?

Unlike cloud TTS (Google, AWS, Azure), **local-tts** ensures:
- **Zero data transmission** - 100% on-device processing
- **Works offline** - No network required
- **No API keys** - No external dependencies
- **GDPR/HIPAA friendly** - Simplified compliance

See [privacy & security details](references/privacy_security.md).

## Platform Overview

| Platform | Backend | Installation | Best For |
|----------|---------|--------------|----------|
| macOS (Apple Silicon) | `mlx_audio` | `pip install mlx-audio` | M1/M2/M3/M4 Macs |
| Linux/Windows | `qwen-tts` | `pip install qwen-tts` | CUDA GPUs |

## Quick Start

### macOS

```bash
pip install mlx-audio
brew install ffmpeg

# Natural female voice
python -m mlx_audio.tts.generate \
    --text "Hello world" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
    --voice Chelsie
```

### Linux/Windows

```bash
pip install qwen-tts

# With optimizations (FlashAttention, bfloat16, auto-device)
python scripts/tts_linux.py "Hello world" --female
```

## Key Concepts

### `--voice` vs `--instruct` (Important)

| Model | `--voice` | `--instruct` | Notes |
|-------|-----------|--------------|-------|
| **CustomVoice** | Select preset voice | Add style/emotion | **Can use together** - voice + style control |
| **VoiceDesign** | N/A | Create voice from description | `--instruct` only |
| **Base** | N/A | N/A | For voice cloning with `--ref_audio` |

**CustomVoice with style control:**
```bash
python -m mlx_audio.tts.generate \
    --text "Hello there!" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
    --voice Serena \
    --instruct "excited and enthusiastic"
```

### 9 Preset Voices (Open Source CustomVoice)

| Voice | Gender | Language | Character |
|-------|--------|----------|-----------|
| Chelsie | Female | English (American) | Gentle, empathetic |
| Serena | Female | English | Warm, gentle |
| Ono Anna | Female | Japanese | Playful |
| Sohee | Female | Korean | Warm |
| Aiden | Male | English (American) | Sunny |
| Dylan | Male | English | Natural |
| Eric | Male | English | Real |
| Ryan | Male | English | Natural |
| Uncle Fu | Male | Chinese | Youthful Beijing |

**Defaults:** Female=`Serena`, Male=`Aiden`

## Usage Examples

### CustomVoice (Preset Voices)

```bash
# Natural female
python -m mlx_audio.tts.generate \
    --text "Your text" --voice Serena --lang_code en \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit

# Real male
python -m mlx_audio.tts.generate \
    --text "Your text" --voice Aiden --lang_code en \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit
```

### VoiceDesign (Text-Based)

```bash
python -m mlx_audio.tts.generate \
    --text "Hello" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit \
    --instruct "A warm female voice, professional and clear"
```

### Long Text Generation

For long text, increase `--max_tokens` and enable `--join_audio` (macOS/MLX only):

```bash
python -m mlx_audio.tts.generate \
    --text "Your very long text here..." \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
    --voice Serena \
    --max_tokens 4096 \
    --join_audio \
    --output long_audio.wav
```

### Voice Cloning

```bash
python -m mlx_audio.tts.generate \
    --text "Cloned voice speaking" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit \
    --ref_audio sample.wav --ref_text "Sample transcript"
```

## Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `--text` | Text to speak | Required |
| `--model` | Model ID | See table below |
| `--voice` | Preset voice (CustomVoice) | Chelsie, Serena, Aiden, Ryan... |
| `--instruct` | Voice description (VoiceDesign) or style/emotion (CustomVoice) | e.g., "excited", "calm", "professional" |
| `--speed` | Speaking rate | 0.5-2.0 (default: 1.0) |
| `--pitch` | Voice pitch | 0.5-2.0 (default: 1.0) |
| `--lang_code` | Language | en, cn, ja, ko, de, fr... |
| `--ref_audio` | Reference for cloning | File path |
| `--output` | Output file | Path (auto-generated if omitted) |
| `--max_tokens` | Max generation tokens | Integer (default: 2048) - Increase for long text |
| `--join_audio` | Merge audio segments | `true` (default) or `false` - Recommended for long text |

## Models

| Model | Size | Purpose |
|-------|------|---------|
| `Qwen3-TTS-12Hz-1.7B-CustomVoice` | 1.7B | 9 preset voices + style control |
| `Qwen3-TTS-12Hz-1.7B-VoiceDesign` | 1.7B | Text-based voice creation |
| `Qwen3-TTS-12Hz-1.7B-Base` | 1.7B | Voice cloning |
| `Qwen3-TTS-12Hz-0.6B-*` | 0.6B | Lightweight versions |

macOS: Add `mlx-community/` prefix (e.g., `mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit`)

## Scripts

- `scripts/tts_macos.py` - macOS wrapper
- `scripts/tts_linux.py` - Linux/Windows wrapper with optimizations

## Optimizations (Linux/Windows)

`tts_linux.py` automatically enables:
- **FlashAttention** - Faster, less memory
- **bfloat16** - Better precision
- **Auto device** - CUDA → CPU fallback
- **Mixed precision** - Speed + quality

## Troubleshooting

| Issue | Solution |
|-------|----------|
| macOS: Model not found | Use `mlx-community/` prefix |
| macOS: Audio format | `brew install ffmpeg` |
| Linux: CUDA OOM | Use `0.6B` models |
| Linux: Slow | Check CUDA: `torch.cuda.is_available()` |

## References

- [macOS Details](references/macos_mlx_audio.md)
- [Linux/Windows Details](references/linux_windows_transformers.md)
- [Privacy & Security](references/privacy_security.md)

## Version

**1.0.0** - See [VERSION](VERSION) and [package.json](package.json)
