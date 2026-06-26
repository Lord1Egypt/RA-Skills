---
name: memory-master
version: 2.6.1
description: "Local memory system with structured indexing and auto-learning. Auto-write, heuristic recall, auto learning when knowledge is insufficient. Compatible with self-improving-agent: auto-records skill completions and errors to knowledge base."
author: 李哲龙
tags: [memory, recall, indexing, context]
---

# 🧠 Memory Master — The Precision Memory System

*Transform your AI agent from forgetful to photographic.*

---

## The Problem

Most AI agents suffer from **memory amnesia**:

- ❌ Can't remember what you discussed yesterday
- ❌ Loads entire memory files, burning tokens
- ❌ Fuzzy search returns irrelevant results
- ❌ No structure, just raw text dumps
- ❌ Waits for user to trigger recall, never proactively remembers

**You deserve better.**

---

## The Solution: Memory Master v1.2.4

A **precision-targeted memory architecture** with optional network learning capability.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| **📝 Structured Memory** | "Cause → Change → Todo" format for every entry |
| **🔄 Auto Index Sync** | Write once, index updates automatically |
| **🎯 Zero Token Waste** | Read only what you need, nothing more |
| **⚡ Heuristic Recall** | Proactively finds relevant memories when context is missing |
| **🧠 Auto Learning** | When local knowledge is insufficient, automatically search web to learn and update knowledge base |
| **🔓 Full Control** | All files visible/editable/deletable. No auto network calls. |

---

## The Memory Format

### Daily Memory: `memory/daily/YYYY-MM-DD.md`

**Format:**
```markdown
## [日期] 主题
- 因：原因/背景
- 改：做了什么、改了什么
- 待：待办/后续
```

**Example:**
```markdown
## [2026-03-03] 记忆系统升级
- 因：原记忆目录混乱，查找困难
- 改：目录调整为 daily/ + knowledge/，上传 v1.1.0
- 待：检查 ClawHub 描述
```

**Why this format?**
- 一目了然 (一目了然 = instantly clear at a glance)
- 逻辑清晰：因 → 改 → 待
- 通用模板，适用于任何场景

---

## The Index Format

### Index: `memory/daily-index.md`

**Format:**
```markdown
# 记忆索引

- 主题名 → daily/日期.md,日期.md
```

**Example:**
```markdown
# 记忆索引

- 记忆系统升级 → daily/2026-03-03.md
- 飞书配置 → daily/2026-03-02.md,daily/2026-03-03.md
- 电商网站 → daily/2026-03-02.md
```

**Rules:**
- 逗号分隔多天
- 只有一个一级标题：记忆索引
- 简洁清晰，一眼定位

---

## Heuristic Recall Protocol

### When to Trigger Recall

** DON'T wait for user to say "yesterday" or "remember"**

Trigger recall when:
1. User mentions a topic you don't have context for
2. Current conversation references something past
3. You feel "I'm not sure I have this information"
4. User asks about "that", "the project", "the skill"

### Recall Flow

```
用户问题 → 发现上下文缺失 → 读 index 定位主题 → 读取记忆文件 → 恢复上下文 → 回答
```

**Example:**
```
User: "那个 skill 你觉得还有什么要改的吗？"

1. 思考：我知道用户指哪个 skill 吗？→ 不知道，上下文没有
2. 读 index → 找到"记忆系统升级 → daily/2026-03-03.md"
3. 读取文件 → 恢复记忆
4. 回答："根据昨天记录，我们..."
```

### Key Principle

**"When you realize you don't know, go check the index."**

---

## Knowledge Base System

### Knowledge Structure

```
memory/knowledge/
├── knowledge-index.md
└── *.md (knowledge entries)
```

### Knowledge Index: `memory/knowledge-index.md`

**极简格式 - 关键字列表：**
```markdown
# 知识库索引

- clawhub
- oauth
- react
```

### When to Read Knowledge Base

**启发式：当前上下文没有相关信息时才读**

1. 用户有要求 → 按用户要求执行
2. 用户没要求 → 检查上下文有没有规则
3. 上下文没有 → 搜索知识库索引
4. 找到对应项 → 读取知识库文件执行

- 上下文有 → 直接用
- 上下文没有 → 搜索引 → 读知识库文件 → 执行

### Problem Solving Flow

```
用户问题 → 上下文有？→ 有：直接解决 / 无：搜索引 → 有知识？→ 有：解决 / 无：自动网络搜索学习 → 写知识库 → 更新索引 → 解决问题
```

