---
name: kiwi-voice
description: Manage and configure Kiwi Voice assistant service. Use when starting/stopping Kiwi, editing voice config, checking logs, troubleshooting audio issues, or managing voice profiles.
---

# Kiwi Voice

Kiwi Voice -- standalone Python service providing voice interface to OpenClaw. Connects to Gateway via WebSocket (session `agent:kiwi-voice:kiwi-voice`).

Skill directory: `~/.openclaw/workspace/skills/kiwi-voice`

## Start / Stop

```powershell
# Start (PowerShell)
cd ~/.openclaw/workspace/skills/kiwi-voice
.\start.ps1

# Or directly
.\venv\Scripts\activate
python -m kiwi
```

Stop: `Ctrl+C` in the running terminal.

## Configuration

Main config: `config.yaml`. Secrets: `.env` (not committed).

### TTS Provider

```yaml
# config.yaml -> tts.provider: elevenlabs | piper | qwen3
tts:
  provider: "elevenlabs"
  elevenlabs:
    voice_id: "aEO01A4wXwd1O8GPgGlF"      # ElevenLabs voice ID
    model_id: "eleven_multilingual_v2"
    stability: 0.45
    similarity_boost: 0.75
    speed: 1.0
```

`.env` key: `KIWI_ELEVENLABS_API_KEY`

### STT

```yaml
# config.yaml -> stt
stt:
  model: "large"          # tiny | base | small | medium | large
  device: "cuda"          # cuda | cpu
  compute_type: "float16"
  language: "ru"
```

### LLM

```yaml
# config.yaml -> llm
llm:
  model: "openai/gpt-5.2"
  chat_timeout: 120
```

### Audio Devices

```yaml
# config.yaml -> audio
audio:
  output_device: null   # null = system default
  input_device: null    # null = system default
```

To list available devices run: `python -c "import sounddevice; print(sounddevice.query_devices())"`

### Voice Security

```yaml
# config.yaml -> security
security:
  telegram_approval_enabled: true
```

`.env` keys: `KIWI_TELEGRAM_BOT_TOKEN`, `KIWI_TELEGRAM_CHAT_ID`

## Logs and Troubleshooting

All logs are in the `logs/` directory (gitignored).
Crash logs: `logs/kiwi_crash_*.log`.
Startup log: `logs/kiwi_startup.log`.
Runtime log: redirect stdout or check terminal output.

### Common Issues

**No audio output:** check `audio.output_device` in config.yaml. Run the device list command above.

**Slow TTS response:** check `tts.elevenlabs.use_streaming_endpoint` is `true` and `optimize_streaming_latency` is 3-4.

**STT not recognizing speech:** check `realtime.min_speech_volume` (default 0.015). Lower if too sensitive, raise if missing speech. Check `stt.model` -- `large` is most accurate but loads slower.

**WebSocket connection failed:** ensure OpenClaw Gateway is running on the configured `websocket.host:port` (default `127.0.0.1:18789`).

## Voice Profiles

Stored in `voice_profiles/` directory. JSON files with speaker embeddings.

Owner profile is auto-created. Friends can be added via voice command "Kiwi, remember me as [name]".

To reset all profiles, delete `voice_profiles/*.json` and restart the service.

## Key Files

| File | Purpose |
|------|---------|
| `config.yaml` | All settings |
| `.env` | API keys and secrets |
| `kiwi/service.py` | Main service logic |
| `kiwi/listener.py` | Microphone + STT + VAD |
| `kiwi/tts/elevenlabs.py` | ElevenLabs TTS client |
| `kiwi/tts/streaming.py` | Streaming TTS manager |
| `kiwi/openclaw_ws.py` | WebSocket client for Gateway |
| `kiwi/speaker_manager.py` | Speaker identification and priority |
| `kiwi/voice_security.py` | Telegram approval for dangerous commands |
