# jarvis-vocal

Authentic J.A.R.V.I.S. voice synthesis for OpenClaw — powered by Piper TTS and a HuggingFace-trained model.

## Features

- 🎙️ **Movie-accurate voice** — Trained on actual J.A.R.V.I.S. lines from Marvel films
- ⚡ **Fast & lightweight** — Piper ONNX model (~100-114MB), generates speech in <1s
- 📱 **Wireless to Android** — Push voice messages to any OpenClaw-connected Android device via ADB over Tailscale
- 🎵 **Streaming support** — Optional direct streaming (no file storage)
- 🛠️ **Customizable** — Adjust speed, noise scale, and model quality

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

# Download models (via HuggingFace)
cd ~/.local/share/piper/voices/en_GB
hf download jgkawell/jarvis en/en_GB/jarvis/high/jarvis-high.onnx --local-dir .
hf download jgkawell/jarvis en/en_GB/jarvis/high/jarvis-high.onnx.json --local-dir .
hf download jgkawell/jarvis en/en_GB/jarvis/medium/jarvis-medium.onnx --local-dir .
hf download jgkawell/jarvis en/en_GB/jarvis/medium/jarvis-medium.onnx.json --local-dir .
```

## Usage

### Basic TTS Generation
```bash
jarvis-tts "Systems at your service, Sir." /tmp/jarvis.wav
```

### Push to Android Device
```bash
# One-command: generate + push + play on connected Android
jarvis-speak "Good evening, Sir. All systems operational."
```

### Streaming Mode (Faster, Ephemeral)
```bash
jarvis-speak "Incoming message" --stream
```

## OpenClaw Integration

Once your Android device is paired with OpenClaw and ADB over Tailscale is configured (port 5555), you can trigger voice announcements from any OpenClaw session:

```
You: Jarvis, announce: System reboot in 30 seconds
Jarvis: [plays voice on your phone]
```

## How It Works

1. **Piper TTS** generates audio from text using the `jgkawell/jarvis` ONNX model
2. **ADB over Tailscale** sends the audio to your Android device (100.69.58.88:5555)
3. **Android MediaPlayer** plays the WAV file through your phone speakers
4. **Auto-cleanup** deletes the temporary file after playback

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

MIT — The voice model is MIT licensed by [jgkawell](https://huggingface.co/jgkawell).

## Credits

- Voice model: [jgkawell/jarvis](https://huggingface.co/jgkawell/jarvis) on HuggingFace
- TTS engine: [Piper](https://github.com/rhasspy/piper) by Rhasspy
- Integration: OpenClaw by Aidan Park