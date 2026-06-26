---
name: openclaw-cursor-agent
description: Manage long-running Cursor CLI coding tasks through OpenClaw tools backed by tmux sessions. Use when the user asks to start a persistent coding job, inspect task status, send follow-up instructions, stop a running Cursor session, or mentions Cursor 后台任务, /cursor, tmux, spawn, check-status, send-command, or kill-session.
---

# OpenClaw Cursor Agent

让 OpenClaw 把长时间编码任务交给 Cursor CLI 在 tmux 里持久运行。

## 架构

```text
用户（飞书/聊天） → OpenClaw Agent → 插件 → WSL → tmux → Cursor CLI Agent
```

## 可用工具

| 工具 | 说明 |
|------|------|
| `cursor_agent_spawn_task` | 启动后台 Cursor 编码任务 |
| `cursor_agent_list_tasks` | 列出所有任务 |
| `cursor_agent_check_status` | 查询任务状态和进度 |
| `cursor_agent_send_command` | 向任务发送补充指令 |
| `cursor_agent_kill_session` | 结束任务 |
| `cursor_agent_doctor` | 诊断环境和依赖 |

## 工作流程

1. 环境不确定时先 `cursor_agent_doctor` 检查
2. `cursor_agent_spawn_task` 启动后台任务
3. `cursor_agent_check_status` 或 `cursor_agent_list_tasks` 监控进度
4. `cursor_agent_send_command` 发送补充指令（`/pause`、`/resume`、`/status`、或自然语言）
5. `cursor_agent_kill_session` 结束任务

## 自然语言映射

| 用户说 | 调用工具 |
|--------|----------|
| 帮我用 Cursor 在后台做一个任务：… | `cursor_agent_spawn_task` |
| 看看刚才那个任务做到哪了 | `cursor_agent_check_status` |
| 告诉刚才那个任务：改成 RS256 | `cursor_agent_send_command` |
| 把刚才那个 Cursor 任务停掉 | `cursor_agent_kill_session` |
| 列出所有后台任务 | `cursor_agent_list_tasks` |
| 检查 Cursor 环境是否正常 | `cursor_agent_doctor` |

## 输出规范

- spawn 后告知会话名和任务 ID
- 查状态时报告当前步骤、进度百分比、tmux 是否存活
- 环境缺依赖时明确指出缺少什么（tmux / python3 / agent / WSL）

## 参考文件

- [插件入口](extensions/openclaw-cursor-agent/index.js) — 工具注册和执行逻辑
- [工具脚本](cursor-agent-system/scripts/) — spawn / check-status / send / kill / attach
- [使用指南](docs/usage-guide.md) — 用户自然语言操作说明
- [配置示例](extensions/openclaw-cursor-agent/examples/) — openclaw.json 配置参考
