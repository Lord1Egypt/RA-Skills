# Cataas

CATAAS MCP — Cat as a Service (free, no auth)

## random_cat

Get a random cat image. Returns image URL, cat ID, and associated tags.

## cat_by_tag

Get a random cat image matching a specific tag (e.g., 'orange', 'cute', 'sleepy'). Returns image URL

## list_tags

List all available cat tags for filtering. Use tag names with cat_by_tag to find cats by appearance 

```json
{
  "mcpServers": {
    "cataas": {
      "url": "https://gateway.pipeworx.io/cataas/mcp"
    }
  }
}
```
