---
name: pipeworx-gutendex
description: Search Project Gutenberg's 70,000+ free ebooks — by title, author, topic, or popularity via Gutendex
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📜"
    homepage: https://pipeworx.io/packs/gutendex
---

# Project Gutenberg (Gutendex)

Project Gutenberg offers over 70,000 free ebooks. This pack wraps the Gutendex API to search by title, author, or topic, browse the most popular books, and get download links in multiple formats (EPUB, plain text, HTML).

## Tools

| Tool | Description |
|------|-------------|
| `search_books` | Search by title or author name |
| `get_book` | Full details for a specific book by its Gutenberg ID |
| `popular_books` | Most downloaded books on Project Gutenberg |
| `books_by_topic` | Browse by subject keyword (e.g., "science", "love", "history") |

## When to use

- Finding public domain books for text analysis or NLP projects
- Answering "what are the most popular free ebooks?"
- Building a reading list of classic literature by topic
- Getting download links for free ebooks in various formats

## Example: search for Shakespeare

```bash
curl -s -X POST https://gateway.pipeworx.io/gutendex/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_books","arguments":{"query":"Shakespeare"}}}'
```

Returns titles, authors, download count, subjects, and format links (text/html, application/epub+zip, etc.).

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-gutendex": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/gutendex/mcp"]
    }
  }
}
```
