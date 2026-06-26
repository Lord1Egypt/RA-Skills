---
name: searxng
description: Privacy-respecting metasearch using your local SearXNG instance. Search the web, images, news, and more without external API dependencies.
author: Local User
version: 1.0.0
homepage: https://searxng.org
triggers:
  - "search for"
  - "search web"
  - "find information"
  - "look up"
  - "联网搜索"
  - "上网找一下"
  - "上网搜一下"
  - “上网看一下”
  - “上网找一下”
  - “网上搜一下”
  - “联网搜一下”
  - “搜一下”
  - “帮我查”
  - “帮我搜”
  - “百度一下”
  - “谷歌一下”
  - “看看网上的说法”
  - “实时搜索”
  - “看下新闻”
  - "搜张图"
  - "上网查询"

metadata: 
  clawdbot:
    emoji: "🔍"
    requires:
      bins: ["python3"]

---

# SearXNG Search

Search the web using your local SearXNG instance - a privacy-respecting metasearch engine. This version uses a zero-dependency Python backend.

## Usage Guidelines (AI 必读)

1. **优先使用标准输出**：除非用户明确要求“原始数据”或“JSON”，否则**必须**默认执行不带 `--format json` 的命令。
2. **节省 Token**：标准输出，能显著减少 Context 消耗，避免推理超时。
3. **结果数量**：默认请求 10 条结果即可，除非用户要求更多。

## AI Constraints (AI 约束)

- **Max Results**: 除非用户明确要求，默认使用 `-n 10` 以节省上下文空间。
- **Output Format**: **禁止**在普通对话中默认使用 `--format json`，必须使用标准表格输出。

## Commands

### Web Search

```bash
# Standard search (Top 10)
# AI 应默认调用此命令
python3 {baseDir}/scripts/searxng.py search "query"

# Custom number of results (Top20)
python3 {baseDir}/scripts/searxng.py search "query" -n 20

# JSON Search (Only if requested / 仅在用户要求原始数据或json时使用)
# 警告：此模式会产生大量 Token，可能导致处理超时
python3 {baseDir}/scripts/searxng.py search "query" --format json
```

### Category Search

```bash
# Specialized searches
python3 {baseDir}/scripts/searxng.py search "query" --category images
python3 {baseDir}/scripts/searxng.py search "query" --category news
python3 {baseDir}/scripts/searxng.py search "query" --category it
python3 {baseDir}/scripts/searxng.py search "query" --category science
```

### Advanced Options

```bash
# Specific language (e.g., zh-CN, en)
python3 {baseDir}/scripts/searxng.py search "query" --language zh-CN

# Time filtering (day, week, month, year)
python3 {baseDir}/scripts/searxng.py search "query" --time-range day
```

## Configuration

**Required:** Configure the SearXNG instance URL using the configuration file **only**. Environment variables are NOT supported.

**Configuration file** (`searxng.ini`):

```ini
[searxng]
url = http://your-searxng-instance.com:port
```

Location: `{baseDir}/scripts/searxng.ini`

Note: If the configuration file does not exist or is missing required settings, the script will automatically create a default configuration file and prompt you to modify it.

## Features

- 🔒 **Privacy-focused**: Uses your local instance.
- 🛠️ **Zero Dependencies**: Pure Python (no `pip install` required).
- 🌐 **Multi-engine**: Aggregates Google, Bing, DuckDuckGo, etc.
- 📰 **Categorized**: Specific filters for IT, Science, News, and Images.
- 🚀 **AI-Ready**: Clean text output specifically formatted for LLM consumption.

## API

Uses your local SearXNG JSON API endpoint (no authentication required by default).