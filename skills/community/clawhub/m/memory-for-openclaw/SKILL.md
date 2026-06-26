---
name: long-term-memory
description: AI记忆中间件 - 为AI Agent提供持久化、跨会话的长期记忆能力。自动捕获关键事实、决策、用户偏好和项目上下文，支持语义搜索和向量检索。适用于需要记忆连续性的所有AI场景。
pricing:
  community: "开源免费，本地自部署无限制"
  remote_deploy: "¥199/次"
  maas_starter: "¥49/月（2026年6月上线）"
publisher:
  wechat: "18923788188 王工"
version: 1.2.0
---

# Long-Term Memory — AI 记忆中间件

## Overview

为 AI Agent 提供 **长期记忆** 能力，解决大模型「过目就忘」的痛点。自动捕获关键事实、决策、用户偏好和项目上下文，支持语义搜索和向量检索，让 AI 真正记住你。

---

## 🚀 版本与定价

### 社区版（开源免费）

当前版本为**开源社区版**，适合个人开发者本地自部署。
✅ 所有功能无限制使用
✅ 无记忆条数限制
✅ 无需注册、无需付费

---

### 💼 企业版 / 技术支持服务

本地部署遇到困难？需要定制化配置？我来帮你搞定。

| 服务项目 | 价格 | 说明 |
|:---|---:|:---|
| **远程部署** | **¥199/次** | 远程帮你搭好完整环境，跑通持久化记忆 |
| **定制开发** | 另议 | 根据需求定制功能、对接现有系统 |
| **技术咨询** | 另议 | 架构设计、方案评审、性能优化 |

> 📞 **联系我们**：微信 **18923788188**（王工）

---

### ☁️ MaaS 云服务（2026年6月公测预告）

即插即用的云端记忆服务，无需部署，开箱即用。

| 套餐 | 价格 | 容量 | 功能 |
|:---|---:|---|---|
| **公测版** | **免费** | 前100条免费 | 云端API、基础记忆存储 |
| **Starter** | **¥49/月** | 1万条记忆，3个项目 | 标签分类、项目隔离 |
| **Pro** | **¥199/月** | 10万条记忆，无限项目 | 向量检索、语义搜索 |
| **Enterprise** | 定制报价 | 无限容量 | 私有部署、SLA保障、专属存储、审计日志 |

> ⏰ **公测时间**：2026年6月
> 🔗 **支付方式**：支付宝（微信：18923788188 王工）

---

## Core Workflow

```
Session Start → 1. inject_context() → get relevant history
Session Run  → 2. remember() / auto_capture() → save important info
Session End  → 3. summarize() → compress session into memory
```

## Scripts

### `scripts/memory_engine.py` — Core engine

```bash
# Save a memory
python3 scripts/memory_engine.py remember "决定: 使用FastAPI框架" --tags decision,tech --importance 8 --project saas

# Search memories
python3 scripts/memory_engine.py search "技术方案" --tags tech --min-imp 5

# Get context for prompt injection
python3 scripts/memory_engine.py inject "当前任务描述..."

# Auto-capture from text (scans for decisions, facts, preferences)
python3 scripts/memory_engine.py auto "我们决定采用SQLite作为数据库，技术栈为FastAPI..."

# Session management
python3 scripts/memory_engine.py session-start    # returns session_id + context
python3 scripts/memory_engine.py session-end <session_id> --summary "..."

# Stats
python3 scripts/memory_engine.py stats
```

### `scripts/setup.py` — One-time workspace setup

```bash
python3 scripts/setup.py
```

## Memory Structure

- **Storage**: SQLite + FTS5 full-text search
- **Fields**: content, tags[], importance(1-10), source, session, project, timestamps
- **Tags**: Tag memories for filtering (e.g., `decision`, `tech`, `user`, `project:X`)
- **Importance**: 1-10 scale. 8+ = key fact, 6-7 = useful context, 1-5 = normal

## Auto-Capture

The engine automatically detects important content from text:

| Trigger Keywords | Tag | Default Importance |
|:---|---|:---:|
| 决定, 选择, 采用, 改为, 升级, 弃用 | `decision` | 7 |
| 项目名, 产品名, 公司, 版本, 价格 | `fact` | 6 |
| 喜欢, 偏好, 习惯, 不要, 推荐 | `preference` | 6 |
| 技术栈, 框架, 语言, 数据库, API, 部署 | `tech` | 5 |
| 问题, bug, 报错, 异常, 失败 | `problem` | 5 |

## AGENTS.md Integration

Add to your `AGENTS.md` (or the relevant agent's config):

```markdown
## Long-Term Memory Rules

1. On session start: Run `python3 scripts/memory_engine.py inject "current task"` and use the output as context
2. When user shares important info: Use `remember()` to save it
3. Track decisions: Save key decisions with `--importance 8` and tag `decision`
4. Before answering "remember" or "previous" questions: Search memory first
5. On session end: Summarize key outcomes for next session
```

## Data Storage

```
~/.openclaw/workspace/long-term-memory/
├── memory.db          # SQLite database
├── config.json        # Configuration
└── current_context.md # Last built context (for debugging)
```

## Tips

- **Be selective**: Not everything needs remembering. Save decisions, preferences, problems.
- **Use tags**: `project:X` tags make cross-project memory searchable.
- **Importance matters**: 8+ for permanent facts, 5-7 for useful context, 3-4 for temporary.
- **Search before answering**: If user asks "do you remember X?", search memory first.
