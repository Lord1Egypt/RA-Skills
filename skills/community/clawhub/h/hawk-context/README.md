# 🦅 Context Compressor

> **Pure Context Compression Engine** — not a memory manager, a lifesaver.

When your AI conversation context is about to explode, Context Compressor compresses it instantly. 180k → 35k. Continue chatting like nothing happened.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)

---

## What is this vs. context-hawk?

| Tool | What it does | When to use |
|------|--------------|-------------|
| **Context Compressor** | Compresses **current** conversation | Right now, when context is full |
| **context-hawk** | Manages **persistent** memory across sessions | Daily, between conversations |

**Context Compressor = Emergency rescue. context-hawk = Daily maintenance.**

---

## How it works

### Before compression (180k tokens — exploding)

```
[Full conversation history — 180k tokens — at 88%]
System: You are a helpful assistant...
User: First question...
Assistant: First answer...
User: Second question...
... (越来越长，越来越贵，越来越慢)
```

### After compression (35k tokens — clean)

```json
{
  "compressed_prompt": [
    {"role": "system", "content": "[永久保留的系统提示]", "status": "preserved"},
    {"role": "user", "content": "[最新问题完整原文]", "status": "preserved"},
    {"role": "assistant", "content": "[最新回答完整原文]", "status": "preserved"},
    {"role": "summary", "content": "[早期45条消息摘要]", "status": "summarized"}
  ],
  "stats": {
    "original_tokens": 180000,
    "compressed_tokens": 35000,
    "ratio": "5.1x",
    "kept_messages": 5,
    "summarized_count": 87,
    "level": "normal"
  }
}
```

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| **Auto-trigger** | Compresses automatically at 70% context threshold |
| **4 compression levels** | light / normal / heavy / emergency |
| **Structured JSON output** | Full stats: tokens, ratio, counts |
| **System prompt preserved** | Role definitions never compressed |
| **Importance filtering** | Discards noise, keeps decisions/rules/code |
| **Message deduplication** | Merges repeated confirmations |
| **Code collapsing** | Long code blocks folded to meta |
| **Pure Python** | No database, no dependencies |
| **Writes to memory** | Compression history saved to `memory/today.md` |

---

## 🚀 Quick Start

```bash
# Install skill
openclaw skills install ./context-compressor.skill

# Auto-link hawk-compress command to ~/bin (one-time)
bash ~/.openclaw/workspace/skills/context-compressor/scripts/install.sh
source ~/.bashrc

# Compress current conversation (auto-detect level)
hawk-compress

# Compress with specific level
hawk-compress --level heavy

# Preview without writing
hawk-compress --dry-run
```

---

## Compression Levels

| Level | When | Effect |
|--------|-------|--------|
| `light` | 60-70% | Summarize messages > 30 days old |
| `normal` | 70-85% | Summarize + keep recent 10 ← **default** |
| `heavy` | 85-95% | Keep recent 5 only |
| `emergency` | > 95% | Keep recent 3 only |

---

## Auto-Trigger

When context reaches 70%, every answer includes:

```
[🦅 Context: 72%] Compress recommended: /hawk-compress
  148k → ~35k | Save 113k tokens
```

At 85%+, forces confirmation before continuing.

---

## File Structure

```
context-compressor/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk-compress       # Python CLI tool
└── references/
    ├── compression-logic.md    # Compression algorithm
    ├── auto-trigger.md        # Auto-trigger system
    ├── structured-output.md    # JSON output format
    └── cli.md                # CLI reference
```

---

## Requirements

- Python 3.8+
- No external dependencies
- No database required

---

## License

MIT — free to use, modify, and distribute.
