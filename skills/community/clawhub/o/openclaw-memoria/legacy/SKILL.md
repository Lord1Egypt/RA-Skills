---
name: Memoria for OpenClaw
version: 3.34.0
description: "The most advanced memory system for AI agents. 24 cognitive layers, knowledge graph, procedural learning, dialectic queries, AI self-observation, auto skill creation, crash-safe WAL, async prefetch. Works with Claude, Cursor, Copilot, ChatGPT & any OpenClaw agent. 100% local-first (SQLite + Ollama), zero cloud cost, zero API keys required."
author: Primo Studio (@Nieto42)
license: Apache-2.0
homepage: https://github.com/Primo-Studio/openclaw-memoria
repository: https://github.com/Primo-Studio/openclaw-memoria
feedback: https://x.com/Nitix_
keywords:
  - memory
  - ai-agent
  - persistent-memory
  - long-term-memory
  - knowledge-graph
  - procedural-learning
  - vector-search
  - sqlite
  - ollama
  - lm-studio
  - local-first
  - cognitive
  - context
  - claude
  - cursor
  - copilot
  - chatgpt
  - openclaw
  - wal
  - vibe-coding
  - developer-tools
  - devtools
  - typescript
  - llm
  - automation
  - brain-inspired
  - multi-layer
  - fact-extraction
  - self-improving
tags:
  - memory
  - ai-agent
  - persistent-memory
  - long-term-memory
  - knowledge-graph
  - procedural-learning
  - vector-search
  - sqlite
  - ollama
  - lm-studio
  - local-first
  - cognitive
  - context
  - claude
  - cursor
  - copilot
  - chatgpt
  - openclaw
  - wal
  - vibe-coding
  - developer-tools
  - devtools
  - typescript
  - llm
  - automation
  - brain-inspired
  - multi-layer
  - fact-extraction
  - self-improving
  - self-observation
  - dialectic
  - auto-skill
  - prefetch
  - crash-recovery
  - async
env:
  - name: OPENAI_API_KEY
    required: false
    description: Optional — used as fallback for LLM extraction and embeddings when local models are unavailable. Never required for default operation.
  - name: OPENROUTER_API_KEY
    required: false
    description: Optional — used as fallback for remote LLM provider. Never required for default operation.
  - name: OPENCLAW_WORKSPACE
    required: false
    description: Auto-set by OpenClaw runtime — workspace path for memory files. Do not set manually.
