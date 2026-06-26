---
name: memesio-meme-generator
description: Use for meme generation with Memesio through MCP: search meme templates, add captions to templates or uploaded images, create meme agent accounts, and generate AI memes. Also use when setting up the Memesio Meme Generator in MCP clients or writing install and usage examples.
---

# Memesio Meme Generator MCP

Use the hosted Memesio meme generator MCP server:

- Endpoint: `https://memesio.com/api/mcp`
- Docs: `https://memesio.com/developers/mcp`
- Official registry name: `com.memesio/meme-generator`

## When to use

Trigger this skill when the user wants to:

- connect an MCP client to Memesio
- search meme templates
- caption a known meme template
- caption an uploaded image
- create a Memesio agent account
- generate AI memes through Memesio
- document or submit the Memesio meme generator to MCP directories

## Connection shape

Use a remote streamable HTTP server config:

```json
{
  "mcpServers": {
    "memesio": {
      "type": "streamable-http",
      "url": "https://memesio.com/api/mcp"
    }
  }
}
```

The server does not require connection-level secrets for basic connectivity. Public tools work anonymously. Keyed tools accept `apiKey` as a tool argument instead of transport headers.

## Recommended workflow

1. If the caller needs a key, call `create_agent_account`.
2. Use `search_templates` to discover meme formats.
3. Use `caption_template` when a template slug is already known.
4. Use `caption_upload` when the source image is custom.
5. Use `get_ai_quota` before `generate_meme` for keyed AI meme generation.

## Tool surface

Supported tools:

- `create_agent_account`
- `search_templates`
- `get_template_ideas`
- `caption_template`
- `caption_upload`
- `generate_meme`
- `get_ai_quota`

Read `references/tools.txt` when you need concise behavior guidance or example payloads.
