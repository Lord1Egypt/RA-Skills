# Kinema's Task Management | Kinema 个人任务追踪系统

AI Agent 维护的个人任务追踪系统，基于 Markdown 文件持久化存储，支持每日报告和自动归档。

## 功能

- 自然语言创建任务 — 描述任务，AI 补全后结构化存储
- 状态管理 — Pending / In Progress / Done / Snoozed / Cancelled
- 每日早报 — 自动推送任务变动 diff + 当日状况
- 每日快照 — 自动生成任务快照，支持变更追溯
- 自动归档 — 完成和取消的任务自动归档
- 主动询问 — Agent 检测到任务完成时主动确认

## 适用场景

- 日常任务追踪与管理
- 多项目并行任务协调
- 任务状态变更追溯

## 使用方式

本 skill 支持 Codex、Claude Code 和 OpenClaw，安装后可通过对话触发：

```
帮我建一个任务：完成登录模块开发
TASK-00003 标记为 In Progress
/mytask
看看任务列表
任务报告
```

首次使用需完成 [references/ONBOARDING.md](references/ONBOARDING.md) 配置。Codex 手动任务管理不要求 OpenClaw cron；只有用户明确要求定时报告时才配置 Codex Automation。

## Codex 安装

```powershell
codex plugin marketplace add https://github.com/KinemaClawWorkspace/kinema-skills-marketplace.git
codex plugin add kinema-task-management@kinema-skills-marketplace
```

安装后新开一个 Codex 对话。Codex 默认把任务保存在 `%USERPROFILE%\.codex\kinema-tasks`。

## 目录结构

```
kinema-tasks/
├── active/      # 活跃任务
├── archived/    # 归档任务
└── snapshots/   # 每日快照
```

## 作者

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可证

[GNU General Public License v3.0](LICENSE)
