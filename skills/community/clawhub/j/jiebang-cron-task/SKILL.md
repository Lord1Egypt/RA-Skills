---
name: jiebang-cron-task
description: AI Agent定时任务管理工具 - 通过自然语言创建、查询、完成、删除定时任务，查看执行日志和使用预设模板。支持Cron表达式、失败重试、模板快捷创建。当用户提到定时任务、cron、提醒、打卡、盯盘、定时执行、周期任务、任务调度等需求时使用此技能。
---

# 捷帮定时任务

为AI Agent提供完整的定时任务管理能力：创建、查询、完成、删除定时任务，查看执行日志，使用预设模板快速创建常用任务。

**免费使用，自动注册，无需配置。**

## 核心能力

1. **创建定时任务** — 支持Cron表达式和自然语言时间描述，支持失败重试配置
2. **查询任务列表** — 查看所有任务或仅查看到期任务，按标签筛选
3. **完成/失败标记** — 标记任务执行结果，支持附加消息
4. **执行日志** — 查看任务执行历史，包括成功/失败状态和时间
5. **预设模板** — 12个常用模板：每日早报、每小时检查、工作日盯盘、每月报告等
6. **删除任务** — 不再需要的任务可以删除

## 工作流程

### 第一步：确保API Key可用

运行 `python3 main.py ensure-key` 自动注册获取API Key。Key会保存到本地文件，后续调用自动读取。

**只需执行一次**，除非Key丢失才需要重新注册。

### 第二步：根据用户需求执行操作

| 用户意图 | 执行命令 |
|---------|---------|
| 创建定时任务 | `python3 main.py create --name "任务名" --cron "0 9 * * *" [--retries 3] [--tags "daily,report"]` |
| 查看所有任务 | `python3 main.py list` |
| 只看到期任务 | `python3 main.py list --due` |
| 按标签筛选 | `python3 main.py list --tag "stock"` |
| 标记完成 | `python3 main.py done <task_id> [--status success] [--msg "执行成功"]` |
| 标记失败 | `python3 main.py done <task_id> --status failed --msg "API超时"` |
| 查看执行日志 | `python3 main.py logs [--task-id <id>] [--limit 20]` |
| 查看预设模板 | `python3 main.py templates` |
| 用模板创建 | `python3 main.py create --template "daily-morning" --name "每日早报"` |
| 删除任务 | `python3 main.py delete <task_id>` |

### Cron表达式说明

格式：`分 时 日 月 周`

常用示例：
- `0 9 * * *` — 每天9点
- `0 9,22 * * 1-5` — 工作日9点和22点
- `*/30 * * * *` — 每30分钟
- `0 0 1 * *` — 每月1号零点
- `0 9 * * 1` — 每周一9点

### 预设模板列表

| 模板ID | 名称 | Cron | 说明 |
|--------|------|------|------|
| daily-morning | 每日早报 | 0 9 * * * | 每天早上9点 |
| daily-evening | 每日晚报 | 0 18 * * * | 每天下午6点 |
| hourly | 每小时检查 | 0 * * * * | 每小时整点 |
| every-30min | 每30分钟 | */30 * * * * | 每30分钟 |
| weekday-morning | 工作日早报 | 0 9 * * 1-5 | 工作日9点 |
| weekday-evening | 工作日晚报 | 0 18 * * 1-5 | 工作日18点 |
| weekly | 每周报告 | 0 9 * * 1 | 每周一9点 |
| monthly | 每月报告 | 0 9 1 * * | 每月1号9点 |
| stock-open | 开盘提醒 | 30 9 * * 1-5 | 工作日9:30 |
| stock-close | 收盘提醒 | 0 15 * * 1-5 | 工作日15:00 |
| stock-morning | 盘前分析 | 0 8 * * 1-5 | 工作日8点 |
| stock-evening | 盘后复盘 | 0 22 * * 1-5 | 工作日22点 |

## 输出格式

所有命令输出JSON格式，包含status和data/result字段。错误时返回error字段。

## 边界情况

- 首次使用必须先运行 `ensure-key` 注册API Key
- 免费版限制：10次/分钟，100次/天
- Cron表达式必须是5段格式（分 时 日 月 周）
- 任务ID是字符串，在完成/删除时需要精确传入
- 同一agent_id下的任务名称可以重复，用task_id区分

## 使用示例

```
输入: "帮我设个每天早上9点的定时任务"
执行: python3 main.py create --name "每日任务" --cron "0 9 * * *"

输入: "看看我有哪些到期的任务"
执行: python3 main.py list --due

输入: "用盯盘模板创建一个任务"
执行: python3 main.py create --template "stock-open" --name "开盘提醒"

输入: "任务abc123完成了"
执行: python3 main.py done "abc123" --status success
```
