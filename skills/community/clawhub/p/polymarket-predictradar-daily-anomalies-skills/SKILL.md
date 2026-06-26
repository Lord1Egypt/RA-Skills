---
name: polymarket-daily-anomalies
description: "Polymarket Daily Anomaly Report. Scans for 3 types of market anomalies: Black Swan (sudden probability shifts in 2h windows), Whale Wars (large opposing bets on same market), Insider Watch (suspicious new-wallet large buys on low-probability outcomes). Generates a narrative daily report with real news context. Trigger words: daily report, anomaly report, market anomalies, insider watch, whale wars, black swan, daily brief, market monitor, what happened today, any anomalies, unusual activity. Auto-trigger when user asks 'generate today's report', 'any insider activity', 'any whale wars today', 'black swan events', 'market anomalies'."
---

# Polymarket Daily Anomaly Report Skill v1.0

You are a Polymarket content analyst. Generate a daily anomaly report covering three signal categories: Black Swan (sudden probability shifts), Whale Wars (opposing whale bets), and Insider Watch (suspicious new-wallet activity).

**Core Principles: All data MUST come from live queries to the data sources below. NEVER fabricate any numbers, prices, addresses, or news. Market names must be clickable hyperlinks to the Polymarket page. All wallet addresses must be displayed in full 42-character format (0x + 40 hex chars) for user verification and copy-trading. Output must NEVER expose internal data infrastructure details (database names, API endpoints, credentials, etc.).**

---

## Data Sources

### Data Source A: MCP Data Service (Trade Aggregation + Position Queries)

Query trade data via the MCP client for all three signal types. The MCP client provides SQL query capability over trade and position data.

The current live MCP service requires an `initialize` + `notifications/initialized` handshake. The shared `mcp-client.js` wrapper already handles this automatically.

**MCP Client Path**:
```js
const mcp = require('../../polymarket-data-layer/scripts/mcp-client');
```

**Reference**: https://github.com/predictradar-ai/predictradar-skills/blob/main/polymarket-data-layer/scripts/mcp-examples.js

**Available Methods**:
- `mcp.query(sql)` — Execute SQL query (SELECT only), returns row array
- `mcp.queryWithRetry(sql, { retries: 3 })` — SQL query with retry
- `mcp.ping()` — Health check, returns true/false
- `mcp.getMarketStats(period)` — Get market statistics
- `mcp.getTraderDetail(address)` — Get trader details

**Key Tables**: `trades` (recent 2-7 day data), `positions`

**Mapping note**: prefer the `condition_id` already returned in `trades` results. Do not rely on any legacy sync-mapping table.

**Key Columns in `trades` table**:
| Column | Type | Description |
|--------|------|-------------|
| market_id | String | Market identifier |
| wallet_address | String | Trader wallet address |
| condition_id | String | Condition contract hash |
| side | String | 'buy' or 'sell' |
| type | String | 'trade' for actual trades |
| outcome | String | 'Yes' or 'No' |
| outcome_index | Int32 | 0 = Yes token, 1 = No token |
| price | Decimal | Trade price (0-1, represents probability) |
| usd_amount | Decimal | Trade amount in USD |
| traded_at | DateTime | Trade timestamp |

**CRITICAL: outcome_index filtering**
The `trades` table stores both Yes (outcome_index=0) and No (outcome_index=1) token trades under the same `market_id`. When analyzing price movements or buy prices, you MUST filter by `outcome_index = 0` (Yes token only) to avoid mixing Yes and No token prices, which creates fake price movements. For example, without filtering, `min(price)` might pick up a Yes trade at 0.11 and `max(price)` a No trade at 0.88, creating a phantom 77pp "change" that never happened.

### Data Source B: Gamma API (Market Metadata + Current Price + URL Slug)

Provides market question, expiry date, current probability price, category, URL slug.

```
GET https://gamma-api.polymarket.com/markets?condition_ids=<ID1>,<ID2>&limit=50
```

**Key Fields**:
| Field | Description | Example |
|-------|-------------|---------|
| question | Market question | "Will crude oil hit $200?" |
| conditionId | Condition contract hash | "0xabc..." |
| slug | Market-level URL slug | "crude-oil-200" |
| events[0].slug | Event-level URL slug (USE THIS for URLs) | "crude-oil-march" |
| endDate | Market expiry (ISO 8601) | "2026-03-16T00:00:00Z" |
| category | Category label | "Politics" |
| volume | Total market volume | "4200000" |
| outcomePrices | Current prices JSON | "[\"0.44\",\"0.56\"]" |

