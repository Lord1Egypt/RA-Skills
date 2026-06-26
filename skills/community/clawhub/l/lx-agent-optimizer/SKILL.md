---
name: lx-agent-optimizer
slug: lx-agent-optimizer
version: 1.3.1
description: |
  A battle-tested agent self-improvement system built by a non-coder from weeks of real-world usage with OpenClaw.
  No fluff, no theory — every rule here was learned from something that actually broke.
  Covers: behavior learning, proactive patterns, cron discipline, cost control, and false-positive prevention.
  Use when: you want your agent to get smarter over time, stay lean, and stop interrupting you with noise.
author: paoloxiamn
license: MIT
tags: [self-improvement, optimization, proactive, cron, cost-control, learning]
---

# LX Agent Optimizer

A unified skill for agents that want to **learn, act proactively, run lean, and cost less** — built from real production experience, not theory.

> Born from weeks of real usage by Paolo + LX (OpenClaw). Every pattern here was tested, broke something, got fixed, and survived.
>
> **Notably: this skill was created by a non-coder author.**
> That is exactly why it is practical — it focuses on observable failures, reusable workflows, and user experience, instead of abstract agent philosophy.

---

## Four Pillars

### 1. 🧠 Behavior Learning
Learn from real mistakes. Write them down. Review weekly. Change behavior.

→ See `references/behavior-learning.md`

### 2. 🎯 Proactive Patterns
Know when to speak up, when to stay silent, and when to just do it.

→ See `references/proactive-patterns.md`

### 3. ⚙️ Cron Discipline
Script-first cron jobs that are silent on success, reliable, and cheap.

→ See `references/cron-discipline.md`

### 4. 💰 Cost Control
Token spend is real. Route models wisely, cache aggressively, stay lean.

→ See `references/cost-control.md`

---

## Quick Start

### Step 1: Set up improvement log
```bash
touch ~/.openclaw/workspace/improvement_log.md
```

Add this header:
```markdown
# Agent Improvement Log
Record weekly: problems encountered, lessons learned, behavior changes.
```

### Step 2: Add weekly analysis cron (main session)
```json
{
  "name": "Weekly Self-Improvement",
  "schedule": { "kind": "cron", "expr": "0 9 * * 1", "tz": "Asia/Shanghai" },
  "sessionTarget": "main",
  "payload": {
    "kind": "systemEvent",
    "text": "⏰ Weekly improvement: read improvement_log.md, review last week's problems, add 2-3 new lessons, send brief report to user."
  }
}
```

### Step 3: Run the optimizer audit
Say: **"audit my agent setup"** — the skill will analyze your workspace and propose improvements.

---

## Core Rules (Non-Negotiable)

These were learned the hard way:

| Rule | Why |
|------|-----|
| **File writes → main session only** | work agents can't write files; main session can |
| **Data fetch → validate with curl first** | SPAs return empty shells; APIs return 403; test before shipping |
| **Debugging → internal, not exposed** | User sees results, not "trying A... trying B..." |
| **Infer before asking** | Read filenames, context, history — ask only when truly ambiguous |
| **Script-first cron** | Embed logic in `.py` files, not in cron message prompts |
| **Silent on success** | Only alert on anomalies, errors, or changes |
| **Channel health checks → real-time probe, not stale logs** | Historical cron errors may be old; verify current channel state before alerting or auto-remediating |
| **Cron alerts → classify error type before paging user** | Delivery failure, task logic failure, and node failure need different handling; don't treat them as the same outage |
| **Reminder source mapping → check both cron and HEARTBEAT.md** | Some reminders live in cron jobs, others live in heartbeat rules; disabling one side is not enough |
| **Success once ≠ learned** | A task is only truly learned after the verified path is written into external memory (`TOOLS.md`, improvement log, or long-term memory) |

---

## Tool Path Memory (Verified)

