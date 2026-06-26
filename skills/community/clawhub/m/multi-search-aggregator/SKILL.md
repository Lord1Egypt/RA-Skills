---
name: multi-search-aggregator
description: 多搜索聚合器 - 一次搜索调用多个引擎（Tavily、Brave、Perplexity），结果统一返回
tags: [search, aggregator, tavily, brave, perplexity]
version: 1.0.0
---

# 🔍 Multi-Search Aggregator 多搜索聚合器

一次搜索调用多个搜索引擎，返回统一格式的结果。

## 功能

- **多源搜索**: 同时调用 Tavily、Brave、Perplexity
- **并行执行**: 多源同时搜索，速度更快
- **统一格式**: 结果标准化输出
- **灵活配置**: 可选择启用哪些搜索源

## 配置

### API Key 配置

在 `~/.openclaw/.env` 中配置：

```bash
# Tavily (必须，至少一个)
TAVILY_API_KEY=tvly-xxx

# Brave Search (可选)
BRAVE_API_KEY=xxx

# Perplexity (可选)
PERPLEXITY_API_KEY=xxx
```

## 使用方式

### 命令行

```bash
# 基本搜索（默认 Tavily + Brave）
python3 scripts/multi_search.py --query "关键词"

# 指定搜索源
python3 scripts/multi_search.py --query "关键词" --sources tavily,brave

# 指定结果数
python3 scripts/multi_search.py --query "关键词" --max-results 10

# 输出格式 (md/json/unified)
python3 scripts/multi_search.py --query "关键词" --format md
python3 scripts/multi_search.py --query "关键词" --format unified
```

### 在 Skill 中调用

```python
import subprocess
import json

result = subprocess.run(
    ["python3", "scripts/multi_search.py", "--query", "搜索内容", "--format", "unified"],
    capture_output=True,
    text=True,
    cwd="/home/admin/.openclaw/workspace/skills/multi-search-aggregator"
)

data = json.loads(result.stdout)
print(data["answer"])  # AI 摘要
for r in data["results"]:
    print(f"{r['title']} - {r['url']}")
```

## 输出格式

### Markdown (--format md)
```markdown
# 🔍 搜索结果: 关键词

**调用源**: tavily, brave

## 📡 TAVILY
**摘要**: AI 总结...

1. **标题**
   🔗 url
   📝 摘要...
```

### Unified JSON (--format unified)
```json
{
  "query": "关键词",
  "sources": ["tavily", "brave"],
  "answer": "AI 总结...",
  "results": [
    {"source": "tavily", "title": "...", "url": "...", "snippet": "..."},
    {"source": "brave", "title": "...", "url": "...", "snippet": "..."}
  ]
}
```

## 示例

### 搜索 AI 新闻
```bash
python3 scripts/multi_search.py --query "AI 最新的技术突破" --sources tavily --format md
```

### 聚合搜索
```bash
python3 scripts/multi_search.py --query "python 教程" --sources tavily,brave --max-results 3 --format unified
```

## 搜索源对比

| 源 | 优点 | 缺点 |
|----|------|------|
| Tavily | 简单可靠，有 AI 摘要 | 需要 API Key |
| Brave | 结果丰富 | 需要 API Key |
| Perplexity | 答案引擎 | 需要 API Key，较慢 |

## 扩展

如需添加新的搜索源，修改 `scripts/multi_search.py` 中的 `search_xxx` 函数：
1. 添加加载 API Key 的逻辑
2. 实现搜索函数
3. 在 `aggregate_search` 中注册