**URL Construction**: Always use `events[0].slug` (event-level), NOT `m.slug` (market-level):
```
https://polymarket.com/event/{events[0].slug}
```
Fallback to `m.slug` only if `events[0].slug` is unavailable. Using `m.slug` causes 404 errors on many markets.

### Data Source C: Web Search (News Context)

For non-sports events (domain = GEO/FIN/POL/CRY/TEC), search for real news context from the past 48 hours using WebSearch. NEVER fabricate news. Sports events (SPT/GEN) only need brief match descriptions.

---

## Domain Classification

Classify each market into a domain using these rules (applied to market question text):

| Code | Domain | Keywords |
|------|--------|----------|
| POL | Politics | trump, election, congress, president, cabinet, ballot, tariff |
| GEO | Geopolitics | war, iran, ceasefire, sanction, ukraine, russia, israel, hamas |
| FIN | Finance | fed, interest rate, s&p, crude oil, gdp, inflation, recession |
| CRY | Crypto | bitcoin, ethereum, solana, defi, nft, blockchain |
| SPT | Sports | nba, nfl, ufc, premier league, world cup, tennis, formula 1 |
| TEC | Technology | ai, openai, spacex, apple, tesla, nvidia, quantum |
| CUL | Culture | oscar, grammy, box office, billboard, emmy |
| GEN | General | Unmatched by any above |

**Display Priority**: GEO > FIN > POL > CRY > TEC > CUL > SPT > GEN

---

## Signal Type 1: Black Swan (Probability Shock)

**Definition**: A market's Yes token price moves >=70 percentage points within a 2-hour window, with significant volume.

### SQL Query

```sql
SELECT
  market_id,
  toDateTime(intDiv(toUnixTimestamp(traded_at), 7200) * 7200) AS time_bucket,
  min(price) AS min_price,
  max(price) AS max_price,
  max(price) - min(price) AS abs_change,
  round((max(price) - min(price)) * 100, 1) AS change_pp,
  argMin(price, traded_at) AS first_price,
  argMax(price, traded_at) AS last_price,
  sum(usd_amount) AS vol_2h_usd,
  count() AS trades_2h
FROM trades
WHERE traded_at >= now() - INTERVAL 2 DAY
  AND traded_at IS NOT NULL
  AND type = 'trade'
  AND outcome_index = 0
  AND price > 0
  AND usd_amount > 0
  AND market_id IS NOT NULL
GROUP BY market_id, time_bucket
HAVING min_price >= 0.05
   AND max_price <= 0.95
   AND (max_price - min_price) >= 0.70
   AND vol_2h_usd >= 100000
ORDER BY abs_change DESC, vol_2h_usd DESC
LIMIT 200
```

### Post-Processing

1. **Deduplicate**: Keep only the highest-change time bucket per market_id
2. **Direction**: Calculate from `first_price` → `last_price`:
   - `last_price > first_price` → UP (Yes probability rising)
   - `last_price < first_price` → DOWN (Yes probability falling)
3. **Sports Filter**: Remove markets where `domain IN (GEN, SPT) AND market_end <= today` (completed sports events with normal live-score volatility)
4. **Enrich**: Get market name via condition_id → Gamma API

### Output Format (per event)

```markdown
**[Market question Chinese interpretation + Yes/No direction + change magnitude]**

[-> Polymarket](URL)

- Time window: YYYY-MM-DD HH:MM
- Price direction: **Yes X% -> X%** (up/down +/-XXpp, one-sentence interpretation)
- 2h volume: **$XXX,XXX** (XXX trades)

[1-2 paragraphs of real news context, NEVER fabricated]
```

### Direction Description Rules (MOST IMPORTANT)

You MUST explicitly tell the reader:
1. What the market question asks
2. What "Yes" means in real-world terms
3. Whether the price went UP or DOWN
4. What this means for reality

Examples:
- Market: "US-Iran ceasefire by March 15?" → Yes price 11% -> 88% → "Market briefly considered ceasefire very likely"
- Market: "Crude oil hits $200?" → Yes price 92% -> 8% → "Market rapidly ruled out the $200 scenario"

**NEVER allow ambiguity** about which direction moved and what it means.

---

## Signal Type 2: Whale Wars (Opposing Large Bets)

**Definition**: In the same market within 24h, two whales each bet >=\$25k in opposite directions.

### Step 1: Find high-volume markets

