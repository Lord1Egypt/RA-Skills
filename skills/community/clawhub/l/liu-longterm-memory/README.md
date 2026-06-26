# Liu Longterm Memory 🧠

**The ultimate memory system for AI agents.** Never lose context again.

[![npm version](https://img.shields.io/npm/v/liu-longterm-memory.svg?style=flat-square)](https://www.npmjs.com/package/liu-longterm-memory)
[![npm downloads](https://img.shields.io/npm/dm/liu-longterm-memory.svg?style=flat-square)](https://www.npmjs.com/package/liu-longterm-memory)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

## Works With

<p align="center">
  <img src="https://img.shields.io/badge/Claude-AI-orange?style=for-the-badge&logo=anthropic" alt="Claude AI" />
  <img src="https://img.shields.io/badge/GPT-OpenAI-412991?style=for-the-badge&logo=openai" alt="GPT" />
  <img src="https://img.shields.io/badge/ZhipuAI-智谱-blue?style=for-the-badge" alt="ZhipuAI" />
  <img src="https://img.shields.io/badge/Cursor-IDE-000000?style=for-the-badge" alt="Cursor" />
  <img src="https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge" alt="LangChain" />
</p>

<p align="center">
  <strong>Built for:</strong> Clawdbot • Moltbot • Claude Code • Any AI Agent
</p>

---

Combines 6 memory layers into one bulletproof architecture:

- ✅ **Bulletproof WAL Protocol** — Write-ahead logging survives compaction
- ✅ **LanceDB Vector Search** — Semantic recall of relevant memories
- ✅ **Git-Notes Knowledge Graph** — Structured decisions, branch-aware
- ✅ **File-Based Archives** — Human-readable MEMORY.md + daily logs
- ✅ **Backup** — zip or Git remote (GitHub/Gitee) sync
- ✅ **Memory Hygiene** — Keep vectors lean, prevent token waste
- ✅ **Auto-Extraction** — LLM-powered fact extraction (ZhipuAI free model or zero dependencies)

## Quick Start

```bash
# Initialize in your workspace
npx liu-longterm-memory init

# Check status
npx liu-longterm-memory status

# Create today's log
npx liu-longterm-memory today

# Backup memory (zip)
npx liu-longterm-memory backup

# Backup memory (Git commit + push)
npx liu-longterm-memory backup --git

# Restore from backup
npx liu-longterm-memory restore memory-backup-20260404.zip
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              ELITE LONGTERM MEMORY                  │
├─────────────────────────────────────────────────────┤
│  HOT RAM          WARM STORE        COLD STORE     │
│  SESSION-STATE.md → LanceDB      → Git-Notes       │
│  (survives         (semantic       (permanent      │
│   compaction)       search)         decisions)     │
│         │              │                │          │
│         └──────────────┼────────────────┘          │
│                        ▼                           │
│                   MEMORY.md                        │
│               (curated archive)                    │
└─────────────────────────────────────────────────────┘
```

## The 6 Memory Layers

| Layer | File/System | Purpose | Persistence |
|-------|-------------|---------|-------------|
| 1. Hot RAM | SESSION-STATE.md | Active task context | Survives compaction |
| 2. Warm Store | LanceDB | Semantic search | Auto-recall |
| 3. Cold Store | Git-Notes | Structured decisions | Permanent |
| 4. Archive | MEMORY.md + daily/ | Human-readable | Curated |
| 5. Backup | zip / Git remote | Cross-device sync | Optional |
| 6. Auto-Extract | Agent rules / GLM-4-Flash | Fact extraction | Built-in |

## The WAL Protocol

**Critical insight:** Write state BEFORE responding, not after.

```
User: "Let's use Tailwind for this project"

Agent (internal):
1. Write to SESSION-STATE.md → "Decision: Use Tailwind"
2. THEN respond → "Got it — Tailwind it is..."
```

If you respond first and crash before saving, context is lost. WAL ensures durability.

## Why Memory Fails (And How to Fix It)

| Problem | Cause | Fix |
|---------|-------|-----|
| Forgets everything | memory_search disabled | Enable memorySearch + configure embedding provider |
| Repeats mistakes | Lessons not logged | Write to memory/lessons.md |
| Sub-agents isolated | No context inheritance | Pass context in task prompt |
| Facts not captured | No auto-extraction | Agent auto-extracts by default; or use LLM batch extraction |

## Auto-Extraction (LLM-Powered)

The agent auto-extracts preferences, decisions, deadlines, and corrections from every conversation. Two modes:

1. **Agent-Driven** (零依赖) — agent follows extraction rules, no API needed
2. **LLM Batch** (推荐) — uses ZhipuAI's free GLM-4-Flash model for structured extraction

See [SKILL.md](./SKILL.md) Layer 6 for details and setup.

## For Clawdbot/Moltbot Users

Add to `~/.clawdbot/clawdbot.json`. Supports any OpenAI-compatible embedding provider:

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai-compatible",
    "baseURL": "https://open.bigmodel.cn/api/paas/v4",
    "model": "embedding-3",
    "apiKeyEnv": "ZHIPUAI_API_KEY",
    "sources": ["memory"]
  }
}
```

> **No API key required for core memory.** Vector search is optional — see [SKILL.md](./SKILL.md) for all provider options (ZhipuAI, Ollama, OpenAI, DeepSeek, etc.).

## Files Created

```
workspace/
├── SESSION-STATE.md    # Hot RAM (active context)
├── MEMORY.md           # Curated long-term memory
└── memory/
    ├── 2026-01-30.md   # Daily logs
    └── ...
```

## Commands

```bash
elite-memory init      # Initialize memory system
elite-memory status    # Check health
elite-memory today     # Create today's log
elite-memory help      # Show help
```

## Links

- [Full Documentation (SKILL.md)](./SKILL.md)
- [ClawdHub](https://clawdhub.com/skills/liu-longterm-memory)
- [GitHub](https://github.com/louiseliu/liu-longterm-memory)

---

> **Fork Notice:** This project is based on [elite-longterm-memory](https://github.com/NextFrontierBuilds/elite-longterm-memory) by [@NextXFrontier](https://x.com/NextXFrontier). Modified for Chinese users with ZhipuAI integration, multi-provider support, and localized documentation.
