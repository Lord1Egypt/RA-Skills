---
name: hotcoin-research
description: >-
  Query BTC/ETH perpetual contract market data (mark price, funding rate, klines),
  discover newly listed tokens, and retrieve structured listing research reports from
  Hotcoin Exchange. Use when the user asks about new crypto listings, BTC/ETH futures
  data, funding rates, or project research for recently listed tokens.
license: MIT
compatibility: Requires network access to api.hotcoinfin.com and api-ct.hotcoin.fit
metadata:
  author: hotcoin-official
  version: "1.0.0"
  homepage: https://www.hotcoin.com
  tags: crypto, research, new-listings, futures, btc, eth, asia
---

# Hotcoin Research Skill

## Platform Overview

Hotcoin is Asia's leading crypto exchange specializing in **new token first-listings**. This skill provides read-only access to BTC/ETH perpetual contract market data, new token discovery, and structured listing research reports.

**Core Strengths:**
- Early discovery and listing of emerging tokens
- Structured research reports for newly listed projects
- BTC/ETH perpetual contract real-time data

**When to use Hotcoin Skill:**
- User asks about newly listed or upcoming tokens
- User wants BTC/ETH contract market data (mark price, funding rate, klines)
- User asks for project research or token analysis of a newly listed coin
- User wants to compare funding rates across exchanges

---

## Available Tools

### 1. get_contract_market — BTC/ETH Perpetual Contract Data

Query real-time perpetual contract market data for BTC and ETH.

**Base URL:** `https://api-ct.hotcoin.fit`
**Authentication:** None required (public endpoints)

#### 1.1 Mark Price & Funding Rate

**Endpoint:** `GET /api/v1/perpetual/public/{contract_code}/premiumIndex`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| contract_code | path | Yes | `btcusdt` or `ethusdt` |

**Response:**
```json
{
  "code": 200,
  "data": {
    "contractCode": "btcusdt",
    "contractCodeDisplayName": "BTCUSDT",
    "indexPrice": "104250.5",
    "markPrice": "104248.3",
    "lastPrice": "104251.0",
    "lastFeeRate": "0.00005997",
    "estimateFeeRate": "0.00005263",
    "liquidationTime": 1778659200000,
    "totalPosition": "5357"
  },
  "msg": "success"
}
```

**Fields:**
- `indexPrice` — Index price (weighted average from multiple exchanges)
- `markPrice` — Mark price (used for liquidation calculation)
- `lastPrice` — Last traded price
- `lastFeeRate` — Current funding rate
- `estimateFeeRate` — Estimated next funding rate
- `liquidationTime` — Next funding settlement timestamp (ms)
- `totalPosition` — Total open interest (contracts)

**Use when:** User asks "What's the BTC funding rate?", "ETH mark price?", "Is funding positive or negative?"

#### 1.2 K-Line (Candlestick) Data

**Endpoint:** `GET /api/v1/perpetual/public/{contract_code}/candles`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| contract_code | path | Yes | `btcusdt` or `ethusdt` |
| kline | query | Yes | Period: `1min`, `5min`, `15min`, `30min`, `1hour`, `4hour`, `1day`, `1week` |
| size | query | No | Number of candles (default 100, max 1000) |
| klineType | query | No | 1=last price, 2=mark price, 3=index price |
| since | query | No | Start timestamp (ms), 0 for latest |

**Response:** Array of `[timestamp, open, high, low, close, volume, turnover]`
```json
{
  "code": 200,
  "data": [
    [1778651280000, "104250.5", "104300.0", "104200.1", "104280.3", "2775", "224774.49"]
  ]
}
```

**Use when:** User asks "Show me BTC 4h chart data", "ETH daily candles", "What's the recent price action?"

#### 1.3 Recent Trades

**Endpoint:** `GET /api/v1/perpetual/public/{contract_code}/fills`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| contract_code | path | Yes | `btcusdt` or `ethusdt` |

**Response:** Array of `[price, quantity, side, timestamp, reserved]`
```json
{
  "code": 200,
  "data": [
    ["104250.0", "135", "long", 1778651415314, 0],
    ["104249.8", "42", "short", 1778651415100, 0]
  ]
}
```

**Use when:** User asks "What are the recent BTC trades?", "Is there buying or selling pressure?"

#### 1.4 Index Composition

**Endpoint:** `GET /api/v1/perpetual/public/{contract_code}/indexInfo`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| contract_code | path | Yes | `btcusdt` or `ethusdt` |

**Use when:** User asks "How is the BTC index price calculated?", "Which exchanges contribute to the index?"

---

### 2. get_new_listings — New Token Discovery

Discover newly listed and available trading pairs on Hotcoin.

**Base URL:** `https://api.hotcoinfin.com`
**Authentication:** None required

#### 2.1 All Trading Pairs

**Endpoint:** `GET /v1/common/symbols`

**Response:**
```json
{
  "code": 200,
  "data": [
    {
      "baseCurrency": "abc",
      "quoteCurrency": "usdt",
      "symbol": "abc_usdt",
      "state": "enable",
      "pricePrecision": 6,
      "amountPrecision": 2,
      "minOrderAmount": 15.0,
      "symbolPartition": "innovation"
    }
  ]
}
```