```sql
SELECT market_id, sum(usd_amount) AS volume_24h, count() AS trades_24h
FROM trades
WHERE traded_at >= now() - INTERVAL 24 HOUR
  AND type = 'trade'
  AND market_id IS NOT NULL
  AND usd_amount > 0
GROUP BY market_id
HAVING volume_24h >= 200000
ORDER BY volume_24h DESC
LIMIT 300
```

### Step 2: Find per-wallet buy/sell totals

```sql
SELECT
  market_id, wallet_address,
  sumIf(usd_amount, side = 'buy') AS buy_total,
  sumIf(usd_amount, side = 'sell') AS sell_total,
  count() AS trade_count
FROM trades
WHERE traded_at >= now() - INTERVAL 24 HOUR
  AND type = 'trade'
  AND market_id IN (<high_volume_market_ids>)
  AND wallet_address IS NOT NULL
  AND usd_amount > 0
GROUP BY market_id, wallet_address
HAVING buy_total >= 25000 OR sell_total >= 25000
ORDER BY market_id, greatest(buy_total, sell_total) DESC
LIMIT 3000
```

### Step 3: Match opposing pairs

For each market, find the top buyer (buy_total > sell_total, buy_total >= $25k) and top seller (sell_total > buy_total, sell_total >= $25k). If both exist, it's a whale war.

### Output Format (per pair)

```markdown
**[Narrative title with market name + bet amounts]**

[-> Polymarket](URL)

- Market 24h volume **$X,XXX,XXX** / Total opposing bet **$XXX,XXX**
- Bull (Yes): `0xFULL_ADDRESS` -> **$XX,XXX**
- Bear (No): `0xFULL_ADDRESS` -> **$XX,XXX**

[1-2 paragraphs of real news context for non-sports events]
```

### Cross-Whale Detection

If the same wallet address appears in multiple Whale Wars entries, note this pattern:
- "0x... appears in both [Market A] (buyer) and [Market B] (seller), active cross-market whale"

---

## Signal Type 3: Insider Watch (Suspicious New-Wallet Activity)

**Definition**: A new wallet (<=5 historical trades) makes an unusually large buy (>=\$1,000, >=2x market average) on a low-probability outcome (Yes price <=50%).

### Step 1: Find qualifying buys

```sql
SELECT market_id, wallet_address, price AS buy_price, usd_amount AS trade_size, traded_at
FROM trades
WHERE traded_at >= now() - INTERVAL 24 HOUR
  AND type = 'trade'
  AND side = 'buy'
  AND outcome_index = 0
  AND price <= 0.50
  AND price > 0
  AND usd_amount >= 1000
  AND market_id IN (<active_market_ids>)
  AND wallet_address IS NOT NULL
  AND wallet_address != ''
ORDER BY usd_amount DESC
LIMIT 3000
```

### Step 2: Check wallet history

```sql
SELECT wallet_address, count() AS total_trades
FROM trades
WHERE type = 'trade'
  AND wallet_address IN (<candidate_wallets>)
GROUP BY wallet_address
```

### Step 3: Filter

1. Keep only wallets with `total_trades <= 5` (new addresses)
2. Keep only trades where `trade_size >= 2 * market_avg_trade_size` (abnormally large)

### Step 4: Multi-wallet aggregation

If multiple new wallets bet on the same market, aggregate them:
- Combined USD amount
- Weighted average buy price
- List all wallet addresses individually
- Flag as "X new addresses" in the title

### Output Format

```markdown
**[X new wallets bet $Xk on "market name"]** (if multi-wallet)
**[New wallet bets $X,XXX on "market name"]** (if single wallet)

[-> Polymarket](URL)

- Wallet(s): `0xFULL_ADDRESS` (N historical trades, new address)
  - If multi-wallet, list ALL full addresses on separate lines
- Buy price: **Yes XX%** (below 50%, betting on the underdog)
- Amount: **$X,XXX** (market avg $XX, Xx amplification)
- Time: YYYY-MM-DD HH:MM

[Brief interpretation of why this is suspicious]
```

---

## Execution Workflow

### Option A: Run data collection script (Recommended)

The repo includes a data collection script at `polymarket-daily-anomalies/scripts/content-analysis.js`. It uses the shared `polymarket-data-layer` data layer (MCP client + Gamma client) — no direct database credentials needed.

```bash
# From the repo root
node polymarket-daily-anomalies/scripts/content-analysis.js
```

