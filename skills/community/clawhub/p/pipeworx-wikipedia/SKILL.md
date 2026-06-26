# Wikipedia

Search, summarize, and explore the structure of English Wikipedia articles.

## Capabilities

**search_wikipedia** -- Full-text search across Wikipedia. Returns titles, text snippets, page IDs, and word counts. Useful for finding the right article before pulling its content.

**get_article_summary** -- The introductory extract for an article by title. Also returns the description, thumbnail URL, and desktop/mobile content links. This is the fastest way to get a concise answer from Wikipedia.

**get_article_sections** -- The table of contents for an article. Returns each section heading with its level, number, and anchor. Helpful for understanding the structure of long articles.

**get_random_articles** -- Fetch 1-10 random Wikipedia articles with their extracts. Good for serendipitous discovery or testing.

## Example: summarize an article

```bash
curl -X POST https://gateway.pipeworx.io/wikipedia/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_article_summary","arguments":{"title":"Turing machine"}}}'
```

```json
{
  "mcpServers": {
    "wikipedia": {
      "url": "https://gateway.pipeworx.io/wikipedia/mcp"
    }
  }
}
```
