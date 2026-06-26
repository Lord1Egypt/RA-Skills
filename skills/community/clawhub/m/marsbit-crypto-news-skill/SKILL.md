---
name: marsbit-crypto-news-skill
description: Crypto-native Web3 news and flash intelligence from MarsBit through hosted MCP. Use this for L1/L2 ecosystems, DeFi/CeFi, regulation, exchange flows, and market-moving events.
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":["curl"]},"install":[{"id":"curl","kind":"brew","formula":"curl","label":"curl (HTTP client)"}],"os":["darwin","linux","win32"]},"version":"0.3.2"}
---

# MarsBit Crypto News Skill (Web3-focused)

This skill is designed to work immediately after installation using the hosted
MCP endpoint.

MCP endpoint:
- `https://www.marsbit.co/api/mcp`

Use this endpoint in all commands:

```bash
MCP_URL="https://www.marsbit.co/api/mcp"
```

## Capabilities

Use this skill when users ask about:

1. Crypto market-moving headlines
2. Web3 ecosystem updates (Ethereum, Solana, Base, Arbitrum, etc.)
3. DeFi protocols, CeFi exchanges, ETFs, policy and regulation
4. Flash updates for short-term market sentiment
5. Narrative discovery (RWA, AI x Crypto, DePIN, restaking, meme sectors)

## Runtime rules

When user asks for crypto/Web3 information, call MCP tools via `curl` directly.

Required headers for every MCP `POST`:
- `Content-Type: application/json`
- `Accept: application/json, text/event-stream`
- `mcp-protocol-version: 2025-11-25`

Response parsing:
- MCP wraps tool output in `result.content[0].text`
- `text` is a JSON string; parse it before answering
- If `success` is `false`, surface the error and ask user whether to retry with different params

Web3 answer format recommendation:
1. TL;DR (1-2 lines)
2. Market impact (`bullish` / `bearish` / `neutral` + why)
3. Key entities (token/protocol/chain/exchange/regulator)
4. Sources with publication time

## Tool calls

### 1) List tools (quick connectivity check)

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

### 2) Get news channels

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_news_channels","arguments":{}}}'
```

### 3) Get latest crypto/Web3 news

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_latest_news","arguments":{"limit":10}}}'
```

### 4) Search news by Web3 keyword

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"search_news","arguments":{"keyword":"Ethereum Layer2","limit":10}}}'
```

### 5) Get one news detail by id

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"get_news_detail","arguments":{"news_id":"20260304151610694513"}}}'
```

### 6) Get related news by id

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"get_related_news","arguments":{"news_id":"20260304151610694513","limit":6}}}'
```

### 7) Get latest crypto flash updates

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"get_latest_flash","arguments":{"limit":10}}}'
```

### 8) Search flash by Web3 keyword

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"name":"search_flash","arguments":{"keyword":"Solana meme","limit":10}}}'
```

## Intent -> tool routing (Web3)

1. Latest crypto headlines -> `get_latest_news`
2. Category/channel browsing -> `get_news_channels`
3. Narrative or keyword lookup -> `search_news`
4. Deep dive one article -> `get_news_detail`
5. Context expansion -> `get_related_news`
6. Short-term market pulse -> `get_latest_flash`
7. Event scanning by keyword -> `search_flash`

Useful query patterns:
1. Chain: `Ethereum`, `Solana`, `Base`, `Arbitrum`, `Sui`
2. Protocol: `Uniswap`, `Aave`, `Jupiter`, `Pendle`
3. Narrative: `RWA`, `DePIN`, `restaking`, `AI crypto`
4. Risk/Event: `hack`, `exploit`, `liquidation`, `SEC`, `ETF`

## Backend architecture alignment

This skill relies on the current `marsbit-co` hosted MCP implementation (`/api/mcp`), which internally uses:
- `fetcher(..., { marsBit: true })` in `src/lib/utils.ts`
- News APIs: `/info/news/channels`, `/info/news/shownews`, `/info/news/getbyid`, `/info/news/v2/relatednews`
- Flash API: `/info/lives/showlives`
- Search API: `/info/assist/querySimilarityInfo` (via `src/lib/db-marsbit/agent`)

## Install via ClawHub

```bash
clawhub login
clawhub whoami
clawhub install domilin/marsbit-crypto-news-skill
openclaw skills list
```

## Install from GitHub

You can install this skill directly from GitHub when ClawHub is unavailable
(for example, rate-limit errors).

Repository:
- `https://github.com/domilin/marsbit-crypto-news-skill`

Example local install:

```bash
git clone https://github.com/domilin/marsbit-crypto-news-skill /tmp/marsbit-crypto-news-skill
mkdir -p ~/.openclaw/skills/marsbit-crypto-news-skill
cp -R /tmp/marsbit-crypto-news-skill/* ~/.openclaw/skills/marsbit-crypto-news-skill/
openclaw skills list
```
