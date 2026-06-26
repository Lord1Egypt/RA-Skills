# Space News

Stay current with spaceflight news. Pulls articles and blog posts from the Spaceflight News API, aggregating coverage from dozens of space journalism outlets.

## Three tools

1. **get_articles** -- Latest spaceflight news articles, sorted by publication date
2. **search_articles** -- Keyword search across all articles (e.g., "SpaceX Starship launch")
3. **get_blogs** -- Latest spaceflight blog posts from the community

All three return title, summary, URL, image, source outlet, and publication timestamp.

## Example

```bash
curl -X POST https://gateway.pipeworx.io/spacenews/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_articles","arguments":{"query":"Artemis moon","limit":5}}}'
```

```json
{
  "mcpServers": {
    "spacenews": {
      "url": "https://gateway.pipeworx.io/spacenews/mcp"
    }
  }
}
```
