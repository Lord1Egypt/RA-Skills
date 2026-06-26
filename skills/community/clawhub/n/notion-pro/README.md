<div align="center">

# 📝 Notion Pro — Complete Notion API Skill for OpenClaw

**The most comprehensive Notion API skill for AI agents.**  
Built-in Python CLI · Agent operation strategies · Auto-pagination · Recursive blocks · 429 retry

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org)
[![Notion API](https://img.shields.io/badge/Notion%20API-2025--09--03-black.svg)](https://developers.notion.com)
[![ClawHub](https://img.shields.io/badge/ClawHub-notion--pro-orange.svg)](https://clawhub.ai)

[English](#overview) · [中文](#中文说明)

</div>

---

## Overview

**Notion Pro** is a production-grade [OpenClaw](https://openclaw.ai) skill that gives AI agents complete control over Notion workspaces. Unlike basic Notion skills that only list API commands, this skill embeds the **operational knowledge** agents need to work with Notion effectively.

### Why Another Notion Skill?

We built this after watching agents fail at Notion tasks in predictable ways:
- Guessing page IDs instead of searching
- Missing nested content inside toggles and lists
- Hitting 429 rate limits and crashing
- Not knowing that "replace" means delete + append
- Sending 5000-character strings into a 2000-char field

**Notion Pro solves all of these** with a combination of smart tooling and embedded strategy.

### Feature Comparison

| Capability | Notion Pro | Built-in Skill | Other Skills |
|---|:---:|:---:|:---:|
| Agent strategy (5-step workflow) | ✅ | ❌ | ❌ |
| Recursive block fetch (`--recursive`) | ✅ | ❌ | ❌ |
| Auto-pagination (`--all`) | ✅ | ❌ | ❌ |
| 429 auto-retry (Retry-After) | ✅ | ❌ | ❌ |
| Positional insert (`--after`) | ✅ | ❌ | ❌ |
| Complete API limits reference | ✅ | Partial | Partial |
| 4 operation pattern SOPs | ✅ | ❌ | ❌ |
| Zero external dependencies | ✅ | N/A | Node.js |
| Bilingual docs (EN + CN) | ✅ | EN only | EN only |

## Quick Start

### Install via ClawHub (Recommended)

```bash
npx clawhub@latest install notion-pro
```

### Install Manually

```bash
# Clone to your OpenClaw skills directory
git clone https://github.com/baixiaodev/notion-pro-skill.git ~/.openclaw/skills/notion-pro
```

### Configure

1. Create a [Notion Integration](https://www.notion.so/profile/integrations) and copy the API key
2. Set up authentication (choose one):

```bash
# Option A: Environment variable
export NOTION_API_KEY="ntn_xxxxx"

# Option B: OpenClaw config (openclaw.json)
# Add to skills.entries:
#   "notion-pro": { "apiKey": "ntn_xxxxx" }
```

3. **Share your pages/databases** with the integration in Notion (click "..." → "Connect to" → your integration name)

### Verify

```bash
python3 ~/.openclaw/skills/notion-pro/scripts/notion_api.py search --query "test"
```

## What's Inside

```
notion-pro/
├── SKILL.md               # English skill doc (agent-facing)
├── SKILL_CN.md             # 中文技能文档
├── scripts/
│   └── notion_api.py       # Python CLI tool (422 lines, zero deps)
├── README.md               # This file
└── LICENSE                 # MIT
```

### The Python CLI Tool

A single-file Python 3 tool with **zero external dependencies** (stdlib `urllib` only). Supports 8 commands:

| Command | Description |
|---|---|
| `search` | Search pages and databases with auto-pagination |
| `get-page` | Get page metadata (properties, parent, URL) |
| `get-blocks` | Get page content with recursive block expansion |
| `query-database` | Query databases with filters, sorts, auto-pagination |
| `create-page` | Create pages in databases or as sub-pages |
| `update-page` | Update page properties |
| `append-blocks` | Append content blocks with positional insert |
| `delete-block` | Archive (soft-delete) a block |

**Key features:**
- 🔄 **429 auto-retry** — Reads `Retry-After` header, retries up to 3 times
- 📄 **Auto-pagination** (`--all`) — Fetches all results across multiple pages
- 🌳 **Recursive blocks** (`--recursive`) — Expands nested blocks up to 5 levels deep
- 📍 **Positional insert** (`--after`) — Insert blocks at specific positions
- 🔀 **API version compatibility** — Auto-falls back between `/data_sources/` and `/databases/` endpoints
- ⏱️ **Rate protection** — 350ms delays between paginated/recursive requests

### The Agent Strategy

The SKILL.md doesn't just list commands — it teaches agents **how to think** about Notion tasks:

```
1. Discover  → search for the target page/database ID
2. Inspect   → read current structure with get-page / get-blocks
3. Plan      → determine operation sequence
4. Execute   → batch operations (≤50 blocks), 300ms intervals
5. Verify    → confirm results with get-blocks
```

Plus 4 battle-tested operation patterns:
- **Bulk Knowledge Base Population** — Schema-first batch writes
- **Page Content Update** — Delete + append workflow
- **Recursive Full-Page Read** — Nested toggle/list expansion
- **Conditional Query + Bulk Update** — Filter, iterate, update

## Usage Examples

```bash
# Search for a page
python3 scripts/notion_api.py search --query "Meeting Notes" --filter page

# Read full page content (recursive)
python3 scripts/notion_api.py get-blocks --block-id "abc123" --recursive

# Query database with filter
python3 scripts/notion_api.py query-database \
  --database-id "def456" \
  --filter '{"property": "Status", "select": {"equals": "Active"}}' \
  --all

# Create a database entry
python3 scripts/notion_api.py create-page \
  --parent-id "def456" \
  --parent-type database \
  --properties '{"Name": {"title": [{"text": {"content": "New Item"}}]}, "Status": {"select": {"name": "Draft"}}}'

# Append content to a page
python3 scripts/notion_api.py append-blocks \
  --block-id "abc123" \
  --children '[{"object":"block","type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"Hello from the API!"}}]}}]'
```

## API Reference

See the full reference in [SKILL.md](SKILL.md) (English) or [SKILL_CN.md](SKILL_CN.md) (中文), including:

- Complete block type reference (15+ types with JSON examples)
- Rich text formatting (bold, italic, code, colors, links, mentions)
- Property type reference (14 types with write examples)
- API limits quick reference table
- API version 2025-09-03 migration notes

## Contributing

Issues and PRs are welcome! If you've found a Notion API edge case or have a useful operation pattern to share, please open an issue.

## License

[MIT](LICENSE)

---

<div align="center">

# 中文说明

</div>

## 概述

**Notion Pro** 是一个生产级 [OpenClaw](https://openclaw.ai) 技能，让 AI Agent 完整掌控 Notion 工作区。不同于仅列出 API 命令的基础技能，本技能内嵌了 Agent 高效操作 Notion 所需的 **操作策略知识**。

### 为什么需要另一个 Notion Skill？

我们在实际使用中观察到 Agent 在 Notion 任务上反复犯同样的错误：
- 猜测页面 ID 而不是先搜索
- 遗漏 toggle 和列表中的嵌套内容
- 触发 429 限速后直接崩溃
- 不知道"替换"实际上是 删除 + 追加
- 往 2000 字符的字段里塞 5000 字符

**Notion Pro 通过智能工具 + 内嵌策略解决了所有这些问题。**

## 快速开始

### 通过 ClawHub 安装（推荐）

```bash
npx clawhub@latest install notion-pro
```

### 手动安装

```bash
git clone https://github.com/baixiaodev/notion-pro-skill.git ~/.openclaw/skills/notion-pro
```

### 配置

1. 创建 [Notion Integration](https://www.notion.so/profile/integrations) 并复制 API Key
2. 设置认证（选其一）：
   - 环境变量：`export NOTION_API_KEY="ntn_xxxxx"`
   - OpenClaw 配置：在 `openclaw.json` 的 `skills.entries` 中添加 `"notion-pro": { "apiKey": "ntn_xxxxx" }`
3. 在 Notion 中将目标页面/数据库**共享给集成**（点击 "..." → "Connect to"）

### 验证

```bash
python3 ~/.openclaw/skills/notion-pro/scripts/notion_api.py search --query "测试"
```

## 核心特性

### Python CLI 工具

单文件 Python 3 工具，**零外部依赖**（仅用标准库 `urllib`），支持 8 个子命令：

| 命令 | 功能 |
|---|---|
| `search` | 搜索页面和数据库，支持自动翻页 |
| `get-page` | 获取页面元数据 |
| `get-blocks` | 获取页面内容，支持递归展开嵌套块 |
| `query-database` | 查询数据库，支持过滤、排序、自动翻页 |
| `create-page` | 在数据库或页面下创建新页面 |
| `update-page` | 更新页面属性 |
| `append-blocks` | 追加内容块，支持指定位置插入 |
| `delete-block` | 归档（软删除）块 |

### Agent 操作策略

SKILL.md 不只列出命令，它教会 Agent **如何思考** Notion 任务：

```
1. Discover  → 搜索目标页面/数据库 ID
2. Inspect   → 读取当前结构
3. Plan      → 确定操作序列
4. Execute   → 分批执行（≤50块），300ms间隔
5. Verify    → 验证结果
```

加上 4 种实战验证的操作模式：
- **知识库批量填充** — Schema-First 批量写入
- **页面内容更新** — 删除 + 追加工作流
- **递归完整页面读取** — 嵌套 toggle/list 展开
- **条件查询 + 批量更新** — 过滤、遍历、更新

## 完整文档

- 英文：[SKILL.md](SKILL.md)
- 中文：[SKILL_CN.md](SKILL_CN.md)

## 贡献

欢迎提 Issue 和 PR！如果你发现了 Notion API 的边界情况或有实用的操作模式，请开 Issue 分享。

## 许可证

[MIT](LICENSE)
