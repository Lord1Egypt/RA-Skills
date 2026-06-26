---
name: pipeworx-books
description: Search and look up books via Open Library — titles, authors, ISBNs, and cover images from the world's largest open book catalog
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📚"
    homepage: https://pipeworx.io/packs/books
---

# Open Library Books

Open Library aims to catalog every book ever published. This pack wraps their API to let you search by title, author, or keyword, look up detailed book info by ISBN, and retrieve author biographies.

## Tools

- **`search_books`** — Search by title, author, or keywords. Returns up to 20 results with titles, authors, publish years, ISBNs, and cover image URLs.
- **`get_book`** — Full details for a book by ISBN-10 or ISBN-13. Includes description, publishers, page count, and subjects.
- **`get_author`** — Author biography, birth/death dates, and photos by Open Library author key (e.g., `OL23919A` for J.K. Rowling).

## Real-world uses

- Answering "who wrote that book about..." questions
- Enriching a reading list with cover images and page counts
- Looking up an ISBN from a barcode scan to get book metadata
- Building a book recommendation system with structured author and subject data

## Example: finding books by Ursula K. Le Guin

```bash
curl -s -X POST https://gateway.pipeworx.io/books/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_books","arguments":{"query":"Ursula Le Guin","limit":5}}}'
```

```json
{
  "results": [
    {
      "title": "The Left Hand of Darkness",
      "authors": ["Ursula K. Le Guin"],
      "first_publish_year": 1969,
      "isbn": "0441478123",
      "cover_url": "https://covers.openlibrary.org/b/id/..."
    }
  ]
}
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-books": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/books/mcp"]
    }
  }
}
```
