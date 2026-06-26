---
name: Polymarket Command Center
description: "Read-only Polymarket interface — browse trending markets, get detailed odds with probability bars, search active markets, and track watchlists. Zero API key required, uses public Gamma and CLOB APIs with thread-safe caching. Part of the OpenClaw Prediction Market Trading Stack — feeds Polymarket data to Market Morning Brief and pairs with Prediction Market Arbiter for cross-platform divergence detection."
---

# Polymarket Command Center

Real-time prediction market data for OpenClaw — no API key required.

## Commands

### trending
Get top 10 active markets by trading volume across Polymarket.

```
trending
trending [category]
```

**Examples:**
- `trending` — all markets
- `trending politics` — political prediction markets
- `trending crypto` — cryptocurrency markets
- `trending sports` — sports betting markets

**Output:**
- Market question (truncated to 65 chars)
- Primary outcome probability (Yes/No split)
- 24h volume
- Days until market closes
- Market slug (for detailed lookups)

**Categories:** Gamma API supports any tag in Polymarket's taxonomy. Common: `politics`, `crypto`, `sports`, `elections`, `entertainment`, `economics`.

---

### odds [slug]
Get detailed odds for a specific market by slug or search term.

```
odds [slug]
odds [search term]
```

**Examples:**
- `odds will-trump-win-2024` — exact slug match
- `odds bitcoin` — search for markets containing "bitcoin"
- `odds fed rate cut march` — multi-term search

**Output:**
- Full market question
- Outcome probabilities with visual bar chart (█ filled, ░ empty)
- 24h trading volume
- Market liquidity
- Close date (absolute + days remaining)
- Market description (truncated to 200 chars)
- Live CLOB midpoint (if available)
- Direct link to Polymarket web interface

**Search behavior:** If exact slug fails, performs client-side text search across market questions, slugs, and descriptions.

---

### search [query]
Search across 100 active markets by text. Client-side filtering for instant results.

```
search [query]
search [term1] [term2] [term3]
```

**Examples:**
- `search bitcoin` — single term
- `search bitcoin 100k` — all terms must match
- `search fed interest rate` — multi-word search
- `search election 2024` — phrase search

**Output:**
- Up to 8 matching markets
- Question, yes probability, volume, slug for each

**Search logic:** All query terms must appear in the market question, slug, or description (case-insensitive). Searches are cached for 2 minutes.

---

### watchlist
Check odds on your configured watchlist markets.

```
watchlist
```

**Output:**
- Current odds for each market on your watchlist
- Volume, close date for each

**Configuration:** Add market slugs to `~/.openclaw/state/polymarket_watchlist.json`:

```json
{
  "slugs": [
    "will-trump-win-2024",
    "bitcoin-above-100k",
    "fed-rate-cut-march-2026"
  ]
}
```

Or via `~/.openclaw/config.yaml`:

```yaml
polymarket:
  watchlist:
    - will-trump-win-2024
    - bitcoin-above-100k
    - fed-rate-cut-march-2026
```

---

## Data Source & Architecture

### No API Key Required
Polymarket Command Center uses only public APIs:

- **Gamma API** (`https://gamma-api.polymarket.com`) — Market metadata, outcomes, pricing
- **CLOB API** (`https://clob.polymarket.com`) — Live bid/ask midpoints

Zero authentication. Zero credentials. Pure HTTP.

### Thread-Safe Caching
In-memory cache with automatic eviction:

- **TTL:** 120 seconds default (180s for trending, 120s for search)
- **Max entries:** 100 (LRU eviction when full)
- **Thread-safe:** Reentrant locks for concurrent requests
- **Smart invalidation:** Expired entries auto-deleted on next access

### CLOB Midpoints
The "Live midpoint" shown in odds details comes from CLOB (Central Limit Order Book) — Polymarket's on-chain order book. This represents the true real-time bid/ask spread. Falls back gracefully if CLOB data is unavailable.

---

## Output Formats

### Trending Markets
```
🔮 Polymarket Trending (crypto)

1. Will Bitcoin reach $100K by end of 2026?
   Yes: 72% | Vol: $2.5M | Closes: 45d
   📎 bitcoin-above-100k

2. Ethereum price above $5K on March 31 2026?
   Yes: 48% | Vol: $1.2M | Closes: 22d
   📎 ethereum-5k-march

💡 Say 'odds [slug]' for detailed odds on any market
```

### Detailed Odds
```
🔮 Will Trump win the 2024 US Presidential Election?

Yes: 68% ████████████░░░░░░░░
No:  32% ██████░░░░░░░░░░░░░░

📊 Volume: $18.5M | Liquidity: $4.2M
📅 Closes: 2026-11-05 (240 days)

📝 Prediction market for the outcome of the 2024 U.S. Presidential election...

💹 Live midpoint: 67.8%

🔗 polymarket.com/event/will-trump-win-2024
```

### Search Results
```
🔍 Polymarket search: 'bitcoin 100k'

1. Will Bitcoin reach $100K before end of 2026?
   Yes: 72% | Vol: $2.5M
   📎 bitcoin-above-100k

2. Bitcoin price prediction: $100K to $110K range by March 2026?
   Yes: 58% | Vol: $850K
   📎 bitcoin-100k-110k-range

💡 Say 'odds [slug]' for details on any market
```

### Watchlist
```
👀 Polymarket Watchlist

🔮 Will Trump win the 2024 US Presidential Election?
   Yes: 68% | Vol: $18.5M

🔮 Will Bitcoin reach $100K by end of 2026?
   Yes: 72% | Vol: $2.5M

🔮 Will Fed cut rates in March 2026?
   Yes: 64% | Vol: $3.1M
```

