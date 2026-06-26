---
name: polymarket-edge
description: "Trade and analyse Polymarket prediction markets with a 5-minute BTC EMA crossover strategy. Browse markets, read order books, run signals, manage a live auto-trader, and view portfolio positions. Billed per-call via SkillPay.me (0.001 USDT / call, BNB Chain USDT)."
metadata:
  openclaw:
    requires:
      env:
        - SKILL_BILLING_API_KEY
        - SKILL_ID
      bins:
        - python3
        - pip
    primaryEnv: SKILL_BILLING_API_KEY
---

# Polymarket Edge

A locally-running FastAPI skill that wraps the Polymarket Gamma + CLOB APIs with
a built-in EMA(5/20) crossover strategy and SkillPay.me billing.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set required environment variables
export SKILL_BILLING_API_KEY=sk_your_skillpay_api_key_here
export SKILL_ID=polymarket-edge

# Start the skill server (port 8080)
python main.py
```

The interactive docs are available at `http://localhost:8080/docs`.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `SKILL_BILLING_API_KEY` | ✅ | From your skillpay.me dashboard |
| `SKILL_ID` | ✅ | Your skill slug, e.g. `polymarket-edge` |
| `POLYMARKET_PRIVATE_KEY` | optional | EVM private key for live order placement |

## Billing

Every billed endpoint requires `?user_id=<id>` in the query string.
If the user has no tokens the API returns **HTTP 402** with a `top_up_url`.

```
GET  /balance?user_id=alice          → current token balance
GET  /topup?user_id=alice&amount=10  → BNB Chain USDT payment link
```

1 USDT = 1 000 tokens · 1 call = 1 token · min top-up 8 USDT · SkillPay takes 5 %

## Key endpoints (all require `?user_id=`)

### Market data
```
GET /markets/search?q=bitcoin    Search all Polymarket markets
GET /markets/btc                 List active BTC/Bitcoin markets
GET /market/{id}                 Single market details
GET /market/{token_id}/book      Full order book (bids + asks)
GET /market/{token_id}/price     Mid-price, spread, implied probability
GET /market/{token_id}/history   5-min OHLCV candles
```

### Strategy signals
```
POST /signal                     Run EMA crossover on top BTC markets
                                 Returns BUY_YES / BUY_NO / HOLD / SKIP per market
```

### Auto-trader
```
GET  /autotrader/status          Is the auto-trader running?
POST /autotrader/start           Start 5-min BTC cycle (background task)
POST /autotrader/stop            Stop auto-trader
GET  /autotrader/log             Last 50 trade log entries
```

### Portfolio
```
GET /portfolio?wallet=0x...      Open positions + USD value for a wallet
```

## Strategy logic

- **Candles**: 5-minute YES-token price history from Polymarket CLOB
- **Signal**: EMA(5) crosses above EMA(20) → `BUY_YES`; crosses below → `BUY_NO`
- **Filters**: skip if spread > 0.05 or YES price outside [0.15, 0.85]
- **Live trading**: set `?auto_trade=true` on `/autotrader/start` (requires `POLYMARKET_PRIVATE_KEY` + `py-clob-client`)

## Live trading (optional)

```bash
pip install py-clob-client
export POLYMARKET_PRIVATE_KEY=0x<your_burner_wallet>
# Then uncomment the py-clob-client block in polymarket_client.py
curl -X POST "http://localhost:8080/autotrader/start?user_id=alice&auto_trade=true"
```

⚠️ Use a burner wallet. Never commit your private key.