| Task | Use This | Not This |
|------|----------|----------|
| Token usage data | `~/.openclaw/agents/*/sessions/*.jsonl` | codexbar, gateway.log |
| WeChat article body | `agent-browser eval "document.querySelector('#js_content')?.innerText"` | Built-in browser tool |
| PDF image extraction | `pdfimages -j <file> /tmp/out` | pymupdf (not installed) |
| Send image to user | `message` tool (media/filePath) | Absolute/~ paths |
| Sports data (no API key) | ESPN public API | sofascore (403), official site (SPA) |
| Apple Calendar today events | Run `python3 /Users/paolo/.openclaw/workspace/skills/calendar-morning/scripts/today_events.py` on Paolo's Mac mini; under the hood it uses `/usr/bin/osascript` + Calendar.app | Re-guessing the tool, calendar names, or prompting from scratch |
| Telegram channel health check | Send a **silent real-time probe** via `message` tool and only remediate/alert on actual send failure | Scanning historical cron `lastError` / `deliveryStatus` and assuming the channel is currently down |
| Cron anomaly triage | First classify as **delivery failure / task failure / node failure**, then decide whether to alert, retry, or remediate | Treating every `consecutiveErrors > 0` as the same kind of outage |
| Reminder disable audit | Check **both** cron jobs and `HEARTBEAT.md` before saying a reminder is removed | Looking only at cron list and missing heartbeat-driven reminders |

---

## Weekly Improvement Cycle

```
Monday 9:00 AM
    ↓
Read improvement_log.md
    ↓
Review last week's conversations for:
  - Tasks that needed retries
  - Times user waited too long
  - Wrong tool choices
  - Repeated mistakes
    ↓
Write 2-3 new lessons to improvement_log.md
    ↓
Send brief report: "N problems this week, key lesson: X, focus next week: Y"
```

---

## Proactive Trigger Rules

**Reach out when:**
- Important email or calendar event incoming (< 2h)
- Cron task failed with consecutive errors
- Something discovered user would want to know
- Haven't spoken in > 8h during waking hours

**Stay silent when:**
- Late night (23:00–08:00) unless urgent
- User is clearly busy
- Nothing new since last check
- Just checked < 30 min ago
- Task succeeded (success = silent)

**Do without asking:**
- Read files, search, organize
- Execute cron/heartbeat checks
- Update memory and logs
- Commit workspace changes

**Always ask first:**
- Send emails, tweets, public posts
- Delete data
- Spend money
- Make commitments for the user

---

## Heartbeat Design

Heartbeat = **control plane only** (cheap).

✅ Good heartbeat tasks:
- Check cron consecutiveErrors
- **Classify cron errors by type** (delivery / task / node) before deciding whether to alert
- Check if Telegram channel is down
- Quick calendar scan

❌ Move to isolated cron instead:
- Heavy data fetching
- Report generation
- Multi-tool workflows

```
HEARTBEAT_OK  ← 99% of the time
Alert only when: errors > 0, channel down, something changed
```

**Important:** heartbeat may use cron error state to spot anomalies, but **must not auto-remediate Telegram/channel issues from stale cron history alone**. Use cron state to detect "something looks wrong," then verify with a live probe before fallback alerts or recovery actions.

---

## Cron Design Checklist

Before shipping any cron job:

- [ ] Logic is in a `.py` script, not embedded in the prompt
- [ ] Script tested locally with `python3 script.py`
- [ ] Silent on success (`exit(0)` with no output = no message sent)
- [ ] Output is minimal (< 200 chars for routine alerts)
- [ ] Model is cheapest tier that works (e.g., `qwen-plus` for simple tasks)
- [ ] Timeout is realistic (not too short = retries, not too long = waste)
- [ ] File writes use main session, not work agent
- [ ] Validated data source with curl before embedding URL

---

## Model Selection Guide

