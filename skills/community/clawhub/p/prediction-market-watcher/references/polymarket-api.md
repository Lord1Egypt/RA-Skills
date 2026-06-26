# Polymarket API Reference

No auth required for read-only access.

## Gamma API (markets + metadata)
Base: `https://gamma-api.polymarket.com`

| Method | Path | Notes |
|--------|------|-------|
| GET | `/markets?active=true&limit=20` | Active markets |
| GET | `/markets?id={condition_id}` | Single market |
| GET | `/markets?tag=crypto&active=true` | Filter by tag |

## CLOB API (orderbook / prices)
Base: `https://clob.polymarket.com`

| Method | Path | Notes |
|--------|------|-------|
| GET | `/price?token_id={id}&side=buy` | Current price |
| GET | `/book?token_id={id}` | Full orderbook |
| GET | `/last-trade-price?token_id={id}` | Last trade |

## Market Object Key Fields
```
id / condition_id   — unique market ID
question            — e.g. "Will BTC close above $70k on March 31?"
active              — bool
closed              — bool
end_date_iso        — settlement date
tokens[]            — [{token_id, outcome, price}] (YES/NO tokens)
volume              — total volume USD
liquidity           — current liquidity USD
```

## Notes
- Polymarket is on Polygon blockchain — prices are USDC
- Prices are 0.0–1.0 (multiply by 100 for cents equivalent)
- Trading requires wallet + API key (write operations only)
- Good for cross-referencing Kalshi odds on same topic
