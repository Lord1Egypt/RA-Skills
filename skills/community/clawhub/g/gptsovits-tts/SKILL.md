---
name: gptsovits-tts
description: High-quality Chinese TTS using GPT-SoVITS v2 Pro+ — convert text to natural-sounding speech with voice cloning support.
---

# GPT-SoVITS TTS

A production-ready text-to-speech skill that connects to a local GPT-SoVITS v2 Pro+ API server. Converts Chinese text to natural-sounding speech with a cloned reference voice. Designed for voice response automation, content narration, and AI voice applications.

## Features

- **Clean TTS pipeline**: Text → GPT-SoVITS API → WAV → MP3 (128kbps, 44100Hz, mono)
- **Voice cloning**: Uses a pre-recorded reference audio for consistent voice output
- **Configurable**: API URL, timeout, TTS parameters (speed, top_k, top_p, temperature, seed)
- **No GPU required**: Pure CPU inference, works on any machine (approx. 5-10s per sentence)

## Requirements

- **GPT-SoVITS v2 Pro+ API** running at `http://127.0.0.1:9880` (or set `GPT_SOVITS_API_URL`)
- **ffmpeg** installed and in PATH (for WAV→MP3 conversion)
- **Node.js** packages: `axios`

### Model files needed (on the API server side)

| Component | File | Size |
|-----------|------|------|
| s1 | s1v3.ckpt | 148MB |
| s2 | s2Gv2ProPlus.pth | 191MB |
| BERT | chinese-roberta-wwm-ext-large | 621MB |
| CNHuBERT | chinese-hubert-base | 180MB |
| Speaker Verification | pretrained_eres2netv2w24s4ep4.ckpt | 103MB |
| Reference Audio | ref_audio.wav | ~10-30s clean recording |

## Quick Start

### 1. Start GPT-SoVITS API

```bash
cd /path/to/GPT-SoVITS-CPUFast
conda activate GPTSoVits
python api_v2.py -a 127.0.0.1 -p 9880
```

### 2. Set reference audio

Place a clean `.wav` file (10-30 seconds of the target voice) at:
```
voice-clone/ref_audio.wav
```

### 3. Use the skill

```js
const tts = require('./skills/voice-clone');
const mp3 = await tts.speak("你好，欢迎使用GPT-SoVITS语音合成。", "output.mp3");
// Returns: "output.mp3"
```

## API

### `speak(text, outputPath, opts?)`

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| text | string | required | Chinese text to synthesize |
| outputPath | string | required | Output .mp3 file path |
| opts.topK | number | 15 | Top-K sampling |
| opts.topP | number | 0.7 | Top-P sampling |
| opts.temperature | number | 0.5 | Sampling temperature |
| opts.speed | number | 1.0 | Speed factor |
| opts.seed | number | -1 | Random seed (-1 = random) |

Returns: `Promise<string>` — path to the generated MP3 file.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| GPT_SOVITS_API_URL | http://127.0.0.1:9880 | GPT-SoVITS API base URL |
| GPT_SOVITS_API_TIMEOUT | 300000 | API request timeout (ms) |

## Integration

This skill is designed to be called from automation workflows:
- Voice reply for messaging bots (WeChat, Telegram, etc.)
- Content narration for video/audio production
- Voice response for IVR systems

## License

MIT
