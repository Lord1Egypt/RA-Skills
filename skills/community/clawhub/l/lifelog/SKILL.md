---
name: lifelog
description: |
  生活记录自动化系统。自动识别消息中的日期（今天/昨天/前天/具体日期），使用 SubAgent 智能判断，记录到 Notion 对应日期，每次都是**追加记录**而非覆盖。
  适用于：(1) 用户分享日常生活点滴时自动记录；(2) 定时自动汇总分析并填充情绪、事件、位置、人员字段
version: 1.2.4
credentials:
  required:
    - NOTION_KEY
    - NOTION_DATABASE_ID
---

# LifeLog 生活记录系统

自动将用户的日常生活记录到 Notion，支持智能日期识别和自动汇总分析。

## ⚠️ 必需凭据

使用本技能前，必须设置以下环境变量：

```bash
export NOTION_KEY="your-notion-integration-token"
export NOTION_DATABASE_ID="your-notion-database-id"
```

获取方式：
1. 访问 https://www.notion.so/my-integrations 创建 Integration
2. 获取 Internal Integration Token
3. 创建 Database 并 Share 给 Integration
4. 从 URL 中提取 Database ID

# LifeLog 生活记录系统

自动将用户的日常生活记录到 Notion，支持智能日期识别和自动汇总分析。

## 核心功能

1. **实时记录** - 用户分享生活点滴时自动记录到 Notion
2. **智能日期识别（SubAgent）** - 使用 AI SubAgent 智能判断日期，优先分析文本中的日期关键词，其次分析上下文
3. **追加记录** - 每次都是追加到 Notion 指定日期的记录中，**绝不覆盖**
4. **自动汇总** - 每天凌晨自动运行 LLM 分析，生成情绪状态、主要事件、位置、人员

## Notion 数据库要求

创建 Notion Database，需包含以下字段（全部为 rich_text 类型）：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 日期 | title | 日期，如 2026-02-22 |
| 原文 | rich_text | 原始记录内容 |
| 情绪状态 | rich_text | LLM 分析后的情绪描述 |
| 主要事件 | rich_text | LLM 分析后的事件描述 |
| 位置 | rich_text | 地点列表 |
| 人员 | rich_text | 涉及的人员 |

## 记录流程

### 每条消息的处理步骤

1. 用户发送生活记录消息
2. **立即调用 SubAgent 判断日期** - 分析消息中的日期关键词（今天/昨天/前天/具体日期）和上下文，输出判断的日期（YYYY-MM-DD）
3. 调用 `lifelog-append.sh "消息内容" "判断的日期"` → 追加到 Notion 指定日期
4. 如果指定日期已有记录，则**追加**内容到该日期的原文字段中

### SubAgent 日期判断 Prompt

```
分析以下用户消息，判断它描述的是哪个日期的生活记录。

消息内容：「用户消息原文」

请输出：
1. 判断的日期（格式：YYYY-MM-DD）
2. 判断依据（简单说明）

只输出这两项，不要多余内容。
```

### 脚本用法

```bash
# 追加记录到指定日期（SubAgent 判断日期后调用）
bash lifelog-append.sh "消息内容" "YYYY-MM-DD"
```

> 注意：脚本第二个参数为日期，不传则默认为今天。每条记录都是**追加**而非覆盖。

### 2. lifelog-daily-summary-v5.sh

拉取指定日期的原文，用于 LLM 分析：

```bash
# 拉取昨天
bash lifelog-daily-summary-v5.sh

# 拉取指定日期
bash lifelog-daily-summary-v5.sh 2026-02-22
```

输出格式：
```
PAGE_ID=xxx
---原文开始---
原文内容
---原文结束---
```

### 3. lifelog-update.sh

将 LLM 分析结果写回 Notion：

```bash
bash lifelog-update.sh "<page_id>" "<情绪状态>" "<主要事件>" "<位置>" "<人员>"
```

## 配置步骤

1. 创建 Notion Integration 并获取 API Key
2. 创建 Database 并共享给 Integration
3. 获取 Database ID（URL 中提取）
4. 设置环境变量：

```bash
export NOTION_KEY="your-notion-integration-token"
export NOTION_DATABASE_ID="your-database-id"
```

## 定时任务（可选）

每天凌晨 5 点自动汇总昨天数据：

```bash
openclaw cron add \
  --name "LifeLog-每日汇总" \
  --cron "0 5 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "运行 LifeLog 每日汇总" \
  --delivery-mode announce \
  --channel qqbot \
  --to "<用户ID>"
```

## 工作流

1. 用户发送生活记录 → 调用 SubAgent 判断日期 → 调用 `lifelog-append.sh` → **追加**到 Notion
2. 定时任务触发 → 调用 `lifelog-daily-summary-v5.sh` → 拉取原文
3. LLM 分析原文 → 调用 `lifelog-update.sh` → 填充分析字段
