---
name: inspirai-project
description: "多 Agent 项目管理 - 从想法到立项，自动在 Discord 频道创建项目 Thread 并分配 Agent 任务。支持快速讨论路由、批量立项、项目状态追踪。Triggers: '立项', '创建项目', '新项目', '讨论一下', '项目状态', 'create project', 'discuss', 'project status'"
homepage: https://github.com/inspirai-store/skill-market
metadata: {"openclaw":{"emoji":"📂"}}
---

# Project - 多 Agent 项目管理

从想法到立项的完整工作流，基于 Discord 多频道 + Thread 实现项目隔离。

## 子命令

| 命令 | 说明 |
|------|------|
| `/project:init <项目名>` | 立项：智能分配 Agent，批量创建 Discord Thread，下发初始任务 |
| `/project:discuss <话题>` | 快速讨论：把想法路由到最合适的 Agent 频道 |
| `/project:status [项目名]` | 项目状态：查看活跃项目和各 Thread 最新进展 |

## 工作流

```
想法 → /project:discuss → 讨论评估 → /project:init → 正式立项 → /project:status → 跟进
```

## 前置条件

- OpenClaw 已配置 Discord channel（多 agent + bindings）
- `~/.openclaw/openclaw.json` 中包含 Discord 配置
- 辅助脚本: `{SKILL_DIR}/discord-threads.py`
