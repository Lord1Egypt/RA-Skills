---
name: pipeworx-bible
description: Fetch Bible verses, passages, and random scripture from bible-api.com — multiple translations supported
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📖"
    homepage: https://pipeworx.io/packs/bible
---

# Bible

Retrieve specific verses, multi-verse passages, or a random scripture selection from bible-api.com. Supports multiple translations and returns structured text with book name, chapter, and verse numbers.

## Tools

- **`get_verse`** — Fetch a specific verse by reference (e.g., "John 3:16")
- **`get_passage`** — Fetch a range of verses (e.g., "Genesis 1:1-5") with optional translation selection
- **`random_verse`** — Pull a random verse from the entire Bible

## Practical uses

- Displaying a daily verse in a devotional app
- Looking up a passage someone referenced in conversation
- Building a Bible study tool with structured verse data
- Generating scripture-based content for newsletters or social posts

## Example

Fetching Psalm 23:1-6 in the default (KJV) translation:

```bash
curl -s -X POST https://gateway.pipeworx.io/bible/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_passage","arguments":{"reference":"psalm 23:1-6"}}}'
```

Returns the full text split by verse, with the translation name and book metadata.

## Connect

```json
{
  "mcpServers": {
    "pipeworx-bible": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/bible/mcp"]
    }
  }
}
```
