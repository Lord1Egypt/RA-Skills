---
name: openclaw-knowledge
description: OpenClaw 文档知识库 - 搜索与同步 / OpenClaw Documentation Knowledge Base - Search & Sync
metadata:
  {
    "openclaw": {
      "emoji": "📚",
      "os": ["darwin", "linux", "win32"]
    }
  }
---

# OpenClaw 文档知识库 / OpenClaw Knowledge Base

本技能提供 OpenClaw 官方文档的搜索与同步功能。
/ This skill provides search and sync capabilities for OpenClaw official documentation.

## 功能概览 / Features

- **全文搜索** - 快速搜索 366+ 文档 / Full-text search across 366+ documents
- **增量同步** - 从官网获取最新文档 / Incremental sync from official docs
- **分类浏览** - 按类别查看文档 / Browse by category
- **JSON 输出** - 支持 AI 调用 / AI-friendly JSON output

## 命令 / Commands

### 搜索 / Search

```bash
# 基本搜索 / Basic search
node scripts/search.js "memory"

# 分类过滤 / Category filter
node scripts/search.js "docker" --category install

# JSON 输出（供 AI 调用）/ JSON output (for AI)
node scripts/search.js "session" --format json --limit 5

# 列出所有分类 / List all categories
node scripts/search.js --categories

# 查看帮助 / Show help
node scripts/search.js --help
```

### 同步 / Sync

```bash
# 查看同步统计 / Show sync stats
node scripts/sync.js --stats

# 增量同步（5并发）/ Incremental sync (5 concurrent)
node scripts/sync.js

# 强制全量更新 / Force full refresh
node scripts/sync.js --force

# 自定义并发数 / Custom parallel
node scripts/sync.js --parallel=10 --delay=50
```

## 分类 / Categories

| 分类 | 说明 |
|------|------|
| automation | 自动化任务（定时任务、钩子） |
| channels | 消息渠道（Telegram、Discord 等） |
| cli | 命令行工具参考 |
| concepts | 核心概念（Agent、Session、Memory 等） |
| gateway | Gateway 配置与协议 |
| install | 安装指南（Docker、Kubernetes 等） |
| plugins | 插件开发 |
| providers | AI 模型提供商 |
| tools | 工具参考 |

## 使用示例 / Examples

```bash
# 搜索 memory 相关文档
node scripts/search.js "memory" --limit 10

# 搜索 AI 提供商
node scripts/search.js "openai" --category providers

# 搜索渠道相关
node scripts/search.js "telegram" --category channels

# 搜索安装指南
node scripts/search.js "docker kubernetes" --category install

# AI 友好的 JSON 输出
node scripts/search.js "session" --format json --limit 3
```

## 输出格式 / Output

JSON 模式下的返回格式：

```json
{
  "query": "session",
  "total": 5,
  "returned": 3,
  "results": [
    {
      "path": "concepts/session.md",
      "title": "Session Management",
      "category": "concepts",
      "score": 12.5,
      "summary": "Session transcripts are stored..."
    }
  ]
}
```
