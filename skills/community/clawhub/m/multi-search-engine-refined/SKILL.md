---
name: "multi-search-engine"
description: "Multi search engine integration with 4 engines: Google, DuckDuckGo, Brave Search, and WolframAlpha. Supports advanced search operators, time filters, and knowledge queries. No API keys required."
---

# Multi Search Engine v2.0.1

Integration of four search endpoints for web fetching without API keys.

## Search Engines

| Engine | URL template |
|--------|----------------|
| **Google** | `https://www.google.com/search?q={keyword}` |
| **DuckDuckGo** | `https://duckduckgo.com/html/?q={keyword}` |
| **Brave** | `https://search.brave.com/search?q={keyword}` |
| **WolframAlpha** | `https://www.wolframalpha.com/input?i={keyword}` |

## Quick Examples

```javascript
// Google
web_fetch({"url": "https://www.google.com/search?q=python+tutorial"})

web_fetch({"url": "https://www.google.com/search?q=site:github.com+react"})

web_fetch({"url": "https://www.google.com/search?q=machine+learning+filetype:pdf"})

web_fetch({"url": "https://www.google.com/search?q=ai+news&tbs=qdr:w"})

// DuckDuckGo
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy+tools"})

web_fetch({"url": "https://duckduckgo.com/html/?q=!g+machine+learning"})

// Brave
web_fetch({"url": "https://search.brave.com/search?q=privacy+tools"})

// WolframAlpha
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})
```

## Advanced Operators (Google)

| Operator | Example | Description |
|----------|---------|-------------|
| `site:` | `site:github.com python` | Search within site |
| `filetype:` | `filetype:pdf report` | Specific file type |
| `""` | `"machine learning"` | Exact match |
| `-` | `python -snake` | Exclude term |
| `OR` | `cat OR dog` | Either term |

## Time Filters (Google)

| Parameter | Description |
|-----------|-------------|
| `tbs=qdr:h` | Past hour |
| `tbs=qdr:d` | Past day |
| `tbs=qdr:w` | Past week |
| `tbs=qdr:m` | Past month |
| `tbs=qdr:y` | Past year |

## Privacy-Oriented Search

- **DuckDuckGo**: No tracking; HTML endpoint works well with `web_fetch`.
- **Brave**: Independent index.

## Bangs Shortcuts (DuckDuckGo)

Use inside the `q` parameter on `duckduckgo.com` (many bangs redirect to third-party sites when used in a browser; `web_fetch` only retrieves the DuckDuckGo URL you request).

| Bang | Role |
|------|------|
| `!g` | Run query on Google |
| `!brave` | Run query on Brave Search |

## WolframAlpha Queries

- Math: `integrate x^2 dx`
- Conversion: `100 USD to CNY`
- Stocks: `AAPL stock`
- Weather: `weather in Beijing`

## Documentation

- `references/international-search.md` — Detailed guide for these four engines
- `CHANGELOG.md` — Version history

## License

MIT