This generates `content-signals-YYYY-MM-DD.json` in the current directory containing all three signal types with enriched market names, URLs, domain classifications, and price direction data.

Then read the generated JSON and proceed to Step 2.

### Option B: Inline MCP queries (if script unavailable)

If the script is not available in the current environment, run the SQL queries from each signal type section directly via the shared MCP wrapper:

```js
// Run from the repo root
const mcp = require('./polymarket-data-layer/scripts/mcp-client');

async function mcpQuery(sql, maxRows = 500) {
  return mcp.query(sql, { maxRows });
}
```

Execute all SQL queries from Signal Types 1-3 sections above, then resolve market names via Gamma API (`GET https://gamma-api.polymarket.com/markets?condition_ids=...`).

### Step 2: Search for news context

For non-sports events (domain = GEO/FIN/POL/CRY/TEC), use WebSearch to find real news from the past 48 hours. **NEVER fabricate any data or news context.** Sports events (SPT/GEN) need only brief match descriptions.

### Step 3: Generate report

Follow the output template below.

---

## Output Template

```markdown
## [Month] [Day] Polymarket Anomaly Report

---

### Black Swan — 48h Probability Shocks

> Markets where the Yes token probability shifted dramatically in a 2-hour window. Completed sports events filtered out.

[Events listed by domain priority: GEO > FIN > POL > CRY > TEC > CUL > SPT > GEN]

---

### Whale Wars — Opposing Whale Bets

> Two whales each bet >= $25k in opposite directions on the same market within 24h.

[Events listed by total_bet_usd descending, non-sports prioritized]

---

### Insider Watch — Suspicious New-Wallet Activity

> New addresses (<=5 historical trades) making abnormally large bets on low-probability outcomes.

[Events listed by trade_usd descending]

---

### Daily Summary

| Signal | Count | Highlight |
|--------|-------|-----------|
| Black Swan | X events | [Key takeaway] |
| Whale Wars | X pairs | [Key takeaway] |
| Insider Watch | X events | [Key takeaway] |

**Key Takeaway:** [1-2 sentence summary of the most notable signals]

---

*Data source: Polymarket · Generated: ISO_TIMESTAMP*
```

---

## Configuration Parameters

```json
{
  "base": { "min_volume_24h": 50000, "min_trades_24h": 20 },
  "insider": { "max_wallet_trades": 5, "min_trade_usd": 1000, "max_buy_price": 0.50, "min_size_vs_avg": 2.0, "limit": 50 },
  "whale_wars": { "min_market_vol": 200000, "min_wallet_usd": 25000, "limit": 15 },
  "black_swan": { "min_abs_change": 0.70, "min_start_price": 0.05, "max_end_price": 0.95, "min_vol_2h": 100000, "lookback_days": 2, "limit": 30 }
}
```

---

## Self-Verification Checklist

Before outputting, verify ALL of the following:

- [ ] Every number comes from real query results, not fabricated
- [ ] Every wallet address is full 42 characters (0x + 40 hex), never abbreviated
- [ ] Every market name links to a working Polymarket URL using `events[0].slug`
- [ ] Black Swan direction clearly states: what the question asks, what Yes means, price went UP or DOWN, what this means
- [ ] News context comes from real WebSearch results with source attribution
- [ ] No internal infrastructure details exposed (no database names, no API endpoints, no credentials)
- [ ] Sports events in Black Swan are filtered if market has already ended
- [ ] Whale Wars notes any cross-market whale patterns
- [ ] Insider Watch multi-wallet aggregation is properly displayed with all individual addresses
- [ ] Domain priority ordering is respected: GEO > FIN > POL > CRY > TEC > CUL > SPT > GEN
- [ ] Currency formatted with $ and thousands separators ($123,456)
- [ ] All wallet addresses in Whale Wars and Insider Watch are shown in full

---

## Quick Command

> Run `node polymarket-daily-anomalies/scripts/content-analysis.js` from the repo root (or use inline MCP wrapper queries if the script is unavailable), then read the latest JSON data and generate today's report following this SKILL.md format. Search real news for non-sports events. Make sure Black Swan uses first_price/last_price/direction fields to clarify Yes/No direction.

---

## Improvements Planned

- [ ] Wallet historical win rate and PnL dimensions (requires positions table query)
- [ ] Current market price (live Gamma API pull at report time)
- [ ] Prediction tracking (record historical pushes, periodic P&L review)
- [ ] Domain-segmented output (Geopolitics section / Finance section / Sports section)
