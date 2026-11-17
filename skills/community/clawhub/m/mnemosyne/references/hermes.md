# Hermes Adapter

Cross-platform edition for Hermes agent + Windows (MSYS/MinGW) + macOS.

```bash
cd elite && bash install-elite.sh --hermes --skill-dir /path/to/hermes/skills
```

Adds: MNEMOSYNE_ROOT / HERMES_WORKSPACE env vars, MSYS path mapping, WSL detection, Hermes skill auto-install with absolute path replacement, `pre-reply` / `post-reply` / `quick-check` bridge.