| Task Type | Recommended Tier | Example |
|-----------|-----------------|---------|
| Simple fetch + format | cheapest (qwen-plus / gemini-lite) | sports results, reminders, weather |
| **固定流程任务**（文章总结、写文件、数据抓取） | qwen-plus | 微信文章总结、Obsidian 写入、cron 推送 |
| **中文内容处理**（总结/整理/改写） | qwen-plus | 中文语境更准，比 claude 省 token |
| 周复盘 / cron 状态检查 | gemini-2.5-flash | 够用，比 sonnet 便宜 |
| Reasoning + writing | mid-tier (sonnet) | self-improvement analysis, strategy |
| Complex multi-step | high-tier (opus) | only when mid-tier fails repeatedly |

**分工原则：主 session（claude）只做判断+调度+对话；固定流程和中文任务一律 sessions_spawn → qwen-plus。**

**主模型注意事项（2026-03-28）：**
- 不要把 Gemini 设为主 session 默认模型 → `compaction.mode: safeguard` 与 Gemini preview 模型有 API 兼容性问题，导致 400 报错
- Gemini 适合做 fallback 或在 isolated cron 中指定使用
- 主 session 保持 `renlijia/claude-sonnet-4-6`

**Cost rule:** Cache hit rate > 70% = healthy. If < 40%, you're creating too many new sessions.

---

## Files

- `references/behavior-learning.md` — improvement log format and weekly cycle
- `references/proactive-patterns.md` — when to act, when to stay quiet
- `references/cron-discipline.md` — script-first cron patterns, error classification, and channel-health rules
- `references/cost-control.md` — token cost reduction playbook
- `scripts/token_report.py` — weekly token usage report script

---

## Hermes-Inspired Extensions（v1.4）

三个从 Hermes Agent 框架借鉴的自进化机制，补充原有四大支柱。

### 5. 📋 Skill Awareness（技能感知层）

Agent 应该主动知道自己有什么能力，而不是靠记忆猜。

**每周扫描机制：**
```bash
ls /Users/paolo/.openclaw/workspace/skills/
```
扫描后更新 `memory/skill-registry.md`，格式：
```markdown
# Skill Registry（更新日期：YYYY-MM-DD）
- skill-name: 一句话描述，适用场景
```

**触发规则：**
- 每周一自检一次，有新 Skill 时更新
- 接到任务前先查 `skill-registry.md`，判断是否有现成 Skill 可用
- 优先复用已验证的 Skill，不要重新摸索相同路径

---

### 6. 🔁 Memory Recall Gate（记忆召回门控）

在处理较复杂任务前，先主动搜索记忆库，复用已有成功路径。

**执行流程：**
```
接到任务
  ↓
memory_search（关键词：任务类型 + 工具名）
  ↓
命中成功路径？
  ├── 是 → 直接复用，记录为"路径复用"
  └── 否 → 重新执行，执行完后记录路径到 TOOLS.md 或 improvement_log.md
```

**规则：**
- 命中率低（连续 3 次同类任务都没命中记忆）→ 说明记忆库记录不足，补录
- 禁止"凭印象试错"：有相似历史路径一定先查，再动手
- 验证路径写入格式：`TOOLS.md | 已验证工具路径` 表格

---

### 7. 📊 Task Quality Signal（任务质量反馈）

每次执行较复杂任务后，记录结果质量，形成可追踪的成功率数据。

**记录格式**（追加到 `improvement_log.md`）：
```markdown
## Task Signal（YYYY-MM-DD）
- 任务：[任务简述]
- 结果：✅ 成功 / ⚠️ 部分成功 / ❌ 失败
- 是否重试：否 / 是（N次）
- 关键路径：[用了什么工具/命令]
- 教训（失败时）：[一句话]
```

**什么算"较复杂任务"：**
- 调用超过 2 个工具
- 涉及文件写入 / cron 变更 / 外部 API
- 用户明确说"帮我做XX"

**周报中汇报：**
> 本周任务信号：共 N 次，成功率 X%，重试 Y 次，最高频失败点：Z
