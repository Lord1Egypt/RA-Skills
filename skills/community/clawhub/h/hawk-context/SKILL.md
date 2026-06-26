---
name: context-compressor
description: |
  Context Compressor — Real-time conversation context compression engine. Activates when user says "compress context", "压缩上下文", "上下文爆了", "context full", "上下文瘦身", "reduce context", or when context exceeds 70% threshold. This skill compresses the CURRENT conversation history into a clean, short prompt. NOT a memory manager — pure context compression tool.
  
  Core capabilities:
  - Compress current chat history (180k → 30k instantly)
  - Auto-trigger at 70% context threshold
  - Structured JSON output with compression metrics
  - Preserve system prompt, keep recent N messages intact
  - Summarize older messages with configurable intensity
  - No database, no dependencies, pure Python
---

# Context Compressor 🦅

> **纯上下文压缩引擎** — 不是记忆库，是救命工具。
> 当上下文爆炸前，压缩当前对话，继续轻松对话。

---

## 核心定位

| 工具 | 做什么 | 何时用 |
|------|--------|--------|
| **Context Compressor** | 压缩当前对话上下文 | 现在、立刻、当上下文快满 |
| memory-lancedb-pro | 跨会话持久记忆 | 对话之间存取知识 |
| context-hawk | 长期记忆管理 | 日常沉淀 |

**Context Compressor = 急救工具。memory-lancedb-pro/context-hawk = 日常工具。**

---

## 触发方式

**自动触发**（推荐）：
- 上下文超过 70% 时自动提示压缩
- 每 10 轮对话自动检查水位

**手动触发**：
- "压缩上下文" / "compress context"
- "上下文爆了" / "context full"
- "瘦身" / "reduce context"
- `/compress`

---



## Quick Start

```bash
# Install skill
openclaw skills install ./context-compressor.skill

# Auto-link command to ~/bin (one-time)
bash ~/.openclaw/workspace/skills/context-compressor/scripts/install.sh
source ~/.bashrc

# Compress current conversation
hawk-compress --level normal --keep 5

# Dry run (preview)
hawk-compress --dry-run --level light --keep 3

# Python API
python3 -c "from hawk_compress import ContextCompressor; \
  c = ContextCompressor(keep_recent=5); \
  r = c.compress(your_chat_history); \
  print(r['stats']['ratio'])"
```

## 压缩原理

### 输入（压缩前）

```
[完整对话历史 — 180k tokens — 爆炸边缘]
System: 你是一个助手...
User: 第一个问题...
Assistant: 第一个回答...
User: 第二个问题...
Assistant: 第二个回答...
... (越来越长)
```

### 输出（压缩后）

```json
{
  "compressed_prompt": "...[结构化压缩后的对话]...",
  "original_tokens": 180000,
  "compressed_tokens": 32000,
  "ratio": "5.6x",
  "kept_messages": 5,
  "summarized_count": 87,
  "compression_level": "normal",
  "timestamp": "2026-03-29T00:39:00+08:00"
}
```

---

## 压缩层级

| 层级 | 触发 | 效果 | 适用 |
|------|------|------|------|
| `light` | 60-70% | 摘要 > 30天的消息 | 日常维护 |
| `normal` | 70-85% | 摘要 + 保留最近10轮 | 推荐默认 |
| `heavy` | 85-95% | 只保留最近5轮 + 核心摘要 | 紧急急救 |
| `emergency` | > 95% | 只保留系统提示 + 最近3轮 | 立即执行 |

---

## 系统指令永久保留

以下内容**永远不参与压缩**（完整保留）：

- System Prompt / SOUL.md / AGENTS.md
- 用户设定的角色定义
- 核心规则和约束
- 当前的任务描述

---

## 重要度过滤

压缩时自动判断每条消息的重要度：

| 重要度 | 消息类型 | 处理方式 |
|--------|---------|---------|
| 🔴 极高 | 决策/规则/任务 | 保留原文 |
| 🟡 高 | 技术方案/代码片段 | 保留摘要 |
| 🟢 中 | 一般讨论 | 摘要或合并 |
| ⚪ 低 | 闲聊/确认/废话 | **直接丢弃** |

---

## 压缩策略

### 1. 消息摘要
把每条老消息压缩为一句话：
```
User: 讨论了Laravel的四层架构，讨论了Controller层的作用...
  → [摘要] User就Laravel四层架构提出问题
```

### 2. 合并重复
重复的说明/确认/指令合并为一条：
```
User: 好的
User: 好的
User: 明白了
  → [合并] User确认理解
```

### 3. 代码折叠
长代码片段只保留文件路径和关键行号：
```
[代码: app/Logic/OrderLogic.php — 45行] → [代码折叠]
```

### 4. 时间戳裁剪
同一时间段内的密集对话压缩为一条：
```
[上午10:00-10:30 共12轮对话] → [摘要]
```

---

## 压缩后的上下文格式

```
## 对话摘要

[最近5轮完整对话]
User: 最新问题...
Assistant: 最新回答...

[历史摘要]
- 2026-03-28: 讨论了Skill架构，决定不拆分
- 2026-03-28: 补充了DAO查询模式
- 2026-03-28: 完成qujin-laravel-team Skill v2

## 任务状态
- 当前任务：压缩上下文
- 进度：进行中

## 核心规则（永久保留）
[系统提示内容]

## 用户偏好（永久保留）
[关键偏好]
```

---

## 参考文档

| 文档 | 用途 |
|------|------|
| [references/compression-logic.md](references/compression-logic.md) | 压缩算法详解 |
| [references/auto-trigger.md](references/auto-trigger.md) | 自动触发机制 |
| [references/structured-output.md](references/structured-output.md) | JSON输出格式 |
| [references/cli.md](references/cli.md) | CLI工具 |
