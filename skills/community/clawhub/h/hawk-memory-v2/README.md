# 🦅 Context-Hawk

> **AI Context Memory Guardian** — Stop losing track, start remembering what matters.

*Give any AI agent a memory that actually works — across sessions, across topics, across time.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## What does it do?

Most AI agents suffer from **amnesia** — every new session starts from zero. Context-Hawk solves this with a production-grade memory management system that automatically captures what matters, lets noise fade away, and recalls the right memory at the right time.

**Without Context-Hawk:**
> "I already told you — I prefer concise replies!"
> (next session, the agent forgets again)

**With Context-Hawk:**
> (silently applies your communication preferences from session 1)
> ✅ Delivers concise, direct response every time

---

## ✨ 10 Core Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Task State Persistence** | `hawk resume` — persist task state, resume after restart |
| 2 | **4-Tier Memory** | Working → Short → Long → Archive with Weibull decay |
| 3 | **Structured JSON** | Importance scoring (0-10), category, tier, L0/L1/L2 layers |
| 4 | **AI Importance Scoring** | Auto-score memories, discard low-value content |
| 5 | **5 Injection Strategies** | A(high-imp) / B(task) / C(recent) / D(top5) / E(full) |
| 6 | **5 Compression Strategies** | summarize / extract / delete / promote / archive |
| 7 | **Self-Introspection** | Checks task clarity, missing info, loop detection |
| 8 | **LanceDB Vector Search** | Optional — hybrid vector + BM25 retrieval |
| 9 | **Pure-Memory Fallback** | Works without LanceDB, JSONL file persistence |
| 10 | **Auto-Dedup** | Merges duplicate memories automatically |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── Current session (recent 5-10 turns)       │
│       ↓ Weibull decay                                        │
│  Short-term      ←── 24h content, summarized                 │
│       ↓ access_count ≥ 10 + importance ≥ 0.7                │
│  Long-term       ←── Permanent knowledge, vector-indexed      │
│       ↓ >90 days or decay_score < 0.15                      │
│  Archive          ←── Historical, loaded on-demand              │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── Persistent across restarts (key!)     │
│  - Current task / next steps / progress / outputs           │
├──────────────────────────────────────────────────────────────┤
│  Injection Engine  ←── Strategy A/B/C/D/E decides recall     │
│  Self-Introspection ←── Every answer checks context         │
│  Auto-Trigger       ←── Every 10 rounds (configurable)       │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Task State Memory (Most Valuable Feature)

Even after restart, power failure, or session switch, Context-Hawk resumes exactly where it left off.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "Complete the API documentation",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["Review architecture template", "Report to user"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["Coverage must reach 98%", "APIs must be versioned"],
  "resumed_count": 3
}
```

```bash
hawk task "Complete the documentation"  # Create task
hawk task --step 1 done             # Mark step done
hawk resume                           # Resume after restart ← CORE!
```

---

## 🧠 Structured Memory

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Full original content",
  "summary": "One-line summary",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### Importance Scoring

| Score | Type | Action |
|-------|------|--------|
| 0.9-1.0 | Decisions/rules/errors | Permanent, slowest decay |
| 0.7-0.9 | Tasks/preferences/knowledge | Long-term memory |
| 0.4-0.7 | Dialog/discussion | Short-term, decay to archive |
| 0.0-0.4 | Chat/greetings | **Discard, never store** |

---

## 🎯 5 Context Injection Strategies

| Strategy | Trigger | Saves |
|----------|---------|-------|
| **A: High-Importance** | `importance ≥ 0.7` | 60-70% |
| **B: Task-Related** | scope match | 30-40% ← default |
| **C: Recent** | last 10 turns | 50% |
| **D: Top5 Recall** | `access_count` top 5 | 70% |
| **E: Full** | no filter | 100% |

---

## 🗜️ 5 Compression Strategies

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 4-Level Alert System

| Level | Threshold | Action |
|-------|-----------|--------|
| ✅ Normal | < 60% | Silent |
| 🟡 Watch | 60-79% | Suggest compression |
| 🔴 Critical | 80-94% | Pause auto-write, force suggestion |
| 🚨 Danger | ≥ 95% | Block writes, must compress |

---

## 🚀 Quick Start

```bash
# Install LanceDB plugin (recommended)
openclaw plugins install memory-lancedb-pro@beta

# Activate skill
openclaw skills install ./context-hawk.skill

# Initialize
hawk init

# Core commands
hawk task "My task"    # Create task
hawk resume             # Resume last task ← MOST IMPORTANT
hawk status            # View context usage
hawk compress          # Compress memory
hawk strategy B        # Switch to task-related mode
hawk introspect         # Self-introspection report
```

---

## Auto-Trigger: Every N Rounds

Every **10 rounds** (default, configurable), Context-Hawk automatically:

1. Checks context water level
2. Evaluates memory importance
3. Reports status to user
4. Suggests compression if needed

```bash
# Config (in memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # check every N rounds
  "keep_recent": 5,                 # preserve last N turns
  "auto_compress_threshold": 70      # compress when > 70%
}
```

---

## File Structure

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI tool
└── references/
    ├── memory-system.md           # 4-tier architecture
    ├── structured-memory.md      # Memory format & importance
    ├── task-state.md           # Task state persistence
    ├── injection-strategies.md  # 5 injection strategies
    ├── compression-strategies.md # 5 compression strategies
    ├── alerting.md             # Alert system
    ├── self-introspection.md   # Self-introspection
    ├── lancedb-integration.md  # LanceDB integration
    └── cli.md                  # CLI reference
```

---

## 🔌 Tech Specs

- **Persistence**: JSONL local files, no database required
- **Vector Search**: LanceDB (optional), auto-fallback to files
- **Cross-Agent**: Universal, no business logic, works with any AI agent
- **Zero-Config**: Works out-of-the-box with smart defaults
- **Extensible**: Custom injection strategies, compression policies, scoring rules

---



## 🦅 Context-Hawk — Pure Python Memory Package

> **纯 Python 记忆包，零外部依赖，零 API Key，直接 import 就能用**

context-hawk 是一个独立的 Python 包，提供：
- 四层记忆衰减（MemoryManager）
- 向量语义检索（VectorRetriever）
- Markdown 文件导入（MarkdownImporter）
- 上下文压缩（ContextCompressor）
- 记忆提取（Extractor — 支持零 API 关键词模式）
- 自我反思（SelfImproving）
- 系统巡检（Governance）

**不需要 OpenClaw，不需要 API Key**，可嵌入任何 Python 项目。

```bash
pip install lancedb
python3.12 -c "from hawk.memory import MemoryManager; print('OK')"
```

详细文档见 [SKILL.md](SKILL.md)