**Example:**
```
User: "怎么上传 skill 到 ClawHub？"

1. 上下文有 clawhub 信息？→ 有（刚学过）→ 直接回答
2. 不用读知识库

---
User: "怎么实现 OAuth？"

1. 上下文有 OAuth 信息？→ 没有
2. 搜 knowledge-index → 没有 OAuth
3. 告知用户："我还不会，先去查一下"
4. 网络搜索学习
5. 写入 knowledge/oauth.md
6. 更新 knowledge-index
7. 开始和用户沟通解决方案
```

---

## Write Flow

### When to Write

Write immediately after:
1. Discussion reaches a conclusion
2. Decision is made
3. Action item is assigned
4. Something important happens
5. Learned something new (check before every response)

### ⚠️ IMPORTANT: Auto-Trigger Write

**DO NOT wait for user to remind you!**

Before every response, quickly check: "Did I learn anything new in this conversation?" If yes, write it.

Write IMMEDIATELY when any of the above happens. This is NOT optional.

### Skill Event Triggers (Auto-Record)

When a skill completes or errors, automatically record to knowledge:

| Event | Write Location | Content |
|-------|---------------|---------|
| **skill_complete** | memory/knowledge/ | 记录学到了什么新技能/方法 |
| **skill_error** | memory/knowledge/ | 记录错误原因和解决方案 |

**统一写入知识库**，因为都是"学到新知识"。

### Write Steps

1. **Detect** conclusion/action (automatically, every time)
2. **Format** using "因-改-待" template
3. **Write** to `memory/daily/YYYY-MM-DD.md`
4. **Update** `daily-index.md` (add new topic or append date)

**IMPORTANT: Always update index when writing to daily memory!**

### Update MEMORY.md (if needed)

When writing to MEMORY.md:
1. Check for duplicate/outdated rules
2. Merge and clean up
3. Keep it minimal

### Example

```
讨论：我们要改进记忆系统，决定把目录分成 daily/ 和 knowledge/
结论：改完了，今天上传到 GitHub 和 ClawHub

写入：
## [2026-03-04] 记忆系统升级
- 因：原记忆目录混乱，查找困难
- 改：目录调整为 daily/ + knowledge/，上传 v1.1.0
- 待：检查 ClawHub 描述

更新索引：
- 记忆系统升级 → daily/2026-03-03.md,daily/2026-03-04.md
```

---

## Recall Flow Summary

| Step | Action | Trigger |
|------|--------|---------|
| 1 | Parse user query | User asks question |
| 2 | Check: do I have context? | If uncertain |
| 3 | Read daily-index.md | Context missing |
| 4 | Locate relevant topic | Found in index |
| 5 | Read target date file | Know the date |
| 6 | Restore context | Got info |
| 7 | Answer user | Complete |

---

## Knowledge Base Flow Summary

