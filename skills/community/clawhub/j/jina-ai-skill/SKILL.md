---
name: jina-reader
description: "Fetch the markdown content of any webpage using Jina AI's Reader API (r.jina.ai), or search the web using Jina AI's Search API (s.jina.ai). Use this skill whenever you need to read a URL and get clean LLM-friendly markdown output, extract article/documentation content from a page, or search the web and retrieve rich results with content. Triggers on: read this URL, fetch this page, get the content of, what does this page say, summarize this link, search the web for, look up, or any request requiring clean markdown from a URL."
---

# Jina Reader & Search Skill

Two APIs, zero API key required (optional key for higher rate limits).

## Reader — Fetch a URL as Markdown

**Simple (shell):**
```bash
curl -s "https://r.jina.ai/<URL>"
```

**With script:**
```bash
python3 skills/jina-reader/scripts/jina_read.py <URL>
python3 skills/jina-reader/scripts/jina_read.py <URL> --no-images   # strip images
python3 skills/jina-reader/scripts/jina_read.py <URL> --json        # structured JSON response
```

**With API key (set in .env):**
```bash
JINA_API_KEY=your_key python3 skills/jina-reader/scripts/jina_read.py <URL>
```

**Useful request headers (for direct curl):**
| Header | Purpose |
|--------|---------|
| `Authorization: Bearer <key>` | Higher rate limits |
| `X-Return-Format: markdown` | Force markdown output |
| `X-Remove-Selector: img` | Strip images |
| `Accept: application/json` | JSON response with title, url, content |

## Search — Web Search via Jina

**Simple (shell):**
```bash
curl -s "https://s.jina.ai/<URL-encoded-query>"
```

**With script:**
```bash
python3 skills/jina-reader/scripts/jina_search.py "your query"
python3 skills/jina-reader/scripts/jina_search.py "your query" --json
python3 skills/jina-reader/scripts/jina_search.py "your query" --json --results 3
```

## API Key

| API | Without Key | With Key |
|-----|-------------|----------|
| Reader (`r.jina.ai`) | ✅ Works (rate-limited) | Higher limits |
| Search (`s.jina.ai`) | ❌ Requires key | ✅ Works |

Store as `JINA_API_KEY` in `.env`. Get a free key at: https://jina.ai/api-dashboard

> **No key for search?** Use the `duckduckgo-search` skill as a fallback.

## Notes

- Reader works on most pages including JS-heavy sites
- Search returns up to 5 results by default, each with title, URL, and content summary
- For very long pages, use `--no-images` to reduce token usage
