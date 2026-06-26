---
name: ondeckllm
description: >
  Localhost dashboard for managing LLM providers, model routing, and batting-order
  fallback chains. Auto-discovers providers from OpenClaw config or works standalone.
  Use when: (1) user wants to manage or view their LLM providers, (2) user wants to
  change model priority/batting order, (3) user wants to check provider health or
  latency, (4) user wants to add/remove/configure LLM providers, (5) user mentions
  OnDeckLLM or model lineup. Requires: Node.js 22+, OnDeckLLM installed
  (`npm install -g ondeckllm`).
install: npm install -g ondeckllm
---

# OnDeckLLM — AI Model Lineup Manager

## Prerequisites

```bash
npm install -g ondeckllm
```

Verify: `ondeckllm --help` or check install with `npm list -g ondeckllm`.

## What It Does

OnDeckLLM is a localhost web dashboard that:

- **Auto-discovers** LLM providers from OpenClaw config (`~/.openclaw/openclaw.json`)
- **Manages** a batting-order priority list for model routing (primary + fallbacks)
- **Tests** provider health and latency
- **Syncs** model lineup back to OpenClaw config with one click
- **Tracks** session costs (JSONL usage log + Chart.js)
- **Supports** Anthropic, OpenAI, Google AI, Groq, xAI/Grok, Ollama (local + remote), Mistral, DeepSeek, Together, OpenRouter

## Starting the Dashboard

```bash
# Default port 3900
ondeckllm

# Custom port
PORT=3901 ondeckllm
```

The dashboard runs at `http://localhost:3900` (or custom port).

### As a Background Service

Use the helper script to check status or start OnDeckLLM:

```bash
node scripts/status.js
```

Output: JSON with `running` (bool), `port`, `url`, and `pid` if active.

## Agent Workflow

### Check if OnDeckLLM is running

```bash
node scripts/status.js
```

### Open the dashboard for the user

Direct them to `http://localhost:3900` (or the configured port/URL).

### Provider management

OnDeckLLM reads provider config from `~/.openclaw/openclaw.json` automatically.
Changes made in the dashboard sync back to OpenClaw config.
No separate API or CLI commands needed — it's a web UI tool.

## Configuration

OnDeckLLM stores its data in `~/.ondeckllm/`:

- `config.json` — provider settings, port, Ollama URL
- `usage.jsonl` — cost tracking log
- `profiles/` — saved batting-order profiles

### Remote Ollama

To connect to a remote Ollama instance, configure in the dashboard UI:
Settings → Ollama → Remote URL (e.g., `http://192.168.55.80:11434`)

## Links

- 🌐 [ondeckllm.com](https://ondeckllm.com)
- 📦 [npm](https://www.npmjs.com/package/ondeckllm)
- 🐛 [GitHub Issues](https://github.com/canonflip/ondeckllm/issues)
