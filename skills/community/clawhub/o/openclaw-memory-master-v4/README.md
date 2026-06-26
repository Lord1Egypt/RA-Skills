# 🧠 Memory Master v2.6.1

**Local Memory System with Structured Indexing and Auto-Learning**

---

## What is Memory Master?

A memory system for AI agents with **auto-write**, **heuristic recall**, and **auto learning**. Also compatible with self-improving-agent patterns.

---

## ✨ v2.6.1 What's New

### Key Improvements

| Improvement | Benefit |
|-------------|---------|
| **Rules in AGENTS.md** | Rules execute reliably — AGENTS.md loads every session |
| **Less Token Usage** | No extra loading — AGENTS.md is always in context |
| **Clearer Architecture** | AGENTS.md = rules, MEMORY.md = lessons only |
| **Auto Migration** | Upgrading automatically migrates old rules |

### Why This Matters

**Before:**
- MEMORY.md had both rules + lessons → loaded only in main session
- Rules might not execute → "I forgot to record"
- More tokens spent → entire MEMORY.md loaded every time

**After:**
- Rules in AGENTS.md → always in context, always executed
- MEMORY.md = pure lessons → lightweight, loaded every session
- **~50% less tokens** — no duplicate rule loading

---

## Core Features

- 📝 **Structured Memory**: "Cause → Change → Todo" format
- 🔄 **Auto Index Sync**: Write once, index updates automatically  
- ⚡ **Heuristic Recall**: Proactively finds relevant memories when context is missing
- 🧠 **Auto Learning**: When knowledge is insufficient, automatically search web to learn
- 🎯 **Rules Strictly Executed**: Rules in AGENTS.md = guaranteed execution
- 🔒 **100% Local**: All data stored locally, nothing leaves your machine
- 🔓 **Transparent**: All files visible/editable/deletable

---

## What Can It Do?

### 1. Auto-Write Memory
- Automatically records discussions when conclusions are reached
- Records decisions, action items, important events
- No need to remind the AI - it writes automatically

### 2. Rules Strictly Executed
- Rules live in AGENTS.md → loads every session
- **No more "I forgot to record"** — rules are always in context
- 50% less token usage — no duplicate rule loading. Heuristic Recall
- When context

### 3 is missing, proactively searches index to find relevant memories
- No need for user to say "remember" — AI finds it automatically

### 4. Auto Learning
- When knowledge is insufficient, automatically searches the web to learn
- Writes new knowledge to knowledge base for future use

---

## Directory Structure

```
~/.openclaw/workspace/
├── AGENTS.md              # Rules (always in context)
├── MEMORY.md              # Important lessons only
├── memory/
│   ├── daily-index.md     # Memory index
│   ├── knowledge-index.md # Knowledge index
│   ├── daily/             # Daily memories
│   └── knowledge/         # Knowledge base
```

---

## Memory Format

```
## [日期] 主题
- 因：原因/背景
- 改：做了什么
- 待：待办
```

---

## Quick Start

```bash
# Install
clawdhub install memory-master

# Initialize (Enhanced v2.6.1 auto-migration)
clawdhub init memory-master
```

**Enhanced Auto-migration (v2.6.1):**
- Migrates heartbeat rules from AGENTS.md → HEARTBEAT.md
- Optimizes AGENTS.md (deduplicates, streamlines, restructures)
- Converts MEMORY.md → pure lessons/experience repository
- Creates memory directory structure and index files
- Backs up original files to `.memory-master-backup/`

---

## Comparison

| Feature | v2.5.x | v2.6.1 |
|---------|--------|---------|
| Rules execution | May fail | ✅ Guaranteed |
| Token usage | Higher | ✅ ~50% less |
| Architecture | Mixed | ✅ Clear |
| Auto-migration | ❌ | ✅ |

---

## Compression Detection (v2.6.3+)

**⚠️ Must run after EVERY response!**

```bash
node ~/.agents/skills/memory-master/scripts/detect.js
```
Display status after every response:
- 50%: `📝 上下文使用率：50% - 是否需要记录记忆或知识库？`
- 70%: `⚠️ 上下文使用率：70% - 建议记录当前进度`
- 85%: `🚨 上下文使用率：85% - 请立即记录当前进度！`

---

## Rules Summary

- Rules in AGENTS.md → always executed
- Write automatically when discussion reaches conclusion
- Learn automatically when knowledge is insufficient
- Full user control: all files visible/editable/deletable

---

## ⚠️ Upgrade Note

v2.6.1 will automatically:
1. Merge rules into AGENTS.md
2. Convert MEMORY.md to lessons-only
3. Create/update index files

**Backup recommended before upgrading.**

---

**Memory Master** — *Remember what matters, forget what doesn't.* 🧠⚡
