# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kiwi Voice is a multi-language real-time voice assistant integrated with the OpenClaw AI backend. It captures microphone audio, transcribes speech via configurable STT engines (Faster Whisper, ElevenLabs cloud, or MLX Whisper), detects the wake word "kiwi", identifies speakers via pyannote embeddings, communicates with OpenClaw over WebSocket, and speaks responses through configurable TTS providers.

All code comments and docstrings are in English. User-facing strings are externalized into YAML locale files (`kiwi/locales/*.yaml`) supporting 15 languages.

## Running the Service

```bash
# Activate the virtual environment
source venv/Scripts/activate   # Windows/MSYS2
source venv/bin/activate       # Linux

# Install dependencies
pip install -r requirements.txt

# Run the main service
python -m kiwi
```

Smoke tests: `pytest tests/test_smoke.py`

## Configuration

**Precedence:** `config.yaml` → environment variables (`.env`) → hardcoded defaults

- `config.yaml` — primary config (language, WebSocket, STT, TTS, wake word, VAD, speaker priority, security)
- `.env` — secrets and provider overrides (see `.env.example` for available vars)
- Key env vars: `KIWI_LANGUAGE` (ru | en | es | de | fr | ...), `KIWI_TTS_PROVIDER` (qwen3 | piper | elevenlabs), `KIWI_QWEN_BACKEND` (runpod | local), `KIWI_STT_ENGINE` (faster-whisper | mlx-whisper | elevenlabs)

## Architecture

### Audio Pipeline

```
Microphone (24kHz) → Audio Callback (energy + Silero VAD) → Audio Queue
  → KiwiListener._record_loop() → STT (Faster Whisper | ElevenLabs | MLX Whisper) → Wake Word Detection ("kiwi")
  → Speaker ID (pyannote embedding) → Priority Check (OWNER > FRIEND > GUEST > BLOCKED)
  → Voice Security (Telegram approval for dangerous commands from non-OWNER)
  → OpenClaw WebSocket (ws://127.0.0.1:18789, Protocol v3: chat.send → delta/final events)
  → TTS Provider → Speaker Output (with barge-in detection)
  → Loop back to listening
```

### Speaker Priority System

```python
class VoicePriority(IntEnum):
    SELF = -1      # TTS echo filtering
    OWNER = 0      # Full access, cannot be blocked
    FRIEND = 1     # Dangerous commands need Telegram approval
    GUEST = 2      # All potentially dangerous commands need approval
    BLOCKED = 99   # Blacklisted
```

## Internationalization (i18n)

All user-facing strings are externalized into YAML locale files in `kiwi/locales/`. The system is managed by `kiwi/i18n.py`.

### How it works

```python
from kiwi.i18n import setup, t

setup("en", fallback="ru")       # Initialize with locale
t("responses.greeting")           # → "Hello! I'm Kiwi..."
t("responses.heard", command=cmd) # → "Heard: {command}" with placeholder
t("hallucinations.phrases")       # → returns a list
t("wake_word.typos")              # → returns a dict
```

- `setup(locale, fallback)` is called in `service.py` at startup
- `t(key)` resolves dot-notation keys, falls back to fallback locale, then returns the raw key
- Supports `{placeholder}` formatting via kwargs for string values
- Returns lists/dicts as-is for non-string values

### Language switching

```yaml
# config.yaml
language: "en"    # or: ru, es, pt, fr, it, de, tr, pl, zh, ja, ko, hi, ar, id
```

Or via env var: `KIWI_LANGUAGE=en`

### Locale file structure

Each locale YAML has 19 sections:
- `system` — voice system prompt for the LLM
- `responses` — spoken user-facing strings (~37 keys)
- `status` — long-task status announcements
- `security` — warning messages, Telegram buttons
- `speakers` — speaker identification responses
- `speaker_access` — access control messages
- `wake_word` — keyword, typos, fuzzy blacklist (per-language)
- `hallucinations` — Whisper hallucination phrases/patterns (per-language)
- `text_processing` — abbreviations, incomplete/complete patterns, emotion keywords (per-language)
- `security_patterns` — dangerous command regexes (per-language + universal)
- `dangerous_commands` — example dangerous commands
- `owner_commands` — voice control command phrases
- `owner_control_patterns` — owner command regexes
- `name_patterns` — name extraction regexes and filter words
- `commands` — command keywords (stop, calibrate, approval, etc.)
- `cli_errors`, `ws_errors` — error messages
- `tool_activity`, `tool_errors` — tool status descriptions

### Adding a new language

