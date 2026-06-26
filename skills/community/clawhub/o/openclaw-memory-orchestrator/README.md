# OpenClaw Memory Orchestrator Lite

Still dealing with broken conversation continuity, missing historical context, or long chats that burn through huge amounts of tokens?
OpenClaw Memory Orchestrator uses memory deduplication, compression, layered indexing, and adaptive retrieval routing to keep long-term memory cleaner, retrieval more stable, and token costs under control.

## Install

### Linux
```bash
bash install.sh
```

> For the full feature set, install the full package from GitHub:
> https://github.com/che52078/openclaw-memory-orchestrator

## Modes
- minimal-local
- local-ollama
- hybrid-remote

## Notes
- Ollama is optional
- Remote vector database is optional
- Local-only mode is supported

## ClawHub Safe Mode
- No automatic pip install
- No automatic runtime execution during install
- Remote vector DB is disabled by default unless explicitly configured
