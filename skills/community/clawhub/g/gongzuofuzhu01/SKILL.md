---
name: personal-assistant
description: >
  个人工作任务管理助手。使用场景：记录待办事项、查看今日任务、更新任务进展、
  管理周期性任务、同步 OKR、生成工作月报/半年报。触发关键词：任务、待办、
  提醒、进展、OKR、月报、周报、报告。显式触发命令：ZHULI#。
version: 1.0.0
author: alan_huang
license: MIT
platforms: [linux]
prerequisites:
  env_vars: []
  commands: [python3, sqlite3]
metadata:
  hermes:
    tags: [Productivity, Task Management, OKR, Report, Reminder, Personal]
    slug: personal-assistant
    cron_jobs:
      - name: pa-morning-reminder
        schedule: "0 9 * * 1-5"
        description: 工作日上午提醒
      - name: pa-afternoon-reminder
        schedule: "0 14 * * 1-5"
        description: 工作日下午提醒
      - name: pa-evening-reminder
        schedule: "0 20 * * *"
        description: 每日晚间提醒
      - name: pa-recurring-sync
        schedule: "0 1 * * *"
        description: 每日生成周期任务实例
      - name: pa-okr-sync
        schedule: "0 10 * * 1"
        description: 每周一同步 OKR
---

# Personal Assistant — 个人工作任务管理

一站式管理你的工作任务、OKR、周期事项和进展汇报。

## 概述

Personal Assistant 是一个个人工作任务管理技能，通过 CLI 脚本 `scripts/personal_assistant.py` 操作本地 SQLite 数据库，支持任务的增删改查、进展跟踪、周期任务管理、OKR 同步和自动报告生成。

## 触发条件

当用户消息包含以下意图时自动加载本技能：

- 输入 `ZHULI#` 显式触发
- 记录/添加/创建任务或待办事项
- 查看今日/明天/本周任务列表
- 更新任务状态或进展
- 管理周期/定期/重复任务
- 同步或查看 OKR
- 生成工作月报/半年报/周报
- 手动触发任务提醒

## 快速开始

### 添加任务

在对话中自然描述即可，Agent 会自动调用本技能的 CLI 工具：

> "帮我记一下：周五前完成 Q2 述职 PPT，优先级高"
> "添加任务：修复登录 bug，明天中午前完成"

### 查看任务

> "今天有哪些待办？"
> "列出所有进行中的高优先级任务"

### 更新进展

> "任务 #42 进展更新为 60%，已完成数据收集"
> "把修复登录 bug 标记为完成"

### 生成报告

> "生成本月工作月报"
> "生成 2026 上半年工作报告"

## 定时提醒

技能注册了 5 个 cronjob，自动推送提醒和同步：

| 任务名称 | Cron 表达式 | 说明 |
|----------|-------------|------|
| `pa-morning-reminder` | `0 9 * * 1-5` | ☀️ 工作日上午 9:00 — 今日待办概览 |
| `pa-afternoon-reminder` | `0 14 * * 1-5` | 🌤️ 工作日下午 14:00 — 下午任务提醒 + 进度检查 |
| `pa-evening-reminder` | `0 20 * * *` | 🌙 每天 20:00 — 明日预告 + 今日完成总结 |
| `pa-recurring-sync` | `0 1 * * *` | 🔄 每天凌晨 1:00 — 自动生成周期任务实例 |
| `pa-okr-sync` | `0 10 * * 1` | 📊 每周一 10:00 — 从飞书文档同步 OKR |

提醒内容包含：任务列表（按优先级和截止时间排序）、OKR 关联进展、个性化的日程安排建议。

## 可用工具

本技能的核心 CLI 入口为 `scripts/personal_assistant.py`，子命令如下：

