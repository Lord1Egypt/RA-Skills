# Kalshi API Reference

Base URL: `https://api.elections.kalshi.com/trade-api/v2`

Auth: RSA-PSS signed headers on every request:
- `KALSHI-ACCESS-KEY`: key ID
- `KALSHI-ACCESS-TIMESTAMP`: ms since epoch
- `KALSHI-ACCESS-SIGNATURE`: base64(RSA-PSS(timestamp+method+path))

## Endpoints

### Portfolio
| Method | Path | Notes |
|--------|------|-------|
| GET | `/portfolio/balance` | Returns `balance` (cents), `portfolio_value` (cents) |
| GET | `/portfolio/positions` | Returns `market_positions[]`, `event_positions[]` |
| GET | `/portfolio/fills?limit=N` | Recent order fills |

### Markets
| Method | Path | Notes |
|--------|------|-------|
| GET | `/markets` | Params: `status=open\|closed`, `limit`, `cursor` |
| GET | `/markets/{ticker}` | Single market detail |
| GET | `/events/{event_ticker}/markets` | All markets in an event |

### Orders
| Method | Path | Notes |
|--------|------|-------|
| POST | `/portfolio/orders` | Place order |
| GET | `/portfolio/orders` | List orders |
| DELETE | `/portfolio/orders/{order_id}` | Cancel order |

## Market Object Key Fields
```
ticker              — e.g. KXBTC-26MAR3117-B66875
title               — human readable
status              — active | closed | settled
close_time          — ISO8601, when betting closes (= settlement time)
floor_strike        — lower bound of range
cap_strike          — upper bound of range
yes_bid_dollars     — best bid for YES (e.g. "0.08")
yes_ask_dollars     — best ask for YES (e.g. "0.11")
no_bid_dollars      — best bid for NO
no_ask_dollars      — best ask for NO
rules_primary       — plain English settlement rules — READ THIS
result              — "yes" | "no" | "" (empty = not settled)
```

## Order Payload
```json
{
  "ticker": "KXBTC-26MAR3117-B66875",
  "action": "buy",
  "side": "yes",
  "type": "limit",
  "count": 5,
  "yes_price": 11
}
```
- `yes_price` / `no_price` in cents (integer 1–99)
- `count` = number of contracts ($1 face value each)

## Settlement Notes
- BTC markets use CF Benchmarks RTI — 60s average before close_time
- NOT the same as Coinbase/Binance/Google price
- RTI can differ by $50–200 from spot in volatile conditions
