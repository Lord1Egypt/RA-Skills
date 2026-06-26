<p align="center">
  <a href="https://kiwi-voice.com">
    <img src="https://kiwi-voice.com/assets/og-image.svg" width="600" alt="Kiwi Voice — Open-Source Voice Interface for AI Agents">
  </a>
</p>

<h1 align="center">Kiwi Voice</h1>

<p align="center">
  <strong>OpenClaw voice assistant — ML wake word, speaker ID, voice-gated security, multi-provider TTS, and Apple Silicon support</strong>
</p>

<p align="center">
  <a href="https://github.com/ekleziast/kiwi-voice/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+"></a>
  <a href="https://github.com/openclaw/openclaw"><img src="https://img.shields.io/badge/backend-OpenClaw-orange.svg" alt="OpenClaw"></a>
  <br>
  <a href="https://kiwi-voice.com"><strong>Website</strong></a> &middot;
  <a href="https://docs.kiwi-voice.com"><strong>Documentation</strong></a> &middot;
  <a href="https://github.com/ekleziast/kiwi-voice/issues">Issues</a> &middot;
  <a href="https://docs.openclaw.ai">OpenClaw Docs</a>
</p>

---

## What is Kiwi Voice?

Kiwi Voice is a real-time voice interface that turns [OpenClaw](https://github.com/openclaw/openclaw) into a hands-free assistant. It captures audio from your microphone, detects the wake word via ML model or text matching, recognizes speech locally via Faster Whisper (or MLX Whisper on Apple Silicon), identifies *who* is speaking, enforces voice-based security policies, talks to any LLM through OpenClaw's WebSocket gateway, and speaks the response back through one of five TTS providers — all in a continuous loop.

Think of it as Alexa/Siri, but self-hosted, privacy-first, and plugged into your own AI stack.

### Key Features

| Feature | Description |
|---------|-------------|
| 🗣️ **Wake Word** | Text-based fuzzy matching or **ML detection via OpenWakeWord** — low-latency ONNX model on raw audio (~2% CPU) |
| 🎭 **Speaker ID** | Voiceprint recognition via pyannote embeddings — knows who's talking |
| 🔐 **Voice Security** | Priority hierarchy (Owner → Friend → Guest → Blocked) with Telegram approval for dangerous commands |
| 🔊 **Multi-Provider TTS** | ElevenLabs (cloud), Piper (local/free), Qwen3-TTS (local GPU / RunPod), **Kokoro ONNX** (local/free, 14 voices) |
| ⚡ **Streaming TTS** | Sentence-aware chunking — starts speaking before the LLM finishes |
| 🛑 **Barge-In** | Interrupt the assistant mid-sentence by speaking over it |
| 🧠 **Auto-Learning** | Automatically remembers new voices after first interaction |
| 🔌 **WebSocket** | Native OpenClaw Gateway v3 protocol with delta/final streaming |
| 🌍 **Multi-Language** | Built-in i18n with YAML locale files — switch language with a single config field |
| 🍎 **MLX Whisper** | Optional Apple Silicon optimized STT via Lightning Whisper MLX (~10x faster on M-series) |
| 🌐 **Web Dashboard** | Real-time glassmorphism dashboard with live status, event log, controls, and personality switching |
| 🎙️ **Web Microphone** | Talk to Kiwi from any browser — WebSocket audio streaming with AudioWorklet, no local mic setup needed |

## Architecture

```
Mic → [OpenWakeWord OR VAD + Energy Detection]
  → Faster Whisper STT (or MLX Whisper on Apple Silicon)
  → Wake Word Check (text fuzzy match or ML pre-detection)
  → Speaker ID (pyannote) → Priority Gate → Voice Security
  → OpenClaw Gateway (WebSocket) → LLM response stream
  → Real-time streaming TTS → Speaker Output (with barge-in)
  → Back to listening
```

## Quick Start

### Requirements

- **Python 3.10+**
- **FFmpeg** (for audio processing)
- **[OpenClaw](https://github.com/openclaw/openclaw)** running locally
- **GPU with CUDA** recommended (for STT & local TTS), but not required

### Installation

```bash
git clone https://github.com/ekleziast/kiwi-voice.git
cd kiwi-voice

python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Fill in your API keys (ElevenLabs, RunPod, Telegram — all optional)
```

Edit `config.yaml` to match your setup:

```yaml
# Language: controls UI strings, STT, TTS, wake word, and command patterns
language: "ru"               # ru | en (add more in kiwi/locales/)

# TTS provider: elevenlabs | piper | qwen3 | kokoro
tts:
  provider: "piper"          # Free, local, no API key needed

# STT engine
stt:
  engine: "faster-whisper"   # faster-whisper | mlx-whisper | elevenlabs
  model: "small"             # small = fast, large = accurate
  device: "cuda"             # cuda | cpu

# Wake word
wake_word:
  engine: "text"             # text (fuzzy match) | openwakeword (ML model)
  keyword: "kiwi"
  model: "hey_jarvis"        # OpenWakeWord model (built-in or path to .onnx)
  threshold: 0.5             # Detection sensitivity (0.0–1.0)

# Owner name (used for voice commands like "I'm <name>")
speaker_priority:
  owner:
    name: "Owner"            # Change to your name
```

### Pair with OpenClaw Gateway (first time only)

On first launch, Kiwi registers as a new device with the Gateway. You need to **approve the pairing request** before it can connect:

1. **Start Kiwi** in one terminal:
   ```bash
   python -m kiwi
   ```

2. **In a second terminal**, approve the pending device:
   ```bash
   openclaw devices list      # see pending requests
   openclaw devices approve   # approve the latest one
   ```

Kiwi will automatically reconnect once approved. This is a one-time step — the device identity is saved to `device-identity.json` and persists across restarts.

> **Note:** If you skip device pairing, Kiwi will fall back to OpenClaw CLI mode, which is functional but slower due to process spawning overhead. WebSocket pairing is recommended for real-time voice interaction.

### Run

```bash
python -m kiwi
```

Or use the launcher scripts:

```bash
# Windows
start.bat
.\start.ps1

# Linux / macOS
python -m kiwi
```

## STT Engines

| Engine | Quality | Latency | Cost | Local | GPU |
|--------|---------|---------|------|-------|-----|
| **Faster Whisper** | Excellent | ~1–3s | Free | Yes | Optional (CUDA) |
| **ElevenLabs** | Excellent | ~0.3–0.5s | ~$0.018/min | No | No |
| **MLX Whisper** | Excellent | ~0.5–1s | Free | Yes | Apple Silicon |

Switch engines in `config.yaml` or via environment variable:

```bash
KIWI_STT_ENGINE=elevenlabs python -m kiwi
```

## TTS Providers

| Provider | Quality | Latency | Cost | Local GPU |
|----------|---------|---------|------|-----------|
| **ElevenLabs** | Excellent | ~0.3–0.5s | ~$0.30/1K chars | No |
| **Qwen3-TTS (local)** | High | ~1–3s | Free | Yes (CUDA) |
| **Qwen3-TTS (RunPod)** | High | ~2–5s | ~$0.0003/sec | No |
| **Kokoro ONNX** | High | <0.5s | Free | No |
| **Piper** | Good | <0.5s | Free | No |

Switch providers in `config.yaml` or via environment variable:

```bash
KIWI_TTS_PROVIDER=kokoro python -m kiwi
```

> **Kokoro ONNX** — free, fully local TTS with 14 voices at 24kHz. Models auto-download on first use (~340MB). Supports English, Japanese, Chinese, Korean, and several European languages. Russian is not yet supported.

## OpenWakeWord (ML Wake Word Detection)

Instead of running full Whisper transcription to detect the wake word, you can use **OpenWakeWord** — a small ONNX model (~10MB) that listens to raw audio in real time with ~80ms latency and ~2% CPU usage.

```yaml
wake_word:
  engine: "openwakeword"
  model: "hey_jarvis"        # Built-in: hey_jarvis, alexa, hey_mycroft
  threshold: 0.5
```

**Train a custom wake word** (e.g. "hey kiwi") using Google Colab — no voice recordings needed:
```bash
python scripts/train_wake_word.py --phrase "hey kiwi"
```

## Voice Security

Kiwi identifies speakers by voiceprint and enforces a priority hierarchy:

```
OWNER (priority 0)   — Full access, cannot be blocked
FRIEND (priority 1)  — Dangerous commands require Telegram approval
GUEST (priority 2)   — All sensitive commands require approval
BLOCKED (priority 99) — Completely ignored
```

### Voice Commands

| Command | Action |
|---------|--------|
| *"Kiwi, remember my voice"* | Register your voiceprint as owner |
| *"Kiwi, this is my friend [name]"* | Add someone as a friend |
| *"Kiwi, block them"* | Block the last speaker |
| *"Kiwi, who is speaking?"* | Identify the current speaker |
| *"Kiwi, what voices do you know?"* | List all known voiceprints |

> 💡 Voice commands are language-dependent. Set `language` in `config.yaml` to match your locale. See `kiwi/locales/*.yaml` for the full command lists.

### Two-Layer Security

**Pre-filter (Kiwi)** — catches dangerous commands *before* they reach the LLM:
- Regex-based `DangerousCommandDetector` classifies commands as SAFE / WARNING / DANGEROUS / CRITICAL
- Non-owner actionable commands are held until owner approves (by voice or Telegram)

**Post-filter (OpenClaw)** — catches dangerous shell commands the LLM tries to execute:
- When the OpenClaw agent calls the `exec` tool, the Gateway broadcasts an `exec.approval.requested` event
- Kiwi subscribes to this event, announces the command to the owner via voice
- Owner approves/denies by voice ("allow" / "deny") or via Telegram inline buttons
- Decision is sent back to OpenClaw via `exec.approval.resolve`
- Auto-deny on timeout (55s) if no response

This means even if a voice command passes the pre-filter, the actual shell execution still requires approval through OpenClaw's own security layer.

### Telegram Approval

When a non-owner speaker issues a potentially dangerous command, Kiwi sends a confirmation request to the owner via Telegram. The owner can approve or deny it from their phone. Telegram is also used as a secondary channel for OpenClaw exec approvals.

Set `KIWI_TELEGRAM_BOT_TOKEN` and `KIWI_TELEGRAM_CHAT_ID` in `.env` to enable.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `KIWI_ELEVENLABS_API_KEY` | ElevenLabs API key |
| `RUNPOD_API_KEY` | RunPod API key (for Qwen3-TTS serverless) |
| `RUNPOD_TTS_ENDPOINT_ID` | RunPod endpoint ID |
| `KIWI_TELEGRAM_BOT_TOKEN` | Telegram bot token (voice security) |
| `KIWI_TELEGRAM_CHAT_ID` | Telegram chat ID for approval messages |
| `KIWI_TTS_PROVIDER` | Override TTS provider (`elevenlabs`, `piper`, `qwen3`, `kokoro`) |
| `KIWI_WAKE_ENGINE` | Override wake word engine (`text`, `openwakeword`) |
| `KIWI_WAKE_MODEL` | Override OpenWakeWord model name or path |
| `KIWI_WAKE_THRESHOLD` | Override OpenWakeWord detection threshold |
| `KIWI_STT_ENGINE` | Override STT engine (`faster-whisper`, `mlx-whisper`) |
| `KIWI_FFMPEG_PATH` | Custom FFmpeg path |
| `KIWI_LANGUAGE` | Override language/locale (`ru`, `en`, etc.) |
| `KIWI_DEBUG` | Enable debug logging |
| `LLM_MODEL` | Override LLM model |

See `.env.example` for the full list.

## Development

```bash
# Run tests
pytest tests/

# Code conventions:
# - Logging: kiwi_log("TAG", "message", level="INFO") — never print()
# - Paths: PROJECT_ROOT from kiwi package
# - Optional modules: try/except + *_AVAILABLE flags
# - Threads: daemon threads + crash protection
# - GPU: auto-detect CUDA with CPU fallback
```

## Multi-Language Support

Kiwi uses YAML-based locale files in `kiwi/locales/`. All user-facing strings, voice commands, wake word variants, hallucination filters, and security patterns are loaded from locale files.

**Switch language:**
```yaml
# config.yaml
language: "en"   # or "ru", etc.
```

**Add a new language:**
1. Copy `kiwi/locales/en.yaml` to `kiwi/locales/{lang}.yaml`
2. Translate all strings
3. Set `language: "{lang}"` in `config.yaml`

Currently shipped — **15 languages:**

| | | | |
|---|---|---|---|
| `ru` Russian | `en` English | `es` Spanish | `pt` Portuguese |
| `fr` French | `it` Italian | `de` German | `tr` Turkish |
| `pl` Polish | `zh` Chinese | `ja` Japanese | `ko` Korean |
| `hi` Hindi | `ar` Arabic | `id` Indonesian | |

## Soul System (Personalities)

Kiwi supports dynamic personality switching via markdown-based "souls" in `kiwi/souls/`. Each soul defines a system prompt overlay that shapes how Kiwi responds.

**Built-in souls:** Mindful Companion (default), Storyteller, Comedian, Hype Person, Siren (NSFW)

The base system prompt is loaded from `SOUL.md` in the project root. Soul personalities are layered on top of it.

Switch via voice command, Web UI (click the card), or API:
```bash
curl -X POST http://localhost:7789/api/soul -d '{"soul_id": "comedian"}'
```

The Siren (NSFW) soul routes to a separate OpenClaw agent with its own LLM model, configured in `config.yaml`:
```yaml
souls:
  default: "mindful-companion"
  nsfw:
    model: "openrouter/mistralai/mistral-7b-instruct"
    session: "kiwi-nsfw"
```

## REST API & Web Dashboard

Kiwi includes a built-in REST API and a real-time web dashboard.

```bash
# Starts automatically with the service
http://localhost:7789/
```

<p align="center">
  <img src="docs/dashboard.png" width="720" alt="Kiwi Voice Dashboard">
</p>

**Dashboard features:**
- **Live state orb** — animated indicator that changes color and pulse speed with assistant state (idle / listening / thinking / speaking)
- **Real-time event log** — terminal-style feed of all system events via WebSocket
- **Personality cards** — horizontal carousel with holographic accents; click to activate, NSFW souls highlighted in ruby
- **Speaker management** — table with voiceprint priority badges, block/unblock/delete actions
- **Controls** — stop playback, reset context, restart/shutdown, TTS test
- **Language switcher** — change locale on the fly
- **Web Microphone** — talk to Kiwi directly from the browser via WebSocket audio streaming

**API endpoints:** `/api/status`, `/api/config`, `/api/speakers`, `/api/languages`, `/api/souls`, `/api/soul`, `/api/tts/test`, `/api/stop`, `/api/reset-context`, `/api/restart`, `/api/shutdown`, `/api/audio` (WebSocket for browser mic), plus `/api/events` for real-time event streaming.

Configure in `config.yaml`:
```yaml
api:
  enabled: true
  host: "0.0.0.0"
  port: 7789
```

### API Authentication

By default the API is open (no auth). To secure it, enable token-based authentication with scopes:

```yaml
api:
  auth:
    enabled: true
    tokens:
      - token: "your-secret-token-here"
        name: "Home Assistant"
        scopes: ["read", "control", "tts"]
      - token: "admin-token-here"
        name: "Admin"
        scopes: ["read", "control", "tts", "speakers", "admin"]
```

Each token gets a set of scopes that control what it can access:

| Scope | Allows |
|-------|--------|
| `read` | GET endpoints — status, config, speakers, languages, souls |
| `control` | POST stop, reset-context, language, soul; PATCH config |
| `tts` | POST tts/test — speak arbitrary text |
| `speakers` | DELETE/block/unblock speaker profiles |
| `admin` | POST restart, shutdown |

Requests must include `Authorization: Bearer <token>`. Static files (`/`, `/static/*`) are always open.

Use `GET /api/auth/scopes` to discover what scopes a token has.

Override via env var: `KIWI_API_AUTH_ENABLED=true`

> **CLI mode caveat:** API scopes only apply to the REST API. When Kiwi falls back to CLI mode (direct `openclaw` subprocess calls during WebSocket outage), exec approval is not available — that's an architectural boundary, not a bug. WebSocket mode is recommended for full security coverage.

## Web Audio Streaming

The dashboard includes a **Web Microphone** that lets you talk to Kiwi directly from the browser — no local microphone setup or pyaudio installation needed.

**How it works:**
- Browser captures audio via AudioWorklet (low-latency, runs off main thread)
- PCM Int16 audio is streamed to Kiwi over a WebSocket (`/api/audio`)
- Kiwi processes it through the same STT → wake word → LLM → TTS pipeline
- TTS responses are streamed back to the browser and played via AudioWorklet

Click the microphone button in the dashboard to connect. Volume bars show live audio level.

Configure in `config.yaml`:
```yaml
web_audio:
  enabled: true
  sample_rate: 16000
  max_clients: 3
```

## Home Assistant Integration

Bidirectional integration: control Kiwi from HA dashboard, and control your smart home by voice through Kiwi via the Conversation API.

Copy `custom_components/kiwi_voice/` to your HA `custom_components/` directory. Add the integration via the HA UI — enter host, port, and optionally an API token (if auth is enabled in `config.yaml`). The token can also be changed later in the integration options without re-pairing.

**Entities:** state sensor, language sensor, HA connection sensor, speakers count, uptime, listening switch, stop/reset/TTS buttons, TTS platform, voice control services. Entities are created based on token scopes — e.g. the stop button only appears if the token has `control` scope.

**Voice control:** Say *"Kiwi, turn on the lights"* — the command is routed to HA Conversation API and the response is spoken back. Configure in `config.yaml`:
```yaml
homeassistant:
  enabled: true
  url: "http://homeassistant.local:8123"
  token: ""  # Long-Lived Access Token
```

## License

[MIT](LICENSE) — do whatever you want with it.

---

<p align="center">
  Built with 🥝 and too much coffee
</p>
