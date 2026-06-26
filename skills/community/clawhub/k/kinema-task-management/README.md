# Kinema's Task Management | Kinema 个人任务追踪系统

> 该解法非常不优雅，尝试构建真正方便查看修改的解法。说到底 OpenClaw 本身不是完成 daily task 全功能的合适的渠道。

AI Agent 维护的个人任务追踪系统，基于 Markdown 文件持久化存储。

## 功能

- 📝 **自然语言创建任务** — 描述任务，AI 补全后结构化存储
- 🔄 **状态管理** — Pending / In Progress / Done / Snoozed / Cancelled
- 📊 **每日早报** — 自动推送任务变动 diff + 当日状况
- 📸 **每日快照** — 自动生成任务快照，支持变更追溯
- 🗂 **自动归档** — 完成和取消的任务自动归档

## 安装

```bash
clawhub install kinema-task-management
```

首次使用需完成 [ONBOARDING.md](ONBOARDING.md) 配置。

## 目录结构

```
kinema-tasks/
├── active/      # 活跃任务
├── archived/    # 归档任务
└── snapshots/   # 每日快照
```

## 作者

- [LeeShunEE](https://github.com/LeeShunEE)
- [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可

GPL v3
