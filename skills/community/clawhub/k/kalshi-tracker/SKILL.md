---
name: kalshi-tracker
description: "Track Kalshi event contract prices, order book depth, and recent trades. Covers sports, politics, economics, and weather markets. Converts contract prices to American odds for cross-platform comparison. Read-only — no trade execution."
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["curl", "jq"]
    credentials:
      - id: "kalshi-api-key"
        name: "Kalshi API Key"
        description: "API key from your Kalshi account at https://kalshi.com/"
        env: "KALSHI_API_KEY"
---

# Kalshi Event Contract Tracker

Monitor Kalshi prediction market contracts — prices, order books, and trade history.

## When to Use

Use this skill when the user asks about:
- Kalshi market prices or event contracts
- Prediction market odds for sports, politics, economics, or weather
- Order book depth or liquidity on Kalshi
- Converting Kalshi contract prices to American odds
- Recent trades or volume on a Kalshi market
- Comparing Kalshi prices against sportsbook odds

## Event Categories

Common Kalshi event categories:

| Category | Series Prefix | Examples |
|----------|--------------|----------|
| Sports | SPORTS- | NBA winners, NFL spreads, World Cup |
| Politics | POL- | Elections, policy decisions |
| Economics | ECON-, FED- | GDP, inflation, Fed rate decisions |
| Weather | WEATHER- | Temperature records, hurricane landfalls |
| Finance | FINANCE- | Stock prices, crypto prices |
| Entertainment | ENT- | Award show winners, box office |

## Operations

### 1. List Active Events

Browse events with optional category filtering:

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/events?status=open&limit=50" \
  -H "Authorization: Bearer $KALSHI_API_KEY" \
  | jq '[.events[] | {
    ticker: .event_ticker,
    title: .title,
    category: .category,
    markets_count: (.markets | length),
    volume: .volume
  }] | sort_by(-.volume) | .[:20]'
```

To filter by category (e.g., sports):

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/events?status=open&limit=50&series_ticker=SPORTS" \
  -H "Authorization: Bearer $KALSHI_API_KEY" \
  | jq '[.events[] | {
    ticker: .event_ticker,
    title: .title,
    markets_count: (.markets | length),
    volume: .volume,
    close_time: .close_time
  }] | sort_by(-.volume)'
```

### 2. Get Contract Prices

Fetch current Yes/No prices, volume, and status for a specific event's markets. Replace EVENT_TICKER with the event ticker from operation 1:

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/events/EVENT_TICKER" \
  -H "Authorization: Bearer $KALSHI_API_KEY" \
  | jq '{
    event: .event.title,
    category: .event.category,
    markets: [.event.markets[] | {
      ticker: .ticker,
      subtitle: .subtitle,
      yes_price: (.yes_bid // "no bid"),
      no_price: (.no_bid // "no bid"),
      yes_ask: (.yes_ask // "no ask"),
      no_ask: (.no_ask // "no ask"),
      last_price: .last_price,
      volume: .volume,
      open_interest: .open_interest,
      status: .status,
      close_time: .close_time
    }]
  }'
```

### 3. Convert Contract Prices to American Odds

After fetching prices, convert to American odds for sportsbook comparison:

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/events/EVENT_TICKER" \
  -H "Authorization: Bearer $KALSHI_API_KEY" \
  | jq -r '.event.markets[] | "\(.subtitle)\t\(.last_price)"' \
  | python3 -c "
import sys
for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue
    name, price_str = parts
    try:
        price = float(price_str) / 100
    except (ValueError, TypeError):
        print(f'{name}: no price available')
        continue
    if price <= 0 or price >= 1:
        print(f'{name}: {price_str}c (off the board)')
    elif price > 0.5:
        odds = -(price / (1 - price)) * 100
        print(f'{name}: {price_str}c → {int(odds):+d} (implied {price:.1%})')
    elif price < 0.5:
        odds = ((1 - price) / price) * 100
        print(f'{name}: {price_str}c → +{int(odds)} (implied {price:.1%})')
    else:
        print(f'{name}: {price_str}c → +100/-100 (implied 50.0%)')
"
```

### 4. Check Order Book Depth

View resting orders to assess liquidity for a specific market. Replace MARKET_TICKER with the market ticker from operation 2:

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/markets/MARKET_TICKER/orderbook" \
  -H "Authorization: Bearer $KALSHI_API_KEY" \
  | jq '{
    ticker: .ticker,
    yes_orders: [.orderbook.yes[]? | "price: \(.[0])c  qty: \(.[1])"],
    no_orders: [.orderbook.no[]? | "price: \(.[0])c  qty: \(.[1])"],
    spread: ((.orderbook.yes[0]?[0] // 0) + (.orderbook.no[0]?[0] // 0) - 100),
    depth_yes_top3: ([.orderbook.yes[:3]?[]?[1]] | add // 0),
    depth_no_top3: ([.orderbook.no[:3]?[]?[1]] | add // 0)
  }'
```

### 5. Fetch Recent Trades

See the last trades executed on a market for momentum and volume analysis:

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/markets/MARKET_TICKER/trades?limit=20" \
  -H "Authorization: Bearer $KALSHI_API_KEY" \
  | jq '[.trades[] | {
    time: .created_time,
    price: .yes_price,
    count: .count,
    taker_side: .taker_side
  }]'
```

## Output Rules

1. Always show the event title, market subtitle, and contract ticker
2. Show contract prices in cents (e.g., 45c for $0.45)
3. When showing American odds conversion, include both the cent price and the converted odds
4. For order books, report the bid/ask spread and top-3 depth on each side
5. Flag markets with fewer than 5 contracts of top-of-book depth as "thin liquidity"
6. Flag markets with bid/ask spread > 10c as "wide spread — use limit orders"
7. Always show volume and open interest for context
8. Note the market close time so the agent knows time-to-expiry

## Error Handling

- If KALSHI_API_KEY is not set, tell the user to create a Kalshi account at https://kalshi.com/ and generate an API key
- If the API returns 401, the API key may be expired — suggest regenerating it
- If an event ticker returns empty markets, the event may have settled or been delisted
- If rate limited (429), wait 60 seconds before retrying
- If order book is empty, the market may be halted or near expiry

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-kalshi-tracker-skill/](https://agentbets.ai/guides/openclaw-kalshi-tracker-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
