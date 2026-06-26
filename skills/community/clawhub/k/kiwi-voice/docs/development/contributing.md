# Contributing

## Setup

```bash
git clone https://github.com/ekleziast/kiwi-voice.git
cd kiwi-voice
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Code Style

- **Linter:** [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- **Type checking:** mypy (with `--ignore-missing-imports`)
- **Logging:** Always `kiwi_log("TAG", "message")` — never `print()`
- **Paths:** Use `PROJECT_ROOT` from `kiwi` package
- **Imports:** Optional modules with try/except + `*_AVAILABLE` flags
- **Threads:** Daemon threads with crash protection
- **Comments and docstrings:** English
- **User-facing strings:** Externalized via `t()` into locale YAML files

## Running Checks

```bash
# Lint
ruff check kiwi/ tests/

# Format check
ruff format --check kiwi/ tests/

# Type check
mypy kiwi/ --ignore-missing-imports --no-strict-optional

# Tests
pytest tests/ -v --tb=short
```

CI runs these checks on every push and PR via GitHub Actions.

## Project Structure

```
kiwi-voice/
├── kiwi/                    # Main package
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── service.py           # Main service orchestrator
│   ├── listener.py          # Audio capture, STT, wake word
│   ├── openclaw_ws.py       # WebSocket client
│   ├── speaker_manager.py   # Speaker identification
│   ├── voice_security.py    # Dangerous command detection
│   ├── soul_manager.py      # Personality system
│   ├── i18n.py              # Internationalization
│   ├── event_bus.py         # Internal event system
│   ├── utils.py             # Logging, helpers
│   ├── tts/                 # TTS providers
│   ├── mixins/              # Service mixins
│   ├── api/                 # REST API server
│   ├── web/                 # Dashboard (HTML/CSS/JS)
│   ├── locales/             # Language YAML files
│   └── souls/               # Personality markdown files
├── custom_components/       # Home Assistant integration
├── tests/                   # Test suite
├── docs/                    # Documentation (MkDocs)
├── config.yaml              # Configuration
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── mkdocs.yml               # Docs config
```

## Adding a Language

See [Multi-Language Support](../features/multilanguage.md#adding-a-new-language).

## Adding a TTS Provider

1. Create a new file in `kiwi/tts/` implementing the provider interface
2. Register it in the TTS factory
3. Add config section in `config.yaml`
4. Document in `docs/features/tts-providers.md`

## Adding a Soul

Create a markdown file in `kiwi/souls/` — see [Personalities](../features/souls.md#creating-custom-souls).
