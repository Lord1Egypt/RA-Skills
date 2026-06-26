---
version: 1.1.0
name: moore-pyramid-memory-system
description: "Moore 金字塔记忆系统 — 5层记忆架构，确保跨 session 连续性。每次启动时自动加载，新 session 开始时必须执行此 skill。"
---

# Moore 金字塔记忆系统

Moore's self-developed memory system ensures continuity across sessions. Never forget a cross-session task again.

## The Problem It Solves

**Before:** Cross-session tasks were forgotten because there was no persistent todo tracking.

**After:** A 5-layer pyramid with a dedicated `.todos.md` file ensures every cross-session task persists.

## Architecture

```
Workspace Memory (5 Layers)
├── MEMORY.md              — Permanent essence (always loaded at startup)
├── memory/monthly/        — Monthly summaries
├── memory/weekly/         — Weekly summaries
├── memory/*.md            — Daily diaries (last 14 days)
└── .todos.md             — Cross-session todo list (CRITICAL!)
```

## Core Files

| File | Purpose |
|------|---------|
| `scripts/startup-read.js` | Loads all 5 layers on every startup |
| `scripts/weekly-archive.js` | Generates weekly summaries (cron: Monday 9AM) |
| `scripts/monthly-archive.js` | Generates monthly summaries (cron: monthly, last day) |
| `.todos.md` | Cross-session todo list — THE key mechanism |

## How Startup Works

On every session start, `startup-read.js` executes automatically:

```
Layer 1: MEMORY.md — Permanent essence
Layer 2: memory/monthly/*.md — All monthly summaries
Layer 3: memory/weekly/weekly-review-*.md — This month's weeks
Layer 4: memory/*.md — Last 14 days diaries
Layer 5: .todos.md — Cross-session todos ⭐
```

## The .todos.md Rule (Critical!)

**When to write to .todos.md:**
- Masone asks you to create something that can't be completed immediately
- Any cross-session project, agreement, or pending action
- Examples: "publish this skill when network restores", "wait for Masone's input"

**Format:**
```markdown
## 进行中
- [ ] Task description here

## 已完成
- [x] Completed task (keep for history)
```

**After completion:** Move the line from "进行中" to "已完成"

## Conversation Summary Rule

**After every conversation with Masone ends, write a summary immediately.**

- **When:** Trigger words ("好的"/"就这样"/"结束了"), topic switch, 5 min silence
- **Length:** ≤2000 characters
- **Where:** `memory/YYYY-MM-DD.md` (today's diary)
- **Format:**
  1. Topic (1 sentence)
  2. Core content (bullet points)
  3. Masone's preferences/corrections
  4. Todo items
  5. Self-reflection

## Cron Configuration

| Task | Cron | Script |
|------|------|--------|
| Weekly review | Monday 9AM | weekly-archive.js |
| Monthly archive | Last day of month 10AM | monthly-archive.js |

## Scripts Location

All scripts: `~/.openclaw/workspace/scripts/`

## Related Skills

- `memos-memory-guide` — MemOS memory tools (memory_search, etc.)
- `memory-never-forget` — Atkinson-Shiffrin memory model

## History

| Date | Event |
|------|-------|
| 2026-03-22 | Initial creation |
| 2026-03-27 | Enhanced with .todos.md, startup-read.js updated to 5 layers |
| 2026-03-29 | Added conversation summary rule |
| 2026-03-31 | Fixed: scripts separated, monthly cron added, template newlines fixed |

---

_This skill documents Moore's own memory system._
