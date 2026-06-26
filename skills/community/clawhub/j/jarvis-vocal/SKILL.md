---
name: jarvis-vocal
description: Authentic J.A.R.V.I.S. voice synthesis using Piper TTS with HuggingFace-trained model. Generates movie-accurate voice locally and can push to connected Android devices via OpenClaw nodes.
metadata:
  openclaw:
    emoji: "🎙️"
  credits:
    - name: "jgkawell"
      url: "https://huggingface.co/jgkawell/jarvis"
      note: "J.A.R.V.I.S. voice model trained on movie lines (MIT license)"
    - project: "Piper TTS"
      url: "https://github.com/rhasspy/piper"
      note: "Neural TTS engine"
---

# jarvis-vocal

Uses the authentic **J.A.R.V.I.S. voice model** from HuggingFace (trained on actual movie lines) via Piper TTS. No audio effects needed — the voice is naturally cinematic and British.

> Credit: Voice model by [jgkawell](https://huggingface.co/jgkawell/jarvis) — see the [discussion](https://huggingface.co/jgkawell/jarvis/discussions) for details on training and samples.

## Usage

Generate a WAV file:
```bash
{baseDir}/bin/jarvis-tts "Text to speak" ./output.wav
```

Stream directly to an Android device (if ADB connected):
```bash
{baseDir}/bin/jarvis-tts "Text to speak" - | adb push - /sdcard/Download/temp.wav
```

## Installation

### Prerequisites
```bash
pipx install piper-tts
sudo apt install ffmpeg  # or equivalent
```

### Install Voice Model
```bash
# Create voice directory
mkdir -p ~/.local/share/piper/voices/en_GB

# Download models via HuggingFace CLI
cd ~/.local/share/piper/voices/en_GB
hf download jgkawell/jarvis en/en_GB/jarvis/high/jarvis-high.onnx --local-dir .
hf download jgkawell/jarvis en/en_GB/jarvis/high/jarvis-high.onnx.json --local-dir .
# Optional: medium quality model
hf download jgkawell/jarvis en/en_GB/jarvis/medium/jarvis-medium.onnx --local-dir .
hf download jgkawell/jarvis en/en_GB/jarvis/medium/jarvis-medium.onnx.json --local-dir .
```

## Integration

Works with OpenClaw Android nodes via ADB over Tailscale. Use `jarvis-speak` wrapper for one-command push+play:
```bash
jarvis-speak "Systems at your service, Sir."
```

Or use streaming mode (faster, ephemeral):
```bash
jarvis-speak "Message" --stream
```

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| Model | `jarvis-high` | Voice quality: `high` (114MB) or `medium` (63MB) |
| Speed | 1.0 (native) | Piper length-scale — adjust for faster/slower speech |
| Volume | 1.0 | Post-processing volume boost |

Edit `jarvis-speak` script to change defaults.

## Troubleshooting

**"Model not found"** → Download models to `~/.local/share/piper/voices/en_GB/jarvis-*`

**ADB connection refused** → Ensure phone's ADB over WiFi is enabled and paired with laptop (port 5555)

**Audio doesn't play** → Check Android receives the file at `/sdcard/Download/jarvis-current.wav` and has a WAV-capable media player

## License

MIT — The voice model is MIT licensed by [jgkawell](https://huggingface.co/jgkawell/jarvis).

## Credits

- Voice model: [jgkawell/jarvis](https://huggingface.co/jgkawell/jarvis) on HuggingFace — trained on Marvel movie lines
- TTS engine: [Piper](https://github.com/rhasspy/piper) by Rhasspy
- Integration: OpenClaw by Aidan Park