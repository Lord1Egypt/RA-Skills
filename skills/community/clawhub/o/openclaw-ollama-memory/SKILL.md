---
name: openclaw-ollama-memory
description: "Set up local semantic memory search in OpenClaw using Ollama + nomic-embed-text. Free, private, offline-capable. Replaces cloud embedding APIs (OpenAI, Gemini) with a locally-running model. Trigger phrases: ollama memory, local embeddings, private memory search, offline memory, free embeddings, nomic-embed-text."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["ollama","curl"]},"os":["linux","darwin","win32"]}}
---

# OpenClaw Ollama Memory

Local semantic memory search for OpenClaw using Ollama — free, private, no API key required.

## Quick Start

### 1. Install & Run Ollama

Download from https://ollama.ai, then pull the embedding model:

```bash
ollama pull nomic-embed-text
```

Verify Ollama is running:

```bash
curl http://127.0.0.1:11434/api/tags
```

### 2. Configure OpenClaw

Edit `~/.openclaw/openclaw.json` and add under `agents.defaults.memorySearch`:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama",
        "model": "nomic-embed-text:latest",
        "remote": {
          "baseUrl": "http://127.0.0.1:11434"
        }
      }
    }
  }
}
```

### 3. Restart OpenClaw

```bash
openclaw gateway restart
```

## Key Points

- **Ollama must be explicit** — use `provider: "ollama"`, not `"openai"`. OpenClaw doesn't auto-detect Ollama.
- **No API key needed** — runs locally, fully offline.
- **nomic-embed-text** — 274MB model, fast, accurate, free.
- **baseUrl format** — `http://127.0.0.1:11434` (no `/v1` suffix, no trailing slash).

## Next Steps

- See `references/config-reference.md` for advanced tuning (hybrid search, MMR, temporal decay, extra paths).
- See `references/troubleshooting.md` for common errors and fixes.