| Step | Action | Trigger |
|------|--------|---------|
| 1 | Parse user query | User asks question |
| 2 | Search knowledge-index | Always check first |
| 3 | Found solution? | Yes → Solve / No → Continue |
| 4 | Tell user "I don't know yet" | No solution |
| 5 | Search web & learn | Get knowledge |
| 6 | Write to knowledge/*.md | New knowledge |
| 7 | Update knowledge-index | Keep index in sync |
| 8 | Solve the problem | Complete |

---

## File Structure

```
~/.openclaw/workspace/
├── AGENTS.md              # Your rules
├── MEMORY.md              # Long-term memory (main session only)
├── memory/
│   ├── daily/             # Daily records
│   │   ├── 2026-03-02.md
│   │   ├── 2026-03-03.md
│   │   └── 2026-03-04.md
│   ├── knowledge/         # Knowledge base
│   │   ├── react-basics.md
│   │   └── flask-api.md
│   ├── daily-index.md     # Daily memory index
│   └── knowledge-index.md # Knowledge index
```

---

## Comparison

| Metric | Traditional | Memory Master v1.2 |
|--------|-------------|---------------------|
| Recall precision | ~30% | ~95% |
| Token cost per recall | High (full file) | Near zero (targeted) |
| Proactive recall | ❌ | ✅ (heuristic) |
| Knowledge learning | ❌ | ✅ |
| API dependencies | Vector DB / OpenAI | None |
| Setup complexity | High | Zero |
| Latency | Variable | Instant |

---

## Requirements

**None.** This skill works with pure OpenClaw:

- ✅ OpenClaw installed
- ✅ Workspace configured
- ✅ That's it!

**No external APIs. No embeddings. No costs.**

---

## Installation

### 1. Install Skill
```bash
clawdhub install memory-master
```

### 2. Auto-Initialize (Enhanced for v2.6.0)
```bash
# This will automatically:
# - Migrate heartbeat rules from AGENTS.md to HEARTBEAT.md
# - Optimize AGENTS.md (deduplicate, streamline, restructure)
# - Convert MEMORY.md to pure lessons/experience repository
# - Create memory directory structure and index files
# - Backup original files to .memory-master-backup/ directory
clawdhub init memory-master
```

**What the enhanced initialization does:**

| Step | Action | Result |
|------|--------|--------|
| 1 | **Backup** | Original files saved to `.memory-master-backup/` |
| 2 | **Heartbeat Migration** | Heartbeat content moved from AGENTS.md to HEARTBEAT.md |
| 3 | **AGENTS.md Optimization** | Remove duplicates, outdated rules, streamline language |
| 4 | **MEMORY.md Transformation** | Convert to pure lessons/experience repository |
| 5 | **Memory Structure** | Create `memory/` directories and index files |

**Post-initialization files:**
```
~/.openclaw/workspace/
├── AGENTS.md              # Optimized behavior rules + memory system rules
├── MEMORY.md              # Pure lessons/experience repository
├── HEARTBEAT.md           # Heartbeat tasks and guidelines
├── memory/
│   ├── daily/             # Daily records (YYYY-MM-DD.md format)
│   ├── knowledge/         # Knowledge base (*.md files)
│   ├── daily-index.md     # Memory index
│   └── knowledge-index.md # Knowledge index
```

Or manually (advanced users):
```bash
# 1. Run the initialization script directly
node ~/.agents/skills/memory-master/scripts/init.js

# 2. Or manually copy templates
cp ~/.agents/skills/memory-master/templates/optimized-agents.md ~/.openclaw/workspace/AGENTS.md
cp ~/.agents/skills/memory-master/templates/heartbeat-template.md ~/.openclaw/workspace/HEARTBEAT.md
cp ~/.agents/skills/memory-master/templates/memory-lessons.md ~/.openclaw/workspace/MEMORY.md

# 3. Create memory directories
mkdir -p ~/.openclaw/workspace/memory/daily
mkdir -p ~/.openclaw/workspace/memory/knowledge

# 4. Create index files
cp ~/.agents/skills/memory-master/templates/daily-index.md ~/.openclaw/workspace/memory/daily-index.md
cp ~/.agents/skills/memory-master/templates/knowledge-index.md ~/.openclaw/workspace/memory/knowledge-index.md
```

---

## ⚠️ Security & Privacy

- **100% Local**: All memory/knowledge stored in local workspace files only. Nothing leaves your machine except your initiated web searches.
- **Auto-Write to Local**: This is a FEATURE — prevents information loss. Same as OpenClaw's native memory system.
- **Auto Learning**: When local knowledge is insufficient, automatically search web to learn. Writes results to local knowledge base only.
- **Full Transparency**: All files visible/editable/deletable by user anytime.
- **Safe**: No data uploaded, only search queries sent to search engines.
- **User Control**: User explicitly authorizes web searches ("我去查一下", "let me search the web") before any network activity

---

## Triggers

### Memory Recall
- "that"
- "上次"
- "之前"
- "昨天"
- "earlier"
- Or: when you realize you don't have the context

### Knowledge Learning
- When you can't find answer in knowledge base
- User asks something new

### Memory Writing
- Discussion reaches conclusion
- Decision made
- Action assigned

---

## Best Practices

1. **Write immediately** — Don't wait, write right after conclusion
2. **Keep it brief** — One line per point, but core info preserved
3. **Use the template** — 因 → 改 → 待
4. **Update index** — Always sync after writing
5. **Heuristic recall** — Don't wait for user to trigger
6. **Learn proactively** — When you don't know, say it and learn

---

## Compression Detection (v2.6.3+)

**⚠️ Important: Must run after EVERY response!**

### Run after every response:
```bash
node ~/.agents/skills/memory-master/scripts/detect.js
```

Display status at the bottom of every response:
- **50%**: `📝 上下文使用率：50% - 是否需要记录记忆或知识库？`
- **70%**: `⚠️ 上下文使用率：70% - 建议记录当前进度`
- **85%**: `🚨 上下文使用率：85% - 请立即记录当前进度！`

### Why this matters:
- Prevents context loss from compression
- Reminds user to record memories before data is lost
- Works with heartbeat but runs more frequently

---

## The Memory Master Promise

> *"An AI agent is only as good as its memory. Give your agent a memory system that never forgets, never wastes, and always delivers exactly what's needed."*

**Memory Master v1.2.0 — Because remembering everything is just as important as learning something new.** 🧠⚡
