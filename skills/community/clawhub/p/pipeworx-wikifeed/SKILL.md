# Wikifeed

Curated content from Wikipedia: historical events, featured articles, trending pages, and the picture of the day.

## on_this_day

What happened on March 15th throughout history? Pass a month and day to get historical events, notable births, deaths, and holidays for that date across all years.

## featured_article

Wikipedia's daily featured article for any date. Returns the title, extract, description, URL, and original image.

## most_read

The most popular Wikipedia articles on any given day, ranked by view count. Great for tracking what the world is curious about.

## picture_of_day

Wikipedia's picture of the day with title, description, image URL, and thumbnail.

## Example: what happened on July 20?

```bash
curl -X POST https://gateway.pipeworx.io/wikifeed/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"on_this_day","arguments":{"month":"07","day":"20"}}}'
```

(Spoiler: the Moon landing, among other things.)

## Example: most-read articles yesterday

```bash
curl -X POST https://gateway.pipeworx.io/wikifeed/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"most_read","arguments":{"year":"2025","month":"03","day":"30"}}}'
```

```json
{
  "mcpServers": {
    "wikifeed": {
      "url": "https://gateway.pipeworx.io/wikifeed/mcp"
    }
  }
}
```
