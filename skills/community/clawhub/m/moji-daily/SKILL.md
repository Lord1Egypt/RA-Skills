---
name: moji-daily
description: 墨记 — 每日任务追踪系统。通过聊天对话自动管理每日待办事项的创建、更新、跟进、总结和滚动。适用场景：(1) 每日09:00 cron触发早间Review，询问用户当天任务并写入 tasks/YYYY-MM-DD.md；(2) 每日12:00 cron触发午间跟进，检查进度；(3) 每日18:00 cron触发晚间总结，汇总完成情况并滚动未完成项到次日；(4) 用户随时在聊天中报告任务完成、添加新任务、修改或取消任务时，自动更新任务文件。适合需要精细记录每日工作的管理者、创业者、咨询顾问，数据以本地Markdown文件存储，零服务器依赖，可轻松复制迁移。
---

# 墨记 (moji-daily)

## 概述

墨记是一个完全基于聊天对话的每日任务追踪系统。用户不需要打开任何网页——早间安排任务、午间汇报进度、晚间确认总结，全部在聊天中完成。数据存储为本地文件，零服务器运维，复制文件夹即可迁移。

## 架构

```
daily-task-tracker/
├── assets/daily-template.md   ← 每日任务文件模板
├── references/workflow.md     ← 详细工作流（Cron场景 + 用户交互场景）
└── scripts/setup-crons.sh     ← 生成Cron配置JSON
```

任务文件存储在 `tasks/YYYY-MM-DD.md`，每天独立文件。

## 快速开始

### 1. 添加 Cron 配置

运行 setup-crons.sh 获取三个 Cron 的 JSON 配置，添加到 openclaw.json 的 `"crons"` 数组中：

```bash
bash daily-task-tracker/scripts/setup-crons.sh
```

三个 Cron 分别为：
- 🕘 **09:00 早间 Review** — 问用户今天的任务
- 🕛 **12:00 午间跟进** — 检查进度
- 🕕 **18:00 晚间总结** — 汇总并滚动到次日

### 2. 创建任务目录

```bash
mkdir -p tasks
```

### 3. 开始使用

系统自动运行。用户也可以在聊天中随时汇报：
- "XXX做完了"
- "加一个任务XXX"
- "取消XXX"
- "XXX改到明天"

## 核心工作流

详见 `references/workflow.md`，涵盖 4 种场景：

| 场景 | 触发方式 | 目标 |
|------|---------|------|
| 早间Review | 09:00 Cron | 创建/更新当天任务清单 |
| 午间跟进 | 12:00 Cron | 检查进度，适时提醒 |
| 晚间总结 | 18:00 Cron | 汇总完成，滚动未完成项 |
| 用户主动交互 | 聊天消息 | 实时更新任务状态 |

## 命名规范


- **文件命名**：`tasks/YYYY-MM-DD.md`
- **状态标识**：`- [ ]` 待办 → `- [x]` 已完成

## 迁移指南

把 `daily-task-tracker/` 文件夹整体复制到新环境的 `.openclaw/skills/` 目录即可。
复制后添加 cron 配置、创建 `tasks/` 目录，即刻可用。
