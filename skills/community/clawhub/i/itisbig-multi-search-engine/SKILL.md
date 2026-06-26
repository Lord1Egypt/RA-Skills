---
name: multi-search-engine
description: Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required.
---

# Multi Search Engine

Multiple search engine integration with support for Chinese and global search engines.

## Supported Search Engines

### Chinese Search Engines (8 total)
- 🔍 Baidu
- 🦉 360 Search
- 🔍 Bing China
- 🇨🇳 Sogou
- 🥇 Weibo
- 🧭 Baidu Scholar
- 🌐 Zhihu
- 🔖 Bing Scholar

### Global Search Engines (9 total)
- 🌍 Google
- 🔍 Bing
- 🦆 DuckDuckGo
- 🐙 Brave Search
- 🌐 Startpage (privacy-focused)
- 🔬 Google Scholar
- 🧠 WolframAlpha (knowledge queries)
- 📰 Brave News
- 🍴 Hacker News

## When to Use

- User asks to search the web for current information
- Need to find recent news
- Search for academic papers
- Ask knowledge-based computational questions (WolframAlpha)
- Prefer privacy-focused search
- Chinese language/region-specific search

## How to use

### Basic Search

```python
from multi_search import search

results = search(
    query="artificial intelligence latest developments", 
    count=5, 
    engine="google" # optional, default searches all configured
)

for result in results:
    print(result.title, result.url, result.snippet)
```

### Command Line

```bash
# Search all engines
multi-search "what is openclaw" --count 10

# Search specific engine
multi-search "machine learning" --engine bing

# Search with time filter
multi-search "AI news" --days 7

# Site-specific search
multi-search "tavily" --site github.com

# WolframAlpha computational knowledge
multi-search "integral of x^2 sinx dx" --engine wolframalpha
```

## Configuration

### Configure API Keys (optional)

Create `.env` file in skill directory:

```
# Optional API keys (most engines work without API keys for basic search)
GOOGLE_API_KEY=your_key
BING_API_KEY=your_key
WOLFRAM_APP_ID=your_id
WOLFRAM_API_KEY=your_key

# Enable/disable specific engines
ENABLED_ENGINES=baidu,bing,google,duckduckgo,bing,startpage,brave
```

**Most Chinese engines work without API keys via web scraping.

## Response Format

```json
[
  {
    "title": "Result Title",
    "url": "https://example.com",
    "snippet": "Text summary",
    "engine": "google",
    "position": 1
  }
]
```

## Features

- **Advanced search operators**: support for (`site:`, `inurl:`, filetype, exact phrase
- **Time filtering**: search within N days/months/years
- **Language preference**: auto-language detection based on query language
- **Fallback**: if one engine fails, falls back to next
- **No API key required**: most engines work without API keys via public endpoints

## Dependencies

```bash
pip install requests beautifulsoup4

## Credits

- Inspired by [searchapi](https://github.com/tobias neutralone
