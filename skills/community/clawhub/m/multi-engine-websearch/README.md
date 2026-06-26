# 🔍 Multi-Engine WebSearch

A free, open-source web search skill for [OpenClaw](https://openclaw.ai) that queries **6 search engines simultaneously**, merges results, deduplicates URLs, and ranks by cross-engine consensus.

**No API keys required. No paid subscriptions. Runs entirely on your machine.**

## ✨ Features

- 🚀 **6 engines in parallel** — DuckDuckGo, DDG Lite, Yahoo, Yahoo JP, Startpage, Google (headless)
- 📊 **Cross-engine ranking** — Results found in multiple engines rank higher
- 🔄 **Automatic deduplication** — Strips tracking params, normalizes URLs
- 🌐 **Google via headless Chromium** — Bypasses JS rendering with Playwright
- ⚡ **Fast** — All engines run in parallel, typically 3-5 seconds total
- 🆓 **Zero cost** — No API keys, no subscriptions

## 📦 Installation

### Via ClawHub (recommended)
```bash
npx clawhub@latest install multi-engine-websearch
```

### Via Git
```bash
git clone https://github.com/nirveshdagar/multi-engine-websearch.git
```

### Requirements
```bash
pip3 install playwright
python3 -m playwright install chromium
```

## 🚀 Usage

### Basic search
```bash
python3 scripts/search.py "your search query" --json
```

### Options
| Flag | Default | Description |
|------|---------|-------------|
| `--json` / `-j` | off | Output as JSON |
| `--num` / `-n` | 10 | Results per engine |
| `--max` / `-m` | 50 | Max total results |
| `--engines` / `-e` | all 6 | Comma-separated engine list |

### Example output
```json
{
  "query": "AI news 2026",
  "total": 35,
  "engines": {"duckduckgo": 10, "google": 8, "yahoo": 10, ...},
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "snippet": "Description...",
      "engines": ["duckduckgo", "google", "yahoo"]
    }
  ]
}
```

## 🔧 Engines

| Engine | Method | Speed | Reliability |
|--------|--------|-------|-------------|
| DuckDuckGo | HTML scrape | ⚡ Fast | ⭐⭐⭐⭐⭐ |
| DDG Lite | HTML scrape | ⚡ Fast | ⭐⭐⭐⭐ |
| Yahoo | HTML scrape | ⚡ Fast | ⭐⭐⭐⭐ |
| Yahoo JP | HTML scrape | ⚡ Fast | ⭐⭐⭐⭐ |
| Startpage | HTML scrape | ⚡ Fast | ⭐⭐⭐⭐ |
| Google | Headless Chromium | 🐢 ~5s | ⭐⭐⭐⭐ |

## 📜 License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

## 🤝 Contributing

PRs welcome! Ideas for improvement:
- Add more engines (Brave, Bing, Mojeek)
- Improve Google snippet extraction
- Add caching layer for repeated queries
- Browser pool for faster Google searches
