# Installation

## Requirements

- **Python 3.10+**
- **FFmpeg** — for audio processing
- **[OpenClaw](https://github.com/openclaw/openclaw)** running locally
- **GPU with CUDA** recommended for STT and local TTS, but not required

## Clone & Install

=== "Linux / macOS"

    ```bash
    git clone https://github.com/ekleziast/kiwi-voice.git
    cd kiwi-voice

    python -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt
    ```

=== "Windows"

    ```bash
    git clone https://github.com/ekleziast/kiwi-voice.git
    cd kiwi-voice

    python -m venv venv
    venv\Scripts\activate

    pip install -r requirements.txt
    ```

## FFmpeg

=== "Linux"

    ```bash
    sudo apt install ffmpeg
    ```

=== "macOS"

    ```bash
    brew install ffmpeg
    ```

=== "Windows"

    Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH, or set `KIWI_FFMPEG_PATH` in `.env`.

## Environment File

```bash
cp .env.example .env
```

Edit `.env` with your API keys. All keys are optional — Kiwi works with free local providers out of the box:

```bash
# Optional: ElevenLabs for cloud TTS
KIWI_ELEVENLABS_API_KEY=sk-...

# Optional: Telegram bot for voice security approvals
KIWI_TELEGRAM_BOT_TOKEN=123456:ABC...
KIWI_TELEGRAM_CHAT_ID=123456789

# Optional: RunPod for Qwen3-TTS serverless
RUNPOD_API_KEY=...
RUNPOD_TTS_ENDPOINT_ID=...
```

!!! tip "Zero-cost setup"
    Kiwi works fully local and free with **Kokoro ONNX** (TTS) + **Faster Whisper** (STT) + **text** wake word engine. No API keys needed.

## Next Steps

- [Configuration](configuration.md) — customize `config.yaml`
- [First Run](first-run.md) — start Kiwi and register your voice
