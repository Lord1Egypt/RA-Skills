---
name: obsidian-inbox-pipeline
description: >
  将任意来源（AI 资讯、经济雷达、旅游日报、RSS、文章）自动采集、
  结构化写入 Obsidian inbox 的完整流水线。支持 Telegram / 飞书推送
  和 cron 定时执行。一套配置，永久自动沉淀知识。
---

# Obsidian Inbox Pipeline

打通外部信息源与 Obsidian 知识库的自动化流水线。安装后配置好环境变量，即可持续将资讯日报、文章、帖子等结构化沉淀到 Obsidian，无需手动整理。

## 核心脚本

| 脚本 | 功能 | 关键参数 |
|------|------|---------|
| `capture.py` | 写入单条笔记到 inbox | `--type`, `--title`, `--source`, `--tags`, `--content` |
| `query.py` | 搜索知识库（index + 正文） | `--query`, `--type`, `--tags`, `--limit` |
| `review.py` | 生成 inbox 整理报告 | `--dry-run`（预览） |
| `scripts/daily_pipeline.sh` | 三合一流水线参考 | radar 类型、名称、分类、来源 |

## 快速开始

### 1. 安装依赖

```bash
# 克隆 skill 到本地
clawhub install obsidian-inbox-pipeline

# 复制环境变量模板
cp references/.env.example .env
# 编辑 .env，填入真实路径和凭证
```

### 2. 配置环境变量

```bash
# .env 文件示例
OBSIDIAN_VAULT_PATH=/Users/you/obsidian/MyKnowledge
OBSIDIAN_INBOX_DIR=inbox
TELEGRAM_BOT_TOKEN=123456:ABC-xxx
TELEGRAM_CHAT_ID=987654321
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
```

> ⚠️ **安全提醒**：`.env` 文件请加入 `.gitignore`，不要提交到公开仓库。脚本从不硬编码任何凭证。

### 3. 写入一条笔记（测试）

```bash
export OBSIDIAN_VAULT_PATH=/path/to/vault

python3 capture.py \
  --type capture \
  --title "测试笔记" \
  --source "手动测试" \
  --tags "[测试]" \
  --content "这是正文内容，可以是任何文本..."
```

### 4. 搜索知识库

```bash
export OBSIDIAN_VAULT_PATH=/path/to/vault

# 搜索标题和摘要
python3 query.py --query "OpenClaw" --limit 5

# 只看 knowledge 类型
python3 query.py --query "AI Agent" --type knowledge --limit 5

# 搜索正文内容（需要 obsidian-cli）
python3 query.py --query "OpenClaw" --include-content
```

### 5. 生成 Inbox 整理报告

```bash
export OBSIDIAN_VAULT_PATH=/path/to/vault

# 预览（不写文件）
python3 review.py --dry-run

# 正式生成（写入 notes/_review/inbox-review-YYYY-MM-DD.md）
python3 review.py
```

### 6. 定时自动运行（cron）

```bash
# 每天 7:00 自动跑（来源和 cron 触发自行配置）
0 7 * * * cd /path/to/skill && \
  OBSIDIAN_VAULT_PATH=/path/to/vault \
  TELEGRAM_BOT_TOKEN=xxx \
  TELEGRAM_CHAT_ID=xxx \
  bash scripts/daily_pipeline.sh "ai-radar" "AI 资讯雷达" "AI" "🤖" "AI 资讯" \
  >> /var/log/obsidian_pipeline.log 2>&1
```

## 流水线架构

```
外部来源（RSS / API / 爬虫 / 手动）
         │
         ▼
┌─────────────────────┐
│   生成原始 Markdown  │
│   (日报/文章/帖子)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│     capture.py      │◄── 写入 Obsidian inbox
│  (结构化模板写入)     │    （type / tags / source / TL;DR）
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  rebuild_index.mjs  │◄── 重建 .ai/index.json
│  (Obsidian 官方脚本)  │    （支持 query.py 搜索）
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  query.py / review  │◄── 知识库检索 / inbox 整理
│                     │
└─────────────────────┘

可选通知渠道（均走环境变量，不硬编码）：
  ├── Telegram Bot（需 TELEGRAM_BOT_TOKEN）
  └── 飞书自建应用（需 FEISHU_APP_ID / FEISHU_APP_SECRET）
```

## frontmatter 标准格式

写入的每条笔记使用统一 frontmatter，便于后续检索和分类：

```yaml
---
type: capture           # capture | daily-report | knowledge
created: 2026-03-21     # 自动时间戳
tags: [AI, 日报]        # 自定义标签
source: AI 资讯雷达     # 来源
status: inbox           # inbox → knowledge → _archive
---
```

## 配合 AI 雷达使用

配合 `ai-radar`、`economy-radar`、`travel-radar` 等 skill 使用时：

```bash
# 三合一每日自动运行（配合 cron）
0 7 * * * \
  source /path/to/.env && \
  bash /path/to/obsidian-inbox-pipeline/scripts/daily_pipeline.sh \
    "ai-radar" "AI 资讯雷达" "AI" "🤖" "AI 资讯" && \
  bash /path/to/obsidian-inbox-pipeline/scripts/daily_pipeline.sh \
    "economy-radar" "经济雷达" "经济" "📊" "经济资讯" && \
  bash /path/to/obsidian-inbox-pipeline/scripts/daily_pipeline.sh \
    "travel-radar" "旅游雷达" "旅游" "✈️" "旅游资讯"
```

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| `OBSIDIAN_VAULT_PATH` 报错 | 确保环境变量已设置，或安装 `obsidian-cli` |
| inbox 写入了但 query 搜不到 | 运行 `node /path/to/vault/scripts/rebuild_index.mjs` 重建索引 |
| Telegram 推送失败 | 确认 Bot Token 和 Chat ID 正确，Bot 已被用户发起过对话 |
| 飞书推送失败 | 检查 app_id / app_secret 权限（需要发消息权限） |

## 依赖

- Python ≥ 3.8
- `obsidian-cli`（可选，vault 路径自动发现）
- `node`（可选，索引重建脚本）
- Telegram Bot Token（可选，通知推送）
- 飞书自建应用凭证（可选，通知推送）
