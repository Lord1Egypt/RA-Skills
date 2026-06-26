---
name: intel-asrai
description: AI-powered web search via x402 micropayments on Base. Returns synthesized answers with cited sources. Each search costs $0.005 USDC from your own wallet. No API keys, no subscriptions — just connect and search.
license: MIT
metadata: {"openclaw":{"emoji":"🔍","requires":{"env":["INTEL_PRIVATE_KEY"]}},"clawdbot":{"emoji":"🔍","requires":{"env":["INTEL_PRIVATE_KEY"]}}}
---

# Intel — AI Web Search via x402

## Install

```bash
npx -y -p intel-asrai-mcp install-skill
```

Auto-detects OpenClaw, Cursor, Cline, and other agents. Then set your key:

```
INTEL_PRIVATE_KEY=0x<your_private_key>  # add to ~/.env
```

For MCP agents (Cursor, Cline, Claude Desktop) also add to config:

```json
{
  "mcpServers": {
    "intel-search": { "command": "npx", "args": ["-y", "intel-asrai-mcp"] }
  }
}
```

---

Use Intel search when the user asks about current events, recent news, live prices, or anything requiring up-to-date information beyond your training data.

## When to search

- Current events, breaking news, recent developments → search
- Live prices, scores, real-time data → search
- Research needing latest sources → search
- General knowledge you already know well → do NOT search (costs $0.005 USDC each time)

## How to search

### If intel_search tool is available (MCP connected)

```
intel_search(query, mode, sources)
```

### If no MCP tool — use bash (OpenClaw and other agents)

```bash
npx -y -p intel-asrai-mcp intel-search "<query>" <mode> <sources>
```

Examples:
```bash
npx -y -p intel-asrai-mcp intel-search "bitcoin price today" speed web
npx -y -p intel-asrai-mcp intel-search "latest AI research" quality academic
npx -y -p intel-asrai-mcp intel-search "what people think about X" balanced discussions
```

Requires `INTEL_PRIVATE_KEY` set in `~/.env` or environment. Payment ($0.005 USDC) is signed automatically.

## Parameters

- **query** — the search question
- **mode** — `speed` (fast, news), `balanced` (default), `quality` (deep research)
- **sources** — `web` (default), `academic` (papers), `discussions` (Reddit/forums)

## Output rules

- Lead with the synthesized answer — no preamble
- List sources as numbered links after the answer
- For factual questions: direct answer first, then detail
- For news: key developments first, then sources
- Never mention tool names, API calls, or payment details in responses
- Keep it concise — synthesize, don't dump

## Cost

$0.005 USDC per search, signed from the user's own wallet on Base mainnet. Tell the user if they ask.
