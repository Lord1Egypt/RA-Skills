---
name: todoist
description: "Todoist task management for OpenClaw. Unified todo API with multi-agent identity, scheduled checks and reminders."
metadata:
  openclaw:
    emoji: "✅"
    requires: {}
---

# Todoist Skill

为 OpenClaw 提供统一的待办管理能力，支持多 Agent 身份识别。

## 🎯 触发场景

当用户说以下内容时，**必须使用 Todoist** 而非系统提醒：
- "定一个任务"、"添加任务"、"创建任务"
- "提醒我"、"到时候提醒"、"别忘了"
- "待办"、"记下来"
- 任何涉及时间+事项的安排

**原因：** Todoist 有状态追踪、同步、自动提醒，比系统提醒更适合任务管理。

## 🎯 核心功能

1. **多 Agent 身份** - 每个 Agent 有独立任务标签，区分个人业务和 Agent 业务
2. **智能提醒** - 只提醒个人任务，Agent 内部计划不骚扰用户
3. **自动同步** - 心跳时自动同步到 TASK.md，省 Token
4. **保留手动内容** - TASK.md 中手动添加的内容不会被覆盖

## 身份系统

每个 OpenClaw 实例有唯一 ID，每个 Agent 有独立标签：

```
实例 ID: 8259c9d1 (自动生成)
Agent 标签: agent-8259c9d1-main
```

## 命令

| 命令 | 说明 |
|------|------|
| `list [filter]` | 列出任务 (today/personal/agent/overdue) |
| `add <内容> [type] [日期]` | 添加任务 (type: personal/agent) |
| `subtask <父任务> <内容>` | 添加子任务 |
| `show <关键词>` | 查看任务详情 |
| `update <任务> <字段> <值>` | 更新任务 |
| `claim <任务>` | 认领任务 |
| `complete <任务>` | 完成任务 |
| `delete <任务>` | 删除任务 |
| `projects` | 列出项目 |
| `labels` | 列出标签 |

## 🔄 自动同步到 TASK.md

心跳时自动执行：

```bash
~/.openclaw/workspace/skills/openclaw-todoist/scripts/sync-to-task.sh
```

### 任务分类与提醒

| 任务类型 | 存储位置 | 是否提醒用户 |
|---------|---------|-------------|
| 📋 个人任务 | "个人事务" 项目 | ✅ 提醒 |
| 🤖 Agent 任务 | "Agent 任务" 项目 或 带 agent 标签 | ❌ 不提醒 |

**设计原则：**
- 用户关心的是"下午买咖啡" → 提醒
- Agent 的内部计划"实现认证模块" → 不提醒用户，仅记录

### 生成的 TASK.md 格式

```markdown
# 当前任务

_自动同步自 Todoist (2026-03-16 10:00)_

## 🔴 个人逾期任务 (1)
- [ ] 任务名 (逾期: 2026-03-15)

## 📅 个人今日任务 (2)
- [ ] 下午买一杯咖啡
- [ ] 回电话给老王

---

## 🤖 Agent 内部任务 (main)
_这些是 Agent 的计划任务，不会提醒用户_

### 今日
- [ ] 实现用户认证模块
```

### 保留手动内容

在 TASK.md 中添加 `<!-- MANUAL:START -->` 和 `<!-- MANUAL:END -->` 标记，中间的内容不会被覆盖：

```markdown
<!-- MANUAL:START -->
## 📝 临时记录

- [ ] 记得回电话给老王
- [x] 已完成的事情
<!-- MANUAL:END -->
```

### 提醒逻辑

| 情况 | 行为 |
|------|------|
| 🔴 个人逾期任务 | 提醒用户 |
| 📅 个人今日任务 | 提醒用户（临期！） |
| 📆 明日任务 | 仅显示，不提醒 |
| 📌 无日期任务 | 仅显示，不提醒 |
| 🤖 Agent 任务 | 仅显示，**不提醒** |

**核心原则：** 临期提醒才有意义，过期提醒为时已晚

### ⚡ 省 Token 机制

脚本检测**状态变化**，只有以下情况才输出：
- 新增/删除个人紧急任务
- 个人任务状态变化

状态不变时静默，不消耗 Token！

## 配置

| 命令 | 说明 |
|------|------|
| `config` | 显示配置 |
| `set-time HH:MM` | 设置每日提醒时间 |
| `set-interval N` | 设置心跳检查间隔(小时) |

## 心跳配置

在 `HEARTBEAT.md` 中添加：

```markdown
# 心跳任务

## 每次心跳自动执行

```bash
~/.openclaw/workspace/skills/openclaw-todoist/scripts/sync-to-task.sh
```

## 静默条件
- 无个人紧急任务 → HEARTBEAT_OK
- 状态不变 → HEARTBEAT_OK
```

## 发布内容

```
skills/openclaw-todoist/
├── SKILL.md
├── todoist.sh
└── scripts/
    ├── sync-to-task.sh
    └── setup-heartbeat.sh
```

## 用户配置文件（不包含在发布中）

```
~/.openclaw/workspace/
├── .todoist-token          # 用户 API token
└── .agent-identity.json    # 用户身份配置
```