---

## Response Codes

| Status | Meaning | Action |
|--------|---------|--------|
| ❌ | Network error | Retry in a minute; check internet connection |
| 🔮 | Success | Market data loaded and formatted |
| 👀 | Watchlist | Your configured markets |
| 🔍 | Search | Client-side filtered results |
| 💡 | Tip | Suggested next action |

---

## Cache Behavior

- **First call:** Hits Polymarket API, caches result
- **Repeated calls (within TTL):** Returns cached data instantly
- **Stale data (past TTL):** Cache evicted, fresh API call triggered
- **Bounded memory:** Max 100 entries; oldest evicted when full
- **Thread-safe:** Safe for concurrent requests (e.g., morning brief + user query)

**Example timeline:**
```
14:30:00 - User: "trending"
           → API call → cache set (expires 14:32:00)
           → response with 10 markets

14:30:45 - User: "trending"
           → cache hit (28s old)
           → instant response (same data)

14:32:15 - User: "trending"
           → cache miss (expired 15s ago)
           → API call → cache set (expires 14:34:15)
           → response with fresh data
```

---

## Configuration (Optional)

All commands work without any configuration. Optional settings in `~/.openclaw/config.yaml`:

```yaml
polymarket:
  enabled: true
  watchlist:
    - will-trump-win-2024
    - bitcoin-above-100k
    - fed-rate-cut-march-2026
  categories:
    - politics
    - crypto
    - sports
```

**No config needed** — defaults work for all commands.

---

## Supported Market Categories

Gamma API returns markets tagged with these common categories:

- `politics` — Elections, political outcomes
- `crypto` — Bitcoin, Ethereum, altcoins, blockchain
- `sports` — NFL, NBA, Premier League, Olympic Games
- `entertainment` — Movies, award shows, celebrity news
- `economics` — Fed rates, inflation, jobs data
- `weather` — Extreme weather events
- `science` — Space, breakthrough discoveries
- `business` — Tech IPOs, M&A, earnings

Custom tags may appear; Gamma API returns whatever is configured.

---

## Implementation Details

### HTTP Client
- User-Agent: `OpenClaw-Polymarket/1.0`
- Timeout: 10 seconds per request
- Accept: `application/json`
- No cookies; stateless requests

### Error Handling
- Network timeouts → graceful "couldn't reach Polymarket"
- Malformed JSON → ignored, fallback to empty results
- Unicode decode errors → handled silently

### Outcome Parsing
Polymarket API returns outcomes and prices as JSON-stringified arrays. Command Center auto-detects format (string vs. array) and parses both.

**Binary markets:** `["Yes", "No"]` outcomes with `[yes_price, no_price]`

**Categorical markets:** `["Trump", "Harris", "RFK Jr"]` with corresponding prices.

---

## OpenClaw Ecosystem Integration

Read-only Polymarket data layer for the Prediction Market Trading Stack.

| Connected Skill | How It Connects |
|----------------|-----------------|
| **Market Morning Brief** | Polymarket trending data appears in your daily brief |
| **Prediction Market Arbiter** | Polymarket prices compared against Kalshi for divergences |
| **Xpulse** | Social signals correlated with Polymarket movements |

**Install the complete stack:**
```bash
clawhub install kalshalyst kalshi-command-center polymarket-command-center prediction-market-arbiter xpulse portfolio-drift-monitor market-morning-brief personality-engine
```

---

## Example Workflows

### Monitor Crypto Market Sentiment
```
1. trending crypto        # See top crypto markets by volume
2. odds bitcoin-above-100k  # Detailed probability for BTC
3. search ethereum        # Find Ethereum-related markets
4. watchlist             # Check your configured positions
```

### Track Election Predictions
```
1. trending politics     # Top political markets
2. odds will-trump-win-2024  # Detailed odds + CLOB midpoint
3. search harris         # Look for related markets
4. Add to watchlist      # Monitor probability shifts
```

### Find Hidden Opportunities
```
1. trending               # All markets
2. search [niche term]   # Find underexplored markets
3. odds [slug]           # Check volumes and liquidity
4. Compare CLOB midpoint vs. displayed probability
```

---

## Limitations & Notes

- **Read-only:** No trading, no account creation
- **Public data only:** No private market insights
- **Gamma API limits:** ~100 markets per request (used in search)
- **CLOB midpoints:** May be unavailable for some markets (graceful fallback)
- **Pricing:** Outcomes always shown as decimal probabilities (0.68 = 68%)
- **Closed markets:** Excluded from trending/search; archived on Polymarket

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Couldn't reach Polymarket" | Retry in 1 minute; check internet |
| "No markets found for..." | Try broader search term; check spelling |
| "No watchlist configured" | Add watchlist to config.yaml or create ~/.openclaw/state/polymarket_watchlist.json |
| Cached data looks stale | Cache TTL is 2 minutes; wait or restart service |
| CLOB midpoint missing | Market may not have CLOB tokens yet (new markets) |

---

## Version History

**v1.0.0** (2026-03-09)
- Initial release
- Commands: trending, odds, search, watchlist
- Thread-safe caching with 120s TTL
- CLOB midpoint integration
- Zero API key required
- 100% read-only (no trading)


---

## Feedback & Issues

Found a bug? Have a feature request? Want to share results?

- **GitHub Issues**: [github.com/kingmadellc/openclaw-prediction-stack/issues](https://github.com/kingmadellc/openclaw-prediction-stack/issues)
- **X/Twitter**: [@KingMadeLLC](https://x.com/KingMadeLLC)

Part of the **OpenClaw Prediction Stack** — the first prediction market skill suite on ClawHub.
