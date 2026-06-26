---
name: proactive-memory-agent
version: 1.0.1
description: "Ultimate memory optimization for AI agents. Combines WAL protocol, Working Buffer, three-tier memory (HOT/WARM/COLD), context budgeting (10/40/20/20), and .learnings/ system. Maximum context efficiency with zero information loss."
description_zh: "AI智能体终极记忆优化系统。整合WAL预写协议、工作缓冲区、三级记忆架构(HOT/WARM/COLD)、上下文预算分区(10/40/20/20)和学习记录系统。实现60-70%上下文占用降低，零信息丢失保障。"
author: integrated-from-proactive-agent-context-budgeting-memory-tiering
---

# Proactive Memory Agent 🧠⚡

**The ultimate memory optimization system for OpenClaw agents.**

**OpenClaw 智能体终极记忆优化系统。**

Combines the best of three worlds:
- 🦞 **Proactive Agent** — WAL protocol, Working Buffer, learning system
- 📊 **Context Budgeting** — Strict 10/40/20/20 partitioning
- 🗂️ **Memory Tiering** — Automatic HOT/WARM/COLD archiving

**Result: 60-70% context reduction + complete learning retention + zero maintenance**

**效果：降低60-70%上下文占用 + 完整保留学习记录 + 零维护成本**

---

## 快速开始 / Quick Start

### 中文简介

**Proactive Memory Agent** 是一个专为 OpenClaw 设计的记忆优化系统，解决长会话中的上下文爆炸问题。

**核心特性：**
- 🔥 **WAL 预写协议** — 关键决策先写后回，确保信息不丢失
- ⚠️ **工作缓冲区** — 危险区(>60%)自动记录所有对话
- 📊 **上下文预算** — 严格 10/40/20/20 分区控制
- 🗂️ **三级记忆架构** — HOT→WARM→COLD 自动归档
- 📝 **学习记录系统** — 自动记录错误、纠正和最佳实践

**适用场景：**
- 长会话 (>50条消息)
- 复杂任务 (多步骤、多文件)
- 高频交互 (需要记住用户偏好)
- 成本控制 (降低token消耗)

**预期效果：**
- Context 占用降低 **60-70%**
- Token 消耗降低 **50-60%**
- 信息丢失风险 **几乎为零**

---

## Memory Architecture / 记忆架构

```
workspace/
├── SESSION-STATE.md          # 🔥 HOT: Current task (WAL target)
├── .learnings/               # 🌡️ WARM: Learning records
│   ├── ERRORS.md            — 错误记录
│   ├── LEARNINGS.md         — 学习/纠正记录
│   └── FEATURE_REQUESTS.md  — 功能请求记录
├── MEMORY.md                 # ❄️ COLD: Long-term archive
├── memory/
│   ├── hot/HOT_MEMORY.md     # 快速恢复检查点
│   ├── warm/                 # 稳定偏好/配置
│   ├── cold/                 # 长期归档
│   └── working-buffer.md     # ⚠️ 危险区日志
└── AGENTS.md/SOUL.md/TOOLS.md — 只读参考
```

---

## The Four Protocols / 四大协议

### 1️⃣ WAL Protocol (Write-Ahead Logging) / 预写协议

**Law:** Context is a BUFFER, not storage. Write first, respond second.
**法则：** 上下文是缓冲，不是存储。先写再回。

**SCAN every message for:**
**扫描每条消息中的：**
- ✏️ Corrections — "It's X, not Y" / "Actually..." / 纠正
- 📍 Proper nouns — Names, places, products / 专有名词
- 🎨 Preferences — Colors, styles, approaches / 偏好
- 📋 Decisions — "Let's do X" / "Go with Y" / 决策
- 🔢 Specific values — Numbers, dates, IDs, URLs / 具体数值

**The Protocol:**
1. **STOP** — Do not start composing your response / 停止，不要开始回复
2. **WRITE** — Update SESSION-STATE.md with the detail / 写入 SESSION-STATE.md
3. **THEN** — Respond to your human / 然后回复用户

---

### 2️⃣ Working Buffer Protocol / 工作缓冲区协议

**Purpose:** Capture EVERY exchange in the danger zone (>60% context).
**目的：** 在危险区(>60%上下文)记录每一条消息。

**中文说明：**
当上下文使用率超过 60% 时，系统自动启用工作缓冲区，记录每一条对话。即使发生压缩，也能从缓冲区恢复。

**How:**
1. At **60% context**: Clear old buffer, start fresh
2. Every message after 60%: Append to `memory/working-buffer.md`
3. After compaction: Read buffer FIRST, extract important context
4. Leave buffer as-is until next 60% threshold

---

### 3️⃣ Context Budgeting (10/40/20/20) / 上下文预算分区

**Strict partitioning / 严格分区：**