security: |
  ## Data & Privacy
  - Memoria runs 100% locally by default. No data leaves your machine unless you explicitly configure a remote LLM.
  - All memory is stored in a local SQLite database in your OpenClaw workspace.
  - API keys (OPENAI_API_KEY, OPENROUTER_API_KEY) are optional fallbacks — never required.

  ## What Memoria reads
  - Workspace files: USER.md, COMPANY.md, projects/* — used for identity-aware relevance scoring.
    These files may contain personal or business information. Review them before enabling Memoria.
  - Conversation content: assistant messages and tool call results, to extract durable facts.
  - No files outside the OpenClaw workspace are read.

  ## What Memoria writes
  - A single SQLite database (memoria.db) in your workspace/memory/ folder.
  - Optional markdown summaries in workspace/memory/ folder.
  - No network requests unless a remote LLM fallback is configured.

  ## Hooks used
  - before_prompt_build: injects recalled facts into context
  - after_tool_call: captures procedural knowledge (how-to steps)
  - agent_end: extracts facts from completed conversations
  - after_compaction: extracts facts from compacted summaries
  These are standard OpenClaw plugin hooks. They run locally within the plugin process.
entrypoint: index.ts
---

# 🧠 Memoria — Multi-Layer Persistent Memory for OpenClaw

**The most complete memory system for OpenClaw.** 20 layers of memory that work together, powered by YOUR choice of LLM.

## Why Memoria?

### 🏗️ 20 Memory Layers (not just a fact store)
1. **Facts** — Durable knowledge extracted from every conversation
2. **Procedures** — HOW to do things, improves with repetition, learns from failures
3. **Knowledge Graph** — Entities + relations connecting your facts
4. **Topics & Expertise** — Tracks what you talk about most, specializes over time
5. **Observations** — Short-term working memory for active context
6. **Error Detection** 🔥 — Touch fire once, remember forever. Dangers captured on first occurrence
7. **Lifecycle** — Fresh → Settled → Dormant. Nothing deleted, priority shifts naturally

### 🔌 Bring Your Own LLM
Configure each layer independently. Mix and match:
- **Ollama** — Run gemma3, qwen3.5, llama, or any model locally (recommended)
- **LM Studio** — Use any GGUF model from your local server
- **Remote APIs** — OpenAI, Anthropic, OpenRouter as primary or fallback
- **Fallback chains** — Ollama → LM Studio → API. If one fails, the next takes over automatically

### 🏠 100% Local-First
- **SQLite + FTS5** — No external database needed
- **Local embeddings** — nomic-embed-text via Ollama (zero API cost)
- **Zero cloud dependency** — Works offline, your data stays on your machine
- **Fallback chain** — Degrades gracefully if a provider goes down

### 🧬 What Makes Memoria Different
| Feature | Memoria | Basic memory plugins |
|---------|---------|---------------------|
| Memory layers | 20 specialized layers | Single fact store |
| LLM choice | Any local or remote model | Usually hardcoded |
| Per-layer LLM config | ✅ Different model per layer | ❌ |
| Procedural learning | ✅ Learns HOW, not just WHAT | ❌ |
| Error detection | ✅ Auto-captures dangers | ❌ |
| Knowledge graph | ✅ Entities + relations | ❌ |
| Lifecycle management | ✅ Smart aging, never forgets | ❌ or simple TTL |
| Cost | $0 with local models | Varies |

## Installation

### As Plugin (recommended — one command)
```bash
openclaw plugins install clawhub:memoria-plugin
```
This installs Memoria from the ClawHub registry. No manual steps needed.

### From source (for contributors / advanced users)
If you prefer to inspect the code first:
1. Browse the repository: [github.com/Primo-Studio/openclaw-memoria](https://github.com/Primo-Studio/openclaw-memoria)
2. Review the source code, especially `index.ts` (main entrypoint) and `openclaw.plugin.json` (config schema)
3. Clone and install:
```bash
cd ~/.openclaw/extensions
git clone https://github.com/Primo-Studio/openclaw-memoria.git memoria
cd memoria && npm install
```

Then add to your `openclaw.json` under `plugins.entries`:
```json
{
  "memoria": { "enabled": true },
  "memory-convex": { "enabled": false }
}
```

## Configuration

### Minimal (works out of the box with Ollama)
Just install and restart. Defaults: Ollama + gemma3:4b for extraction, nomic for embeddings.

### Custom LLM per layer
```json
"memoria": {
  "enabled": true,
  "config": {
    "llm": {
      "default": { "provider": "ollama", "model": "qwen3.5:4b" },
      "procedural": { "provider": "lmstudio", "model": "your-model" },
      "graph": { "provider": "openai", "model": "gpt-4o-mini" }
    }
  }
}
```

## Source Code

The full source is available on GitHub: [Primo-Studio/openclaw-memoria](https://github.com/Primo-Studio/openclaw-memoria)

Key files:
- `index.ts` — Main plugin entrypoint (hooks, extraction, recall pipeline)
- `procedural.ts` — Procedural memory (how-to learning)
- `lifecycle.ts` — Lifecycle management (fresh/settled/dormant)
- `scoring.ts` — Temporal scoring and relevance ranking
- `selective.ts` — Dedup, contradiction detection, fact quality
- `openclaw.plugin.json` — Configuration schema

## Feedback & Community

**We'd love your feedback!** Tell us how Memoria works for you:
- 🐦 **Tweet us** [@Nitix_](https://x.com/Nitix_) — share your setup, results, or ideas
- ⭐ **Star the repo**: [github.com/Primo-Studio/openclaw-memoria](https://github.com/Primo-Studio/openclaw-memoria)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Primo-Studio/openclaw-memoria/issues)

Built with ❤️ by [Primo Studio](https://primo-studio.fr) 🇬🇫 — AI tooling from French Guiana.
