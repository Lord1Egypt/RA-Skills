---
name: news-for-ai
description: >-
  Fetches real-time AI industry news, daily AI digests, and searches AI topics
  including products, models, and MCP services. Outputs structured JSON with
  clean text content and separated media resources. Use when the user mentions
  AI新闻, AI资讯, AI日报, AI热点, AI热榜, AI前沿, AI动态, AI行业趋势,
  AI产品, AI模型, 最新AI, 今日AI, AI圈, 人工智能资讯, ai news, ai daily,
  ai trending, AI选题, AI文章素材, or wants to look up a specific AI topic,
  product, or model by keyword. Also triggers on general questions like
  "今天AI圈有什么新闻", "有什么新的AI进展", "帮我查一下XX模型".
---

# News For AI

Fetches AI news, daily digests, and searches AI-related content. Outputs structured JSON (clean Markdown text + separated images/videos/links), ready for article writing or analysis.

## Setup

```bash
pip install -r ${SKILL_DIR}/requirements.txt
```

## Command Selection

Pick the right command based on user intent:

| User intent | Command | Example |
|---|---|---|
| 最新AI新闻/资讯/热点/行业动态 | `news` | `news --limit 10` |
| AI日报/每日汇总/今日速递 | `daily` | `daily --limit 3` |
| 查找特定话题/产品/模型/技术 | `search` | `search "GPT" --type news` |
| 新闻+日报一起获取 | `all` | `all --limit 10` |

## CLI Reference

```bash
python ${SKILL_DIR}/news_cli.py <command> [options]
```

### Commands and Options

```bash
# AI新闻资讯
python ${SKILL_DIR}/news_cli.py news [--limit N] [--no-content]

# AI日报
python ${SKILL_DIR}/news_cli.py daily [--limit N] [--no-content]

# 搜索（关键词必填）
python ${SKILL_DIR}/news_cli.py search "关键词" [--type TYPE] [--limit N] [--no-content]
#   --type: news / products / models / mcp / all (default: all)

# 新闻+日报
python ${SKILL_DIR}/news_cli.py all [--limit N] [--no-content]
```

| Option | Effect |
|---|---|
| `--limit N` | 返回条数，默认 20 |
| `--no-content` | 跳过正文抓取，仅返回标题+摘要（快 20x，适合浏览选题） |
| `--type TYPE` | 搜索范围过滤，仅 `search` 命令可用 |

## Article Writing Workflow

For gathering source material to write AI articles:

1. **选题** — 快速扫标题：`news --limit 20 --no-content`
2. **深挖** — 获取选中文章的完整正文+图片+链接：`news --limit 5`
3. **定向搜索** — 补充特定话题素材：`search "Sora" --type news --limit 3`

## Output Format

All commands output JSON to stdout, errors to stderr (exit code 1).

### news / daily

```json
{
  "type": "news",
  "timestamp": "2026-03-30 15:00:00 +0800",
  "count": 5,
  "data": [
    {
      "id": 26659,
      "title": "...",
      "description": "摘要...",
      "url": "https://...",
      "create_time": "2026-03-30 14:52:05",
      "pv": 5426,
      "content": "正文纯文本（Markdown格式）...",
      "images": [{"src": "https://...", "alt": "..."}],
      "videos": [{"src": "https://..."}],
      "links": [{"text": "...", "href": "https://..."}]
    }
  ]
}
```

`--no-content` 模式下 `content`、`images`、`videos`、`links` 字段不会出现。

### search

```json
{
  "type": "search",
  "keyword": "千问",
  "search_type": "all",
  "news": {"type": "news", "count": 5, "data": [...]},
  "products": {"type": "products", "count": 3, "data": [...]},
  "models": {"type": "models", "count": 10, "data": [...]},
  "mcp": {"type": "mcp", "count": 1, "data": [...]}
}
```

For complete field definitions of each item type, see [schemas.md](schemas.md).
