---
name: iteratools-api
description: "Call the IteraTools multi-tool API (api.iteratools.com) — 80+ tools for AI agents: image generation (Flux), browser automation (Playwright), web scraping, TTS, OCR, PDF, charts, QR codes, code execution, translation, WhatsApp, and more. Pay-per-use with API key or x402 micropayments. Available as MCP server (npx mcp-iteratools) or REST API."
metadata:
  openclaw:
    requires:
      bins: []
    mcp:
      url: "https://mcp.iteratools.com/mcp"
      protocol: "streamable-http"
    links:
      homepage: "https://iteratools.com"
      docs: "https://docs.iteratools.com"
      npm: "https://www.npmjs.com/package/mcp-iteratools"
      github: "https://github.com/fredpsantos33/iteratools-mcp"
      smithery: "https://smithery.ai/server/iterasoft/iteratools"
---

# IteraTools API

Pay-per-use multi-tool API with MCP support. 80+ tools for AI agents.

## MCP Integration

### Quick Start (Local)

```bash
npx mcp-iteratools
```

Set your API key:

```bash
export ITERATOOLS_API_KEY=it-YOUR-KEY
npx mcp-iteratools
```

### Remote MCP Server

```
URL: https://mcp.iteratools.com/mcp
Protocol: StreamableHTTP (MCP 2025-03-26)
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "iteratools": {
      "command": "npx",
      "args": ["mcp-iteratools"],
      "env": {
        "ITERATOOLS_API_KEY": "your-api-key"
      }
    }
  }
}
```

### OpenClaw

Add to your `openclaw.json` mcp section:

```json
{
  "mcp": {
    "servers": {
      "iteratools": {
        "url": "https://mcp.iteratools.com/mcp"
      }
    }
  }
}
```

## REST API

Base URL: `https://api.iteratools.com`

Auth: `Authorization: Bearer it-YOUR-API-KEY` or x402 micropayments.

## Tool Categories

- **Image**: generate (Flux 1.1 Pro), fast (Schnell), rembg, OCR, describe, resize, compress
- **Video**: generate (Kling v1.6), transcribe, frames
- **AI**: chat (GPT-4o, Claude, etc.), summarize, sentiment, embeddings
- **Memory**: vector upsert/search/clear, KV store
- **Web**: scrape, search, crawl, screenshot, browser automation
- **Messaging**: WhatsApp send/reply, SMS, Slack, email
- **Docs**: PDF extract/generate, document convert, spreadsheet
- **Code**: execute (Python, JS, Bash) in sandbox
- **Productivity**: GitHub (repo/issue/search/file), Google Sheets, Google Calendar
- **Maps**: geocode, places, directions, nearby, distance
- **Utilities**: translate, QR code, barcode, weather, currency, DNS, hash, chart, time convert

## Pricing

All tools are pay-per-use. Most cost $0.001–$0.01 per call. See full pricing at [docs.iteratools.com](https://docs.iteratools.com/#tools-reference).

## Links

- Docs: https://docs.iteratools.com
- API: https://api.iteratools.com
- NPM: https://www.npmjs.com/package/mcp-iteratools
- GitHub: https://github.com/fredpsantos33/iteratools-mcp
- Smithery: https://smithery.ai/server/iterasoft/iteratools
