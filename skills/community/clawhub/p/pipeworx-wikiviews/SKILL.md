# Wikiviews

Wikipedia pageview analytics. Track how many people are reading specific articles, find the most popular pages on any given day, or measure aggregate traffic across all of English Wikipedia.

## get_article_views

Daily pageview counts for a specific article over a date range. Dates in YYYYMMDD format. Returns per-day breakdown and total views.

## get_top_articles

The top 1000 most-viewed Wikipedia articles on a specific day. Each entry includes rank, article title, and view count.

## get_project_views

Aggregate daily pageview totals for all of English Wikipedia. Useful for spotting traffic trends and seasonality.

## Example: how popular is the "Taylor Swift" article?

```bash
curl -X POST https://gateway.pipeworx.io/wikiviews/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_article_views","arguments":{"title":"Taylor_Swift","start":"20250301","end":"20250331"}}}'
```

Note: article titles use underscores instead of spaces.

```json
{
  "mcpServers": {
    "wikiviews": {
      "url": "https://gateway.pipeworx.io/wikiviews/mcp"
    }
  }
}
```
