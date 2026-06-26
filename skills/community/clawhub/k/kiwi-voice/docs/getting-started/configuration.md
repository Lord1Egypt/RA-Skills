# Configuration

Kiwi Voice is configured through two files:

| File | Purpose |
|------|---------|
| `config.yaml` | All settings — language, STT, TTS, wake word, security, API |
| `.env` | Secrets and provider overrides (API keys, tokens) |

**Precedence:** `config.yaml` → environment variables (`.env`) → hardcoded defaults.

## config.yaml

### Language

```yaml
language: "en"   # en, ru, es, pt, fr, it, de, tr, pl, zh, ja, ko, hi, ar, id
```

Controls all user-facing strings, STT language, TTS voice selection, wake word variants, and security patterns.

### Wake Word

```yaml
wake_word:
  engine: "text"             # text (fuzzy match) or openwakeword (ML model)
  keyword: "kiwi"
  model: "hey_jarvis"        # OpenWakeWord model name or path to .onnx
  threshold: 0.5             # Detection sensitivity (0.0–1.0)
```

See [Wake Word Detection](../features/wake-word.md) for details on both engines.

### Speech-to-Text

```yaml
stt:
  engine: "faster-whisper"   # faster-whisper, elevenlabs, or mlx-whisper
  model: "small"             # tiny, base, small, medium, large
  device: "cuda"             # cuda or cpu
  compute_type: "float16"    # float16 (GPU) or int8 (CPU)
  # ElevenLabs STT (cloud, uses same API key as TTS)
  elevenlabs:
    model_id: "scribe_v2"
    language_code: ""        # auto-detect if empty
```

!!! tip "Model size tradeoff"
    `small` is the sweet spot — fast with good accuracy. Use `large` for best accuracy (slower startup), `tiny` for minimal resources.

See [STT Engines](../features/stt-engines.md) for a full comparison.

### Text-to-Speech

```yaml
tts:
  provider: "kokoro"         # kokoro, piper, qwen3, elevenlabs
  elevenlabs:
    voice_id: "aEO01A4wXwd1O8GPgGlF"
    model_id: "eleven_multilingual_v2"
    stability: 0.45
    similarity_boost: 0.75
    speed: 1.0
  kokoro:
    voice: "af_heart"        # 14 voices available
    speed: 1.0
  piper:
    model: "en_US-lessac-medium"
  qwen3:
    backend: "local"         # local or runpod
```

See [TTS Providers](../features/tts-providers.md) for a full comparison.

### Speaker Priority

```yaml
speaker_priority:
  owner:
    name: "Owner"            # Change to your name
```

### Voice Security

```yaml
security:
  telegram_approval_enabled: true
```

### LLM

```yaml
llm:
  model: "openai/gpt-4o"
  chat_timeout: 120
```

### Audio Devices

```yaml
audio:
  output_device: null        # null = system default
  input_device: null         # null = system default
```

List available devices:

```bash
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### REST API

```yaml
api:
  enabled: true
  host: "0.0.0.0"
  port: 7789
```

### Web Audio

```yaml
web_audio:
  enabled: true
  sample_rate: 16000
  max_clients: 3
```

### Home Assistant

```yaml
homeassistant:
  enabled: true
  url: "http://homeassistant.local:8123"
  token: ""                  # Long-Lived Access Token
```

### Souls (Personalities)

```yaml
souls:
  default: "mindful-companion"
  nsfw:
    model: "openrouter/mistralai/mistral-7b-instruct"
    session: "kiwi-nsfw"
```

## Environment Variables

All settings can be overridden via environment variables in `.env`:

| Variable | Description |
|----------|-------------|
| `KIWI_LANGUAGE` | Override language (`en`, `ru`, etc.) |
| `KIWI_TTS_PROVIDER` | Override TTS provider (`kokoro`, `piper`, `qwen3`, `elevenlabs`) |
| `KIWI_ELEVENLABS_API_KEY` | ElevenLabs API key |
| `RUNPOD_API_KEY` | RunPod API key (Qwen3-TTS serverless) |
| `RUNPOD_TTS_ENDPOINT_ID` | RunPod endpoint ID |
| `KIWI_TELEGRAM_BOT_TOKEN` | Telegram bot token (voice security) |
| `KIWI_TELEGRAM_CHAT_ID` | Telegram chat ID for approvals |
| `KIWI_WAKE_ENGINE` | Override wake word engine (`text`, `openwakeword`) |
| `KIWI_WAKE_MODEL` | Override OpenWakeWord model |
| `KIWI_WAKE_THRESHOLD` | Override detection threshold |
| `KIWI_STT_ENGINE` | Override STT engine (`faster-whisper`, `elevenlabs`, `mlx-whisper`) |
| `KIWI_FFMPEG_PATH` | Custom FFmpeg path |
| `KIWI_DEBUG` | Enable debug logging |
| `LLM_MODEL` | Override LLM model |

See `.env.example` in the repository for the full list.