| 命令 | 说明 |
|------|------|
| `task add` | 添加新任务（使用 `--parent-id` 可创建子任务） |
| `task list` | 列表查询（支持按状态、分类、优先级过滤） |
| `task today` | 查看今日待办 |
| `task show <id>` | 查看任务详情 |
| `task update <id>` | 更新任务字段 |
| `task done <id>` | 完成任务 |
| `task delete <id>` | 删除任务 |
| `task search <keyword>` | 搜索任务 |
| `progress log <id>` | 记录任务进展 |
| `progress history <id>` | 查看进展历史 |
| `progress milestone-add <id>` | 添加里程碑 |
| `progress milestone-done <id>` | 完成里程碑 |
| `progress milestone-list <id>` | 列出里程碑 |
| `progress timeline` | 查看进展时间线 |
| `recurring add` | 添加周期任务 |
| `recurring list` | 列出周期任务 |
| `recurring generate` | 手动生成周期任务实例 |
| `recurring toggle <id>` | 暂停/恢复周期任务 |
| `recurring delete <id>` | 删除周期任务 |
| `okr add-objective` | 添加 Objective |
| `okr add-kr` | 添加 Key Result |
| `okr list` | 查看 OKR 列表 |
| `okr show <id>` | 查看 OKR 详情及关联任务 |
| `okr tree` | 查看 OKR 全景树 |
| `okr link` | 关联任务到 OKR |
| `okr sync` | 从飞书文档同步 OKR |
| `remind trigger` | 手动触发提醒 |
| `remind preview` | 预览待提醒任务（dry-run） |
| `remind history` | 查看提醒历史 |
| `report monthly` | 生成月度报告 |
| `report semiannual` | 生成半年度报告 |
| `advice` | 生成 LLM 智能建议上下文 |
| `db stats` | 查看数据库统计信息 |
| `db export` | 数据导出（JSON） |
| `db import` | 数据导入 |
| `db cleanup` | 清理历史数据 |

详细用法参见 `references/commands.md`。

## 数据存储

所有数据存储在 **`~/.hermes/data/personal_assistant/tasks.db`**（SQLite），包含 6 张表：

| 表名 | 用途 |
|------|------|
| `tasks` | 核心任务表（标题、状态、优先级、截止时间、进展等） |
| `milestones` | 任务里程碑 |
| `progress_logs` | 进展日志 |
| `recurring_tasks` | 周期任务模板 |
| `okr_items` | OKR 本地缓存 |
| `reminder_log` | 提醒推送记录（去重） |

数据库支持 WAL 模式、自动迁移和 JSON 导出备份。数据模型详见 `references/schema.md`。

## 配置

```bash
# 自定义数据库路径（默认：~/.hermes/data/personal_assistant/tasks.db）
export PA_DB_PATH=~/.hermes/data/personal_assistant/tasks.db

# 提醒时段（覆盖默认值）
export PA_MORNING_TIME=9
export PA_AFTERNOON_TIME=14
export PA_EVENING_TIME=20

# OKR 飞书文档 token
export PA_OKR_DOC_TOKEN=YOUR_DOC_TOKEN_HERE

# 报告输出目录（默认：~/.hermes/reports/）
export PA_REPORT_DIR=~/.hermes/reports/
```

## 注意事项

- 所有时间使用 **北京时间 (UTC+8)**
- 任务删除默认为**软删除**（status → 'cancelled'），使用 `--hard` 可物理删除
- OKR 同步依赖飞书文档可读，需确保 bot 有文档访问权限；同步失败时保留最近一次成功缓存
- 报告默认输出到 `~/.hermes/reports/` 目录
- 数据库文件自动创建，无需手动初始化
- 并发写入通过 SQLite WAL 模式 + 自动重试（最多 3 次）保障

## 常见问题

### 提醒没有推送？

1. 检查 `pa-morning-reminder` 等 cronjob 是否已注册：`cronjob(action='list')`
2. 检查 `reminder_log` 表确认是否触发过提醒
3. 手动测试：`python3 scripts/personal_assistant.py remind trigger --type morning`

### 周期任务没有自动生成实例？

- `pa-recurring-sync` cronjob 每天凌晨 1:00 运行
- 手动触发：`python3 scripts/personal_assistant.py recurring list` 查看待生成的周期任务
- 检查 `recurring_tasks.enabled` 是否为 1

### OKR 同步失败？

- 确认 `PA_OKR_DOC_TOKEN` 环境变量已设置
- 确认飞书 bot 对目标文档有读取权限
- 查看错误日志：`~/.hermes/logs/agent.log`

## 验证检查清单

- [ ] `~/.hermes/data/personal_assistant/tasks.db` 数据库已创建
- [ ] `python3 scripts/personal_assistant.py task add --title "测试任务"` 可成功添加
- [ ] `python3 scripts/personal_assistant.py task list` 可列出任务
- [ ] `python3 scripts/personal_assistant.py remind preview --type morning` 可预览提醒
- [ ] cronjob 已通过 `cronjob(action='create', ...)` 注册
- [ ] `python3 scripts/personal_assistant.py db stats` 统计信息正常