| Zone | % | Content | File | 中文说明 |
|------|---|---------|------|----------|
| **Objective** | 10% | Core task, active constraints | SESSION-STATE.md | 核心任务 |
| **Short-term** | 40% | Recent 5-10 turns raw dialogue | Working Buffer | 短期对话 |
| **Decision Log** | 20% | Summarized outcomes | .learnings/*.md | 决策日志 |
| **Background** | 20% | High-relevance snippets | MEMORY.md | 背景知识 |

**Rule:** When any zone exceeds quota, oldest content moves to lower tier.
**规则：** 任何分区超出配额时，最旧内容移至下一层级。

---

### 4️⃣ Memory Tiering (HOT → WARM → COLD) / 记忆分层归档

**Automatic lifecycle / 自动生命周期：**

```
🔥 HOT (Current session) 当前会话
   ↓ (Task complete) 任务完成
🌡️ WARM (Recurring use) 重复使用
   ↓ (30 days old / promoted) 30天旧/已提升
❄️ COLD (Archive) 归档
```

| Tier | Location | Update Frequency | Retention | 中文 |
|------|----------|-----------------|-----------|------|
| HOT | SESSION-STATE.md | Every message | Current task only | 当前任务 |
| WARM | .learnings/ | When learning occurs | Until promoted | 学习记录 |
| COLD | MEMORY.md | Weekly archival | Permanent | 长期存档 |

---

## 使用脚本 / Scripts

### 快速设置 / Quick Setup
```bash
~/.openclaw/workspace/skills/proactive-memory-agent/scripts/init.sh
```

### 日常使用 / Daily Operations
```bash
# 检测当前状态 / Check current status
~/.openclaw/workspace/skills/proactive-memory-agent/scripts/detect.sh

# 搜索记忆 / Search memories
~/.openclaw/workspace/skills/proactive-memory-agent/scripts/search.sh "关键词"

# 执行记忆分层归档 / Run memory tiering
~/.openclaw/workspace/skills/proactive-memory-agent/scripts/tiering.sh

# 创建预压缩检查点 / Create pre-compaction checkpoint
~/.openclaw/workspace/skills/proactive-memory-agent/scripts/checkpoint.sh
```

---

## 学习记录系统 / Learning System (.learnings/)

### 何时记录 / When to Record

| 场景 / Situation | 记录位置 / Record To | 类别 / Category |
|------------------|---------------------|-----------------|
| 命令失败 / Command fails | ERRORS.md | error |
| 用户纠正 / User corrects | LEARNINGS.md | correction |
| 缺失功能 / Missing feature | FEATURE_REQUESTS.md | feature_request |
| 知识过时 / Knowledge outdated | LEARNINGS.md | knowledge_gap |
| 更好方法 / Better approach | LEARNINGS.md | best_practice |

### 记录格式 / Format

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | in_progress | resolved | promoted

### Summary / 摘要
一句话描述学到了什么

### Details / 详情
What happened, what was wrong, correct approach
发生了什么，哪里错了，正确做法

### Suggested Action / 建议操作
Specific fix or improvement
具体的修复或改进建议

---
```

### 提升路径 / Promotion Path

```
Learning in .learnings/ 在学习记录中
    ↓
IF recurring (3+ times) OR broadly applicable 如果重复(3+次)或广泛适用
    ↓
Promote to / 提升到:
  ├─ Behavioral patterns → SOUL.md 行为模式
  ├─ Workflow improvements → AGENTS.md 工作流改进
  └─ Tool gotchas → TOOLS.md 工具技巧
```

---

## 心跳集成 / Heartbeat Integration

Add to `HEARTBEAT.md`:
添加到心跳文件：

```markdown
## Memory Management / 记忆管理 (每30分钟)
- [ ] Run detect.sh — 检查context使用率
- [ ] If >80%: Create checkpoint with checkpoint.sh / 创建检查点
- [ ] If >70%: Run tiering.sh to archive old content / 归档旧内容
- [ ] Review .learnings/ for pending items / 检查待处理项
```

---

## 核心原则 / Key Principles

1. **Write before respond** — WAL is non-negotiable / 先写再回，WAL不可妥协
2. **Buffer the danger zone** — >60% = automatic logging / 缓冲危险区，>60%自动记录
3. **Strict budgeting** — 10/40/20/20, no exceptions / 严格预算，10/40/20/20无例外
4. **Auto-tiering** — HOT→WARM→COLD without manual effort / 自动分层，无需手动
5. **Promote aggressively** — Recurring patterns become permanent / 积极提升，重复模式永久化
6. **Never lose context** — Working Buffer + Compaction Recovery / 永不丢失，缓冲+恢复

---

## 预期效果 / Expected Results

| Metric / 指标 | Before / 之前 | After / 之后 | Improvement / 改进 |
|---------------|---------------|--------------|-------------------|
| Context usage / 上下文占用 | 100% | 30-40% | **60-70% reduction** |
| Token consumption / Token消耗 | Baseline / 基准 | -50-60% | **Major savings** |
| Maintenance / 维护成本 | High / 高 | Minimal / 极低 | **Auto-tiering** |
| Information loss / 信息丢失 | Risk / 有风险 | Zero / 零 | **Buffer protection** |

---

## Changelog / 更新日志

### v1.0.1 (2026-03-24)
- Added Chinese documentation / 添加中文文档
- Improved README with bilingual support / 改进双语支持
- Fixed minor formatting issues / 修复格式问题

### v1.0.0 (2026-03-24)
- Initial release / 初始版本
- Integrated: proactive-agent + context-budgeting + memory-tiering / 整合三大技能
- 5 management scripts included / 包含5个管理脚本
- Full documentation in SKILL.md / 完整文档

---

## License / 许可证

MIT License — Free to use, modify, distribute.
MIT 许可证 — 自由使用、修改、分发。

---

*Part of the Hal Stack 🦞 + Self-Improvement Integration*
*Integrated by @silaszhu*