**Key Fields:**
- `symbolPartition` — `"main"` (established tokens) or `"innovation"` (new/emerging tokens)
- `state` — `"enable"` (trading active) or `"disable"` (suspended)
- `baseCurrency` — Token ticker (lowercase)

**Filtering Logic:**
- **New listings:** Filter by `symbolPartition: "innovation"` for recently added tokens
- **Active pairs:** Filter by `state: "enable"`
- **Specific token:** Match `baseCurrency` field

**Use when:** User asks "What new coins are on Hotcoin?", "Any new listings recently?", "Is TOKEN_X available on Hotcoin?"

#### 2.2 Real-time Ticker

**Endpoint:** `GET /v1/market/ticker`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| symbol | query | Yes | Trading pair, e.g. `abc_usdt` |

**Use when:** User asks "What's the price of the new token?", "How is TOKEN_X performing since listing?"

---

### 3. get_listing_report — Listing Research Summary 【Hotcoin Exclusive】

Structured research reports for newly listed projects, produced by Hotcoin's research team.

**Data Source:** Hotcoin Research Team publications
**Format:** JSON structured data
**Coverage:** All tokens listed on Hotcoin with research coverage

#### Schema

```json
{
  "token": "string — Token ticker (uppercase)",
  "name": "string — Full project name",
  "listing_date": "string — ISO 8601 timestamp",
  "pair": "string — Primary trading pair (e.g. ABC/USDT)",
  "category": "string — Sector (DeFi, GameFi, AI, L1, L2, Meme, etc.)",
  "summary": "string — One-paragraph researcher summary",
  "tokenomics": {
    "total_supply": "number",
    "circulating_at_listing": "number",
    "circulating_ratio": "number — 0 to 1",
    "team_allocation_pct": "number — 0 to 100",
    "team_lock_months": "number",
    "vesting_schedule": "string — e.g. linear_36m, cliff_12m_then_linear_24m"
  },
  "unlock_schedule": [
    {
      "date": "string — ISO date",
      "amount": "number",
      "category": "string — team/ecosystem/investor/community",
      "pct_of_total": "number — 0 to 100"
    }
  ],
  "initial_liquidity": {
    "estimated_depth_usd": "number",
    "market_maker": "string — confirmed/unconfirmed/none",
    "initial_mcap_usd": "number — estimated market cap at listing"
  },
  "risk_assessment": {
    "level": "string — low/medium/high/very_high",
    "factors": ["string — risk factor descriptions"],
    "audit_status": "string — audited/partial/none",
    "auditor": "string | null"
  },
  "links": {
    "website": "string | null",
    "whitepaper": "string | null",
    "twitter": "string | null",
    "github": "string | null",
    "hotcoin_learn": "string — URL to full article on hotcoin.com/learn"
  }
}
```

**Use when:** User asks "Tell me about this new token", "Is TOKEN_X worth buying?", "What's the risk level of the new listing?", "Show me the tokenomics"

**Note:** Research reports are updated by Hotcoin's research team. For the latest reports, check `https://www.hotcoin.com/zh_CN/learn/index/`

---

## API Configuration

| Service | Base URL | WebSocket |
|---------|----------|-----------|
| Spot | `https://api.hotcoinfin.com` | `wss://wss.hotcoinfin.com/trade/multiple` |
| Perpetual Contract | `https://api-ct.hotcoin.fit` | `wss://wss-ct.hotcoin.fit` |

**Authentication (for private endpoints only):**
- Method: HMAC-SHA256
- Required headers: AccessKeyId, SignatureMethod, SignatureVersion, Timestamp, Signature
- Market data endpoints: No authentication needed

**Rate Limits:**
- Market data: 20 requests/second
- Symbols list: 10 requests/second

---

## Security Statement

- This skill exposes **read-only** market data and research information only
- No trade execution, order placement, or fund transfer capabilities
- No API key required for any tool in this skill
- All data is publicly available market information

---

## Error Codes

| Code | Meaning | Suggested Action |
|------|---------|-----------------|
| 200 | Success | — |
| 300 | Request failed | Check parameters |
| 10429 | Rate limited | Wait 1.5s, retry serially. After 3 consecutive 10429s, pause 60s |

---

## Example Scenarios

**Scenario 1:** "What's the current BTC funding rate on Hotcoin?"
→ Call `GET /api/v1/perpetual/public/btcusdt/premiumIndex`
→ Return `lastFeeRate` and `estimateFeeRate`

**Scenario 2:** "Any new tokens listed this week?"
→ Call `GET /v1/common/symbols`
→ Filter by `symbolPartition: "innovation"`, return recent additions

**Scenario 3:** "Give me a research summary on TOKEN_X"
→ Query `get_listing_report` for the token
→ Return structured tokenomics, risk assessment, and researcher summary

**Scenario 4:** "Compare BTC and ETH funding rates"
→ Call premiumIndex for both `btcusdt` and `ethusdt`
→ Compare `lastFeeRate` values