1. Copy `kiwi/locales/en.yaml` → `kiwi/locales/{code}.yaml`
2. Translate all values (preserve keys and `{placeholders}`)
3. Adapt language-specific sections: `wake_word.typos`, `hallucinations`, `text_processing`, `security_patterns`, `commands`
4. Set `language: "{code}"` in `config.yaml`

### Code pattern for i18n strings

```python
from kiwi.i18n import t

# User-facing strings — always use t()
self._speak(t("responses.greeting"))
self._speak(t("responses.heard", command=cmd))

# Developer-facing log messages — do NOT use t()
kiwi_log("TAG", "Internal log message", level="INFO")
```

Module-level constants (e.g. `WAKE_WORD`, `HALLUCINATION_PHRASES`) are kept as fallback defaults. Instance attributes override them from i18n at init time:
```python
self.wake_word = t("wake_word.keyword") or WAKE_WORD
self.hallucination_phrases = set(t("hallucinations.phrases") or HALLUCINATION_PHRASES)
```

## Code Patterns

### Logging

Use `kiwi_log()` from `kiwi.utils` — never bare `print()`:
```python
from kiwi.utils import kiwi_log
kiwi_log("TAG", "message", level="INFO")  # → [14:08:25.342] [INFO] [TAG] message
```

### Project Root Paths

Use `PROJECT_ROOT` for paths to project-level assets:
```python
from kiwi import PROJECT_ROOT
path = os.path.join(PROJECT_ROOT, 'sounds', 'startup.mp3')
```

### Optional Module Loading

Modules are imported with try/except and availability flags:
```python
try:
    from kiwi.speaker_manager import SpeakerManager
    SPEAKER_MANAGER_AVAILABLE = True
except ImportError:
    SPEAKER_MANAGER_AVAILABLE = False
```

### Threading

All background work uses daemon threads with crash protection (try/except + sleep + continue in loops). Shared resources (cache, stdout, WebSocket) are guarded by `threading.Lock`.

### GPU Auto-Detection

CUDA is used when available, with automatic CPU fallback:
```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

### Windows UTF-8

Console codepage is set for Unicode output via `ctypes.windll.kernel32.SetConsoleCP(65001)`.

## Soul System (Personalities)

Dynamic personality switching via markdown files in `kiwi/souls/`. Managed by `kiwi/soul_manager.py`.

- **SoulManager** loads `.md` files, composes system prompt = base Kiwi context + soul personality
- **SoulConfig** dataclass: `id`, `name`, `description`, `prompt`, `model` (informational), `session` (OpenClaw session override), `nsfw`
- NSFW soul routes to a separate OpenClaw agent via session switching (`openclaw_ws.switch_session()`)
- Config: `souls.default`, `souls.nsfw.model`, `souls.nsfw.session` in config.yaml
- Voice commands for switching defined in locale files: `soul_switch_patterns`, `nsfw_enable_patterns`, `default_mode_patterns`
- API: `GET /api/souls`, `GET /api/soul/current`, `POST /api/soul`

## Key Documentation

- `SKILL.md` — voice commands, security hierarchy, and deployment info (in Russian)

## Roadmap

All planned phases are complete:

- Phase 1: Stability & Observability — **done**
- Phase 2: State machine — **done**
- Phase 3: Streaming TTS — **done**
- Phase 4: WebSocket OpenClaw integration — **done**
- Phase 5: Package structure reorganization — **done**
- Phase 6: i18n / multi-language support (15 languages) — **done**
- Phase 7: UnifiedVAD + HardwareAEC + EventBus integration — **done**
- Phase 8: REST API (`kiwi/api/`, aiohttp on port 7789) — **done**
- Phase 9: Web UI dashboard (`kiwi/web/`, dark theme SPA) — **done**
- Phase 10: Home Assistant integration (`custom_components/kiwi_voice/`) — **done**

### REST API

- Server: `kiwi/api/server.py`, runs in background thread on port 7789
- Endpoints: `/api/status`, `/api/config`, `/api/speakers`, `/api/languages`, `/api/souls`, `/api/soul`, `/api/tts/test`, `/api/stop`, `/api/reset-context`, `/api/restart`, `/api/shutdown`
- WebSocket: `/api/events` for real-time EventBus streaming
- Config: `api.enabled`, `api.host`, `api.port` in config.yaml

### Web UI

- Files: `kiwi/web/index.html`, `kiwi/web/static/style.css`, `kiwi/web/static/app.js`
- Served at `http://localhost:7789/`
- Dark theme SPA with live status, language switcher, speaker management, TTS test, event log

### Home Assistant

- Custom component: `custom_components/kiwi_voice/`
- Config flow with connection testing
- Entities: state sensor, language sensor, speakers sensor, uptime sensor, listening switch, stop/reset/TTS buttons, TTS platform
