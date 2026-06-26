# Local Setup

The simplest way to run Kiwi Voice — directly on your machine.

## Install

```bash
git clone https://github.com/ekleziast/kiwi-voice.git
cd kiwi-voice

python -m venv venv
source venv/bin/activate          # Linux/macOS
# source venv/Scripts/activate    # Windows/MSYS2

pip install -r requirements.txt
cp .env.example .env              # Edit with your settings
```

## Run

=== "Linux / macOS"

    ```bash
    python -m kiwi
    ```

=== "Windows (PowerShell)"

    ```powershell
    .\start.ps1
    ```

=== "Windows (batch)"

    ```
    start.bat
    ```

Dashboard: [http://localhost:7789](http://localhost:7789)

## Health Check

```bash
curl http://localhost:7789/api/status
```

Expected:

```json
{"state": "LISTENING", "is_running": true, ...}
```

## Logs

All logs go to the `logs/` directory:

| File | Content |
|------|---------|
| `logs/kiwi_startup.log` | Startup sequence |
| `logs/kiwi_crash_*.log` | Crash reports |

Runtime logs are printed to stdout. Use `KIWI_DEBUG=1` for verbose output.

## Troubleshooting

**No audio output:** Check `audio.output_device` in `config.yaml`. List devices:

```bash
python -c "import sounddevice; print(sounddevice.query_devices())"
```

**STT not recognizing speech:** Check `stt.model` — `large` is most accurate. Also check microphone input level and the energy threshold in audio config.

**WebSocket connection failed:** Make sure OpenClaw Gateway is running on the configured host and port (default: `127.0.0.1:18789`).

**Slow TTS:** Try switching to Kokoro ONNX (fast, free, local) or ElevenLabs (fast, cloud).
