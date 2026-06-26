---
name: noya-agent-skill
description: Interact with the Noya AI platform for crypto trading, prediction markets, token analysis, DCA strategies, and structured crypto data (prices, TVL, funding rates, on-chain analytics, sentiment, news) via curl. Use when the user wants to trade tokens, check portfolios, analyze markets, manage DCA strategies, interact with Polymarket/Rain prediction markets, or pull deterministic crypto data without hitting the agent graph.
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "homepage": "https://agent.noya.ai",
        "requires":
          {
            "env": [],
            "optionalEnv": ["NOYA_API_KEY"],
            "bins": ["curl", "jq"],
          },
        "primaryEnv": "NOYA_API_KEY",
      },
  }
---

# Noya Agent

Noya is a multi-agent AI system for crypto trading, prediction markets (Polymarket, Rain), token analysis, and DCA strategies, plus a large suite of public structured-data endpoints (prices, TVL, funding rates, liquidations, wallet analytics, news, sentiment, prediction-market intelligence, AI-scored token catalog). All on-chain transactions are gas-sponsored — users pay no gas fees.

- **Website:** [agent.noya.ai](https://agent.noya.ai)
- **Agent API Base URL:** `https://agent-api.noya.ai` (requires `NOYA_API_KEY`)
- **Data API Base URL:** `https://data-endpoints.noya.ai` (no API key, no account needed)
- **Docs Base URL:** `https://mcp.noya.ai` (public, no auth — `/llms.txt` for index, `/llms.mdx/docs/{path}/content.md` for full page content)

## Trust & Security

- All API calls use HTTPS. Only `NOYA_API_KEY` is read from the environment, and it is only needed for the conversational agent endpoints.
- The public data endpoints at `data-endpoints.noya.ai` are unauthenticated and can be called without any setup.
- All on-chain transactions require explicit user confirmation via an interrupt prompt before execution.
- Use a short-lived API key (30-day) for testing. Revoke it from Settings > API Keys if compromised.

## Setup

The public data endpoints (see [Data Endpoints](#data-endpoints-no-api-key)) work immediately with no setup.

To additionally use the conversational agent endpoints (messaging, threads, chat completions, user summary, agent summary):

1. Create an account at [agent.noya.ai](https://agent.noya.ai)
2. Go to Settings > API Keys and generate a key
3. Store the key securely — it is only shown once
4. Set the environment variable:

```bash
export NOYA_API_KEY="noya_your_key_here"
```

Configure in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "noya-agent": {
        "enabled": true,
        "apiKey": "noya_your_key_here",
        "env": {
          "NOYA_API_KEY": "noya_your_key_here"
        }
      }
    }
  }
}
```

## When to Use

Use Noya when users want to:

- Check token prices or portfolio balances
- Swap, bridge, or send tokens (cross-chain supported)
- Analyze tokens and market trends
- Trade on Polymarket or Rain prediction markets
- Set up or manage DCA (dollar-cost averaging) strategies
- View DeFi positions
- Start a voice conversation with the Noya agent
- Pull deterministic crypto data: spot/historical prices (CoinGecko), TVL & yields (DeFiLlama), funding rates / open interest / liquidations (CoinGlass), wallet balances / transfers / DeFi & NFT positions (Moralis), crypto news with sentiment (CryptoNews), Fear & Greed index, on-chain DEX pools & trades (GeckoTerminal), AI-scored token catalog, Polymarket market intelligence, Kaito social intelligence (mindshare, volume-weighted sentiment, smart-follower graph, catalyst events)

**Routing guidance:**

- **Use the data endpoints** (no API key, direct curl) for deterministic lookups — prices, TVL, funding rates, news, on-chain analytics, prediction-market discovery, Kaito mindshare/sentiment/smart-follower data. Faster and cheaper than going through the agent graph.
- **Use the agent** (`noya-message.sh`) for anything that requires reasoning, execution, or the user's connected wallet: swaps, bridges, transfers, DCA setup, placing Polymarket orders, personalized portfolio Q&A.

**Don't use for:** Non-crypto tasks, local file operations, or general knowledge questions.

## Core Workflow

Every interaction uses the Noya REST API. The primary endpoint is `POST /api/messages/stream` which returns a streamed response. **Always use the provided `noya-message.sh` script** to send messages — it handles streaming, chunk parsing, and formatted output. Do not call the message endpoint with raw curl.

**OpenClaw integration:** For every new chat OpenClaw initiates with Noya, first call the system message endpoint (step 2.5) to hand off conversation context. This makes the chat feel like a seamless continuation of the user's conversation with OpenClaw.

### 0. Read the Docs (when unsure)

When you need to understand a tool's parameters, response shape, or usage patterns, fetch the docs directly as plain markdown — no API key required:

```bash
# Full index of all doc pages
curl -s https://mcp.noya.ai/llms.txt

# Full content of a specific page
curl -s https://mcp.noya.ai/llms.mdx/docs/data-endpoints/coinglass/content.md
curl -s https://mcp.noya.ai/llms.mdx/docs/data-endpoints/moralis/content.md
curl -s https://mcp.noya.ai/llms.mdx/docs/data-endpoints/coingecko/content.md
```

The index lists every page with its description. Use it to discover what's available, then fetch the specific page for parameter details and examples. Always check the docs before guessing at a response shape.

### 1. Discover Capabilities (first use)

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://agent-api.noya.ai/api/agents/summarize" | jq '.data'
```

Returns all available agent types (token analysis, prediction markets, DCA, etc.) and their tools. Call this once to understand what Noya can do.

### 2. Generate a Thread ID (new conversation)

Generate a UUID v4 for each new conversation topic:

```bash
python3 -c "import uuid; print(uuid.uuid4())"
```

Or on macOS/Linux:

```bash
uuidgen | tr '[:upper:]' '[:lower:]'
```

Each conversation needs a unique UUID. Generate one per topic and reuse it for follow-ups.

### 2.5 Initialize Thread with Conversation Context (OpenClaw)

**For every new chat that OpenClaw initiates with Noya, call this endpoint first** to set up the conversation context. This makes the chat with Noya feel like a natural continuation of the user's conversation with OpenClaw, rather than starting fresh.

```bash
curl -s -X POST "https://agent-api.noya.ai/api/openclaw/system-message" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $NOYA_API_KEY" \
  -d '{
    "threadId": "THREAD_ID_HERE",
    "content": "The user has been chatting with OpenClaw and now wants help with crypto/trading tasks. Here is the relevant context from our conversation:\n\n- The user mentioned they have a meeting at 3pm today and want to check their portfolio before then\n- They previously expressed preference for ETH over BTC\n- Their timezone is EST\n- Earlier in our chat, they asked about setting up a DCA strategy\n\nPlease continue assisting them naturally, as if this is a seamless handoff from our conversation."
  }'
```

The `content` field should frame the handoff as a conversation continuation. Include:

- A brief intro explaining the user was chatting with OpenClaw and is now being handed off to Noya
- Relevant context from the OpenClaw conversation (what the user asked about, their goals)
- User's schedule, preferences, and any other helpful details
- A note to continue the conversation naturally

This ensures the user doesn't have to repeat themselves and Noya can pick up where OpenClaw left off.

**Response:**

```json
{
  "success": true,
  "filtered": false,
  "message": "Content was sanitized before appending"
}
```

The content passes through a security filter. If `filtered` is `true`, the content was sanitized before being added. If the content is rejected entirely, you'll receive a `400` error with a `reason` field.

**Important:** Call this endpoint _before_ sending the first user message via `noya-message.sh`. The system message will be prepended to the thread's context.

### 3. Send Messages (streaming)

Use the provided script to send a message and receive the parsed response:

```bash
bash {baseDir}/noya-message.sh "What tokens do I have in my portfolio?" "THREAD_ID_HERE"
```

The script handles the streaming response, parses `--breakpoint--` delimited JSON chunks, and outputs formatted text including messages, tool results, progress indicators, and interrupt prompts.

### 4. Continue the Conversation

Reuse the same thread ID for follow-ups — Noya maintains context:

```bash
bash {baseDir}/noya-message.sh "Swap 0.1 ETH to USDC" "SAME_THREAD_ID"
```

### 5. Respond to Interrupts

When the agent needs confirmation (e.g., before executing a swap), the output includes `[REQUIRES INPUT]` with options. Send the user's answer as a follow-up in the same thread:

```bash
bash {baseDir}/noya-message.sh "Yes" "SAME_THREAD_ID"
```

## Start Voice Chat

Opens the Noya AI agent in voice chat mode in the user's browser. Use this when the user wants to talk to Noya by voice instead of text.

**Always include `threadIdToUse`** when OpenClaw initiates the voice chat. Since step 2.5 (set system message) creates the thread beforehand with conversation context, you must pass that thread ID to continue the same conversation:

```bash
open "https://agent.noya.ai?mode=voice&threadIdToUse=THREAD_ID_HERE"
```

Only omit `threadIdToUse` if the user explicitly asks to start a completely fresh voice session without any context:

```bash
open "https://agent.noya.ai?mode=voice"
```

On Linux, use `xdg-open` instead of `open`.

## API Reference (curl commands)

All endpoints require the `x-api-key` header. Base URL: `https://agent-api.noya.ai`

### Send Message (streaming) — ALWAYS use the script

**Do not call `/api/messages/stream` with raw curl.** The response is a custom streamed format that requires parsing. Always use the provided script:

```bash
bash {baseDir}/noya-message.sh "<message>" "<threadId>"
```

The script handles authentication, streaming, `--breakpoint--` chunk parsing, and outputs clean formatted text (messages, tool results, interrupts, progress, errors).

### List Threads

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://agent-api.noya.ai/api/threads" | jq '.data.threads'
```

### Get Thread Messages

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://agent-api.noya.ai/api/threads/THREAD_ID/messages" | jq '.data.messages'
```

### Delete Thread

```bash
curl -s -X DELETE -H "x-api-key: $NOYA_API_KEY" \
  "https://agent-api.noya.ai/api/threads/THREAD_ID"
```

### Get Agent Summary

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://agent-api.noya.ai/api/agents/summarize" | jq '.data'
```

### Get User Summary (all holdings, DCA strategies, Polymarket positions)

Returns a single structured snapshot of everything relevant to the authenticated user — ideal for feeding as context to another agent.

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://agent-api.noya.ai/api/user/summary" | jq '.data'
```

Response includes:

- `holdings` — all wallet tokens and DeFi app positions with USD values
- `dcaStrategies` — all DCA strategies (active, inactive, errored, completed)
- `polymarket.openPositions` — current open prediction market positions with PnL
- `polymarket.closedPositions` — 20 most recently closed positions

### Set System Message (OpenClaw)

Injects a system message into a thread before the conversation starts. **OpenClaw should call this for every new chat** to hand off conversation context to Noya, making the transition feel seamless for the user.

```bash
curl -s -X POST "https://agent-api.noya.ai/api/openclaw/system-message" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $NOYA_API_KEY" \
  -d '{
    "threadId": "THREAD_ID_HERE",
    "content": "The user has been chatting with OpenClaw and now wants help with crypto tasks. Context from our conversation: ... Please continue assisting them naturally."
  }'
```

**Request body:**

- `threadId` (string, required) — The thread ID to attach the system message to
- `content` (string, required) — Conversation context framed as a handoff from OpenClaw to Noya

**Response:**

- `success` (boolean) — Whether the operation succeeded
- `filtered` (boolean) — Whether the content was sanitized by the security filter
- `message` (string, optional) — Present if content was sanitized

**Errors:**

- `400` — Invalid request or content rejected by security filter (includes `reason`)
- `401` — Unauthorized (invalid API key)

## Data Endpoints (no API key)

Noya also exposes a large set of public, unauthenticated structured-data endpoints at `https://data-endpoints.noya.ai`. These are ideal for deterministic lookups — they do **not** route through the agent graph, so they are faster and require no `NOYA_API_KEY`.

**Conventions:**

- All POST endpoints take a JSON body with the parameters below. GET endpoints take none.
- All endpoints return JSON from the upstream provider.
- No auth header required.

Prefer these over `noya-message.sh` whenever the user just wants raw data.

### alternative.me

| Tool               | Method | Path                      | Body                         |
| ------------------ | ------ | ------------------------- | ---------------------------- |
| Fear & Greed Index | POST   | `/alternative/fear-greed` | `{ "limit": 10 }` (optional) |

### GeckoTerminal (on-chain DEX data)

| Tool                   | Method | Path                            | Body                                                                                                                |
| ---------------------- | ------ | ------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Token pools            | POST   | `/geckoterminal/token-pools`    | `{ "network": "eth", "tokenAddress": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" }`                                |
| Pool OHLCV candles     | POST   | `/geckoterminal/pool-ohlcv`     | `{ "network": "eth", "poolAddress": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640", "timeframe": "day", "limit": 7 }` |
| Pool trades            | POST   | `/geckoterminal/pool-trades`    | `{ "network": "eth", "poolAddress": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640" }`                                 |
| Trending pools         | GET    | `/geckoterminal/trending-pools` | —                                                                                                                   |
| Token info + top pools | POST   | `/geckoterminal/token-info`     | `{ "network": "eth", "addresses": ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"] }`                                 |

### CoinGecko

| Tool                   | Method | Path                       | Body                                                                                                                   |
| ---------------------- | ------ | -------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Batch spot prices      | POST   | `/coingecko/price`         | `{ "tokenIds": ["bitcoin","ethereum"], "vsCurrencies": ["usd"], "include24hrChange": true, "includeMarketCap": true }` |
| OHLCV candles          | POST   | `/coingecko/ohlcv`         | `{ "tokenId": "bitcoin", "vsCurrency": "usd", "days": "7", "interval": "daily" }`                                      |
| Token info / contracts | POST   | `/coingecko/token-info`    | `{ "tokenId": "ethereum" }`                                                                                            |
| Trending tokens        | GET    | `/coingecko/trending`      | —                                                                                                                      |
| Search by name/symbol  | POST   | `/coingecko/search`        | `{ "query": "eth" }`                                                                                                   |
| Price history          | POST   | `/coingecko/price-history` | `{ "tokenId": "bitcoin", "days": "30" }` or `{ "tokenId": "bitcoin", "from": "2026-01-01", "to": "2026-02-01" }`       |
| Price at date          | POST   | `/coingecko/price-at-date` | `{ "tokenId": "bitcoin", "date": "2025-12-31" }`                                                                       |

> Note: CoinGecko endpoints use token **IDs** (e.g. `bitcoin`, `ethereum`), not symbols. Use `/coingecko/search` first if you only know the symbol.

### CoinGlass (derivatives)

| Tool                         | Method | Path                                  |
| ---------------------------- | ------ | ------------------------------------- |
| Funding rates                | POST   | `/coinglass/funding-rates`            |
| Open interest by exchange    | POST   | `/coinglass/open-interest`            |
| Aggregated liquidations      | POST   | `/coinglass/liquidations`             |
| Long/short ratio             | POST   | `/coinglass/long-short-ratio`         |
| Supported coins              | GET    | `/coinglass/supported-coins`          |
| Supported exchanges          | GET    | `/coinglass/supported-exchanges`      |
| Futures trading pairs        | POST   | `/coinglass/exchange-pairs`           |
| Liquidations by exchange     | POST   | `/coinglass/liquidations-by-exchange` |
| Funding rate history (OHLC)  | POST   | `/coinglass/funding-rate-history`     |
| Open interest history (OHLC) | POST   | `/coinglass/open-interest-history`    |
| Liquidation history          | POST   | `/coinglass/liquidation-history`      |
| Long/short ratio history     | POST   | `/coinglass/long-short-ratio-history` |

### CryptoNews

| Tool               | Method | Path                    | Body / Query                                                                                 |
| ------------------ | ------ | ----------------------- | -------------------------------------------------------------------------------------------- |
| News articles      | POST   | `/cryptonews/news`      | `{ "tickers": "BTC,ETH", "items": 10, "sentiment": "positive" }`                             |
| Sentiment analysis | POST   | `/cryptonews/sentiment` | `{ "tickers": "BTC,ETH", "date": "last7days" }` (`date` defaults to `last30days` if omitted) |
| Trending tickers   | GET    | `/cryptonews/trending`  | optional `?date=last7days` (omit for all-time)                                               |

### DeFiLlama

| Tool                    | Method | Path                       |
| ----------------------- | ------ | -------------------------- |
| Protocol/chain TVL      | POST   | `/defillama/tvl`           |
| Yield pools (APY/APR)   | POST   | `/defillama/yields`        |
| Protocol fees & revenue | POST   | `/defillama/protocol-fees` |
| DEX volumes             | POST   | `/defillama/dex-volumes`   |
| Stablecoin supply       | POST   | `/defillama/stablecoins`   |
| Bridge volume/flows     | POST   | `/defillama/bridges`       |
| List all bridges        | GET    | `/defillama/bridges/list`  |

### Moralis (wallet analytics)

`chain` accepts names (`eth`, `bsc`, `polygon`, `arbitrum`, `base`, `optimism`, `avalanche`) or hex IDs. `toBlock` is supported only on `/moralis/wallet` (historical token-balance snapshot); the DeFi-positions and NFT-holdings endpoints return current state only.

| Tool                        | Method | Path                      | Body                                                                             |
| --------------------------- | ------ | ------------------------- | -------------------------------------------------------------------------------- |
| Wallet balances & net worth | POST   | `/moralis/wallet`         | `{ "address": "0x...", "chain": "eth", "toBlock": 19500000 }` (toBlock optional) |
| ERC20 transfer history      | POST   | `/moralis/transfers`      | `{ "address": "0x...", "chain": "eth", "limit": 100 }`                           |
| Active DeFi positions       | POST   | `/moralis/defi-positions` | `{ "address": "0x...", "chain": "eth" }`                                         |
| NFT holdings                | POST   | `/moralis/nft-holdings`   | `{ "address": "0x...", "chain": "eth", "limit": 50 }`                            |

### Noya Tokens (AI-scored catalog)

| Tool                                                       | Method | Path                           |
| ---------------------------------------------------------- | ------ | ------------------------------ |
| Text + filter search                                       | POST   | `/noya/tokens/search`          |
| Similar tokens                                             | POST   | `/noya/tokens/similar`         |
| Recommendations by risk                                    | POST   | `/noya/tokens/recommendations` |
| Top AI-scored tokens                                       | POST   | `/noya/tokens/top-score`       |
| Service health                                             | GET    | `/noya/tokens/health`          |
| Available analysis versions                                | GET    | `/noya/tokens/versions`        |
| Tokens by version (latest if `versionId` omitted)          | POST   | `/noya/tokens/by-version`      |
| Full token analysis detail (latest if `versionId` omitted) | POST   | `/noya/tokens/detail`          |

### Noya Polymarket (prediction-market intelligence)

| Tool                         | Method | Path                               |
| ---------------------------- | ------ | ---------------------------------- |
| Semantic search              | POST   | `/noya/polymarket/search`          |
| Similar markets              | POST   | `/noya/polymarket/similar`         |
| Personalized recommendations | POST   | `/noya/polymarket/recommendations` |
| Top markets by EV            | POST   | `/noya/polymarket/top-ev`          |
| Hybrid text + filter         | POST   | `/noya/polymarket/filter`          |
| Event list                   | POST   | `/noya/polymarket/events`          |
| Markets for an event slug    | POST   | `/noya/polymarket/by-event`        |
| Tags                         | POST   | `/noya/polymarket/tags`            |
| Service health               | GET    | `/noya/polymarket/health`          |

### Kaito (social intelligence)

Kaito requires **entity resolution first**: before any analytics call that takes `token`/`tokens`, resolve the identifier via `/kaito/entities`. Narrative IDs are case-sensitive — resolve via `/kaito/narratives`.

| Tool                                             | Method | Path                            |
| ------------------------------------------------ | ------ | ------------------------------- |
| Resolve token identifiers                        | GET    | `/kaito/entities`               |
| Resolve narrative IDs (case-sensitive)           | GET    | `/kaito/narratives`             |
| Natural-language search                          | POST   | `/kaito/search`                 |
| Advanced structured search (field-level control) | POST   | `/kaito/advanced-search`        |
| Single-tweet engagement metrics                  | POST   | `/kaito/tweet-engagement`       |
| Ranked top-content feed                          | POST   | `/kaito/feeds`                  |
| Token sentiment time series (volume-weighted)    | POST   | `/kaito/sentiment`              |
| Engagement time series (token or keyword)        | POST   | `/kaito/engagement`             |
| Mention counts (token or keyword)                | POST   | `/kaito/mentions`               |
| Token mindshare time series                      | POST   | `/kaito/mindshare`              |
| Mindshare leaderboard (top 100)                  | POST   | `/kaito/mindshare-arena`        |
| Mindshare gainers/losers                         | POST   | `/kaito/mindshare-delta`        |
| Narrative mindshare time series                  | POST   | `/kaito/mindshare-narrative`    |
| Top KOLs by mindshare for a token                | POST   | `/kaito/kol-mindshare`          |
| Upcoming catalyst events for a token             | POST   | `/kaito/events`                 |
| Twitter user metadata by user ID                 | POST   | `/kaito/twitter-user-metadata`  |
| Accounts smart followers are following           | POST   | `/kaito/market-smart-following` |
| Smart follower count or list                     | POST   | `/kaito/smart-followers`        |
| Latest 100 smart accounts followed               | POST   | `/kaito/smart-following`        |

**Kaito interpretation rules (apply across tools):**

- `sentiment_score` is volume-weighted and absolute — compare against the entity's own historical range, not fixed thresholds. `sentiment_score` is NOT `smart_engagement`.
- Mindshare rank: Top 10 dominant, Top 20 strong, Top 50 moderate, >50 weak. If all-zero data is returned for a ticker, retry with the full project name (e.g. `HYPE` → `HYPERLIQUID`).
- Narrative movement classification: Surging ≥ +10%, Fading ≤ −10%, Stable within ±10%.
- Spike detection for engagement/mentions: flag any day exceeding 2× the period average; cross-reference with `/kaito/events`.
- Smart follower tiers: 5,000+ Elite, 1,000–5,000 Strong, 300–1,000 Solid, 50–300 Emerging, <50 Low.
- `/kaito/events` returns forward-looking catalysts only — always cite the per-event `references` URL. Flag events within 7 days as imminent.
- Advanced-search rules: put time in `min_created_at`/`max_created_at`, not in `query`. Prefer `tokens` alone when the project resolves; Kaito ANDs all fields so every added parameter narrows results. Twitter-only sort options (`smart_engagement`, `engagement`, `sentiment`, `bookmark`, `views`, `author`) aren't compatible with News — use `relevance` or `created_at` across both.

### Batch (parallel multi-request)

Dispatch up to 20 data endpoints in a single HTTP call. Each sub-request runs in parallel through the same rate limiter and cache as a direct call, so cache entries are shared and partial failures are isolated (one failing item never fails the whole batch).

| Tool                               | Method | Path     | Body                                                                                     |
| ---------------------------------- | ------ | -------- | ---------------------------------------------------------------------------------------- |
| Run multiple endpoints in one call | POST   | `/batch` | `{ "requests": [ { "name": "...", "method": "POST", "path": "/...", "body": {...} } ] }` |

Each `requests[]` item:

- `name` (string, required, ≤100 chars) — caller-supplied unique key; results are returned as `results[name]`
- `method` (string, required) — `GET` or `POST`
- `path` (string, required) — full endpoint path starting with `/`, e.g. `/coingecko/price`. Nested `/batch` calls are rejected.
- `body` (object, optional) — JSON body for POST endpoints
- `query` (object, optional) — query params for GET endpoints that take input via query string
- `timeoutMs` (integer, optional) — per-item timeout override in ms, capped at 60000

Top-level `defaultTimeoutMs` (integer, optional) sets the default per-item timeout (default `15000`, max `60000`). Batch size is capped at 20 items; names must be unique within a batch.

```bash
curl -s -X POST "https://data-endpoints.noya.ai/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [
      { "name": "btc-price",   "method": "POST", "path": "/coingecko/price",
        "body": { "tokenIds": ["bitcoin"], "vsCurrencies": ["usd"] } },
      { "name": "fear-greed",  "method": "POST", "path": "/alternative/fear-greed",
        "body": { "limit": 1 } },
      { "name": "btc-funding", "method": "POST", "path": "/coinglass/funding-rates",
        "body": { "symbol": "BTC" } }
    ]
  }' | jq
```

Response shape:

```json
{
  "results": {
    "btc-price":   { "ok": true,  "status": 200, "data": [...], "cache": "HIT" },
    "fear-greed":  { "ok": true,  "status": 200, "data": {...}, "cache": "MISS" },
    "btc-funding": { "ok": false, "status": 504, "error": "Sub-request timed out after 15000ms" }
  }
}
```

Each result is either `{ ok: true, status, data, cache? }` or `{ ok: false, status, error }`. `cache` is `"HIT"` or `"MISS"` when the sub-request went through the cache layer. Use `/batch` whenever you'd otherwise fire multiple sequential curls to the same base URL — it reduces round-trips without changing per-item semantics.

### Calling a data endpoint with curl

```bash
# POST with a JSON body (no auth header)
curl -s -X POST "https://data-endpoints.noya.ai/coingecko/price" \
  -H "Content-Type: application/json" \
  -d '{"tokenIds":["bitcoin","ethereum"],"vsCurrencies":["usd"],"include24hrChange":true}' \
  | jq
```

```bash
# GET (no body, no auth)
curl -s "https://data-endpoints.noya.ai/coingecko/trending" | jq
```

```bash
# Fear & Greed
curl -s -X POST "https://data-endpoints.noya.ai/alternative/fear-greed" \
  -H "Content-Type: application/json" -d '{"limit":7}' | jq
```

If the user provides a plain symbol ("SOL", "ARB"), resolve it to a CoinGecko ID first:

```bash
curl -s -X POST "https://data-endpoints.noya.ai/coingecko/search" \
  -H "Content-Type: application/json" -d '{"query":"sol"}' | jq '.coins[0].id'
```

## Common Patterns

### Check Portfolio

```
User: "What's in my wallet?"

1. Generate a thread ID: uuidgen | tr '[:upper:]' '[:lower:]'
2. bash {baseDir}/noya-message.sh "What tokens do I have in my portfolio?" "$THREAD_ID"
→ Returns wallet address, token balances, and portfolio data
```

### Token Swap

```
User: "Swap 0.5 ETH to USDC"

1. Generate a thread ID
2. bash {baseDir}/noya-message.sh "Swap 0.5 ETH to USDC" "$THREAD_ID"
→ Noya prepares the swap, asks for confirmation (interrupt), then executes.
   All gas fees are sponsored. User must confirm before execution.
3. bash {baseDir}/noya-message.sh "Yes" "$THREAD_ID"  # after user confirms
```

### Token Analysis

```
User: "Analyze SOL for me"

1. Generate a thread ID
2. bash {baseDir}/noya-message.sh "Give me a detailed analysis of SOL" "$THREAD_ID"
→ Returns price data, market trends, and analysis
```

### DCA Strategy

```
User: "Set up a DCA for ETH"

1. Generate a thread ID
2. bash {baseDir}/noya-message.sh "Set up a weekly DCA strategy for ETH with $50" "$THREAD_ID"
→ Noya configures the DCA strategy and confirms details
```

### Prediction Markets

```
User: "What are the top Polymarket events?"

1. Generate a thread ID
2. bash {baseDir}/noya-message.sh "Show me the top trending Polymarket events" "$THREAD_ID"
→ Returns current events, markets, and trading options
```

### Full User Context for Another Agent

```
Use case: You need to brief another AI agent on everything about the user
before delegating a task to it.

1. curl -s -H "x-api-key: $NOYA_API_KEY" \
     "https://agent-api.noya.ai/api/user/summary" | jq '.data' > user_context.json
2. Pass user_context.json as the system/user context to the downstream agent.
→ Returns wallet holdings, all DCA strategies, open and closed Polymarket
  positions in a single JSON object. Partial failures are isolated — the
  response always returns whatever data is available, with an error field
  for any source that failed.
```

### Quick Price Check (no API key)

```
User: "What's the price of BTC and ETH right now?"

curl -s -X POST "https://data-endpoints.noya.ai/coingecko/price" \
  -H "Content-Type: application/json" \
  -d '{"tokenIds":["bitcoin","ethereum"],"vsCurrencies":["usd"],"include24hrChange":true}' | jq

→ Returns USD prices and 24h change. No agent round-trip, no thread ID.
```

### Market Sentiment Snapshot (no API key)

```
User: "How's market sentiment today?"

1. curl -s -X POST "https://data-endpoints.noya.ai/alternative/fear-greed" \
     -H "Content-Type: application/json" -d '{"limit":1}' | jq
2. curl -s "https://data-endpoints.noya.ai/cryptonews/trending?date=last7days" | jq
→ Fear & Greed index + trending tickers from crypto news.
```

### Wallet Snapshot for Any Address (no API key)

```
User: "What's in wallet 0xabc...?"

curl -s -X POST "https://data-endpoints.noya.ai/moralis/wallet" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xabc...","chain":"eth"}' | jq

→ Works for any address. For the user's own connected wallet, prefer
  /api/user/summary (agent API) which also includes DCA & Polymarket.
```

### Discover Top Polymarket Opportunities (no API key)

```
User: "Show me the best Polymarket bets right now"

curl -s -X POST "https://data-endpoints.noya.ai/noya/polymarket/top-ev" \
  -H "Content-Type: application/json" -d '{"limit":10}' | jq

→ Use for research. To actually place a trade, switch to the agent
  via noya-message.sh (requires API key + user wallet).
```

### Voice Chat

```
User: "I want to talk to Noya"

1. Generate a thread ID
2. Call set system message endpoint with conversation context (step 2.5)
3. open "https://agent.noya.ai?mode=voice&threadIdToUse=$THREAD_ID"
→ Opens voice chat with OpenClaw's conversation context already loaded

User: "Start a fresh voice chat with Noya, no context needed"

1. open "https://agent.noya.ai?mode=voice"
→ Opens voice chat without any prior context (only when user explicitly requests)
```

## Important Notes

### Transaction Confirmation

Noya always asks for user confirmation before executing on-chain transactions (swaps, bridges, transfers, orders). The response will include a `[REQUIRES INPUT]` section with details and options. Always relay this to the user and send their answer as a follow-up in the same thread. Never auto-confirm transactions.

### Wallet Delegation (Website Only)

If Noya responds with a **delegation request**, the user must complete this on the website:

```
"To delegate your wallet, visit https://agent.noya.ai and click
'Delegate Wallet' in the chat. This is a one-time action."
```

### Safe Deployment (Website Only)

If Noya responds with a **Safe deployment request**, the user must complete this on the website:

```
"To deploy your Polymarket Safe, visit https://agent.noya.ai and click
'Deploy Safe Now'. This is free, takes ~30 seconds, and only needs to be done once."
```

## Error Handling

**Agent API (`agent-api.noya.ai`):**

| Error              | Solution                                                                     |
| ------------------ | ---------------------------------------------------------------------------- |
| `401 Unauthorized` | API key is invalid, expired, or revoked. Generate a new one at agent.noya.ai |
| `400 Bad Request`  | Missing `message` or `threadId` in request body                              |
| `429 Rate limit`   | Wait a few minutes. Limit is 15 requests per 5-minute window                 |

**Data API (`data-endpoints.noya.ai`):**

| Error             | Solution                                                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `400 Bad Request` | Missing or invalid body field — check the path's body schema in the [Data Endpoints](#data-endpoints-no-api-key) section |
| `5xx`             | Upstream provider issue (CoinGecko, DeFiLlama, etc.). Retry or fall back to a sibling endpoint                           |

## Scripts

This skill includes the following script in its directory:

| Script            | Purpose                                                                                                                            |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `noya-message.sh` | Send a message to the Noya agent and parse the streamed response. Usage: `bash {baseDir}/noya-message.sh "<message>" "<threadId>"` |

## Additional Resources

- For the complete REST API specification, see [{baseDir}/reference.md](reference.md)
