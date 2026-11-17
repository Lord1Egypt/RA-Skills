---
name: unified-web-search
description: "Evidence-first web and workspace search with bounded results, source labels, and machine-readable provenance. Use for research questions, current facts, or finding content in local memory and skills."
license: MIT-0
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["node"]
    version: "1.3.2"
---

# Evidence-first unified search

Use `index.js` when a task needs web retrieval plus a bounded search of local `memory/` and `skills/` content. Results are JSON on stdout; warnings are JSON on stderr so callers can preserve provenance.

## Quick start

```bash
node index.js --query "latest climate policy" --sources '["tavily"]' --allow-network --max_results 5
node index.js --query "meeting notes" --sources '["local"]' --allow-local --max_results 10
node index.js --query "AI developments" --sources '["tavily","local"]' --max_results 10
```

## Trust and scope

- `tavily` requires `TAVILY_API_KEY` and sends the query to Tavily.
- `local` searches only workspace `memory/` and `skills/`, with bounded depth and file size.
- Symlinked files and directories are skipped; binary/unreadable files are ignored.
- `web-search-plus` and `browser` are accepted for compatibility but report that they are not configured rather than pretending to search them.
- Queries are trimmed and capped at 500 characters; `max_results` is 1–50.

Each result includes a source label, title, URL when available, score, and content/snippet. Treat network results as external evidence and verify important claims before relying on them.

## Source and support

Source: https://github.com/iyeque/openclaw-skills/tree/main/skills/unified-web-search

Report bugs and security concerns through the repository issue guidance.
