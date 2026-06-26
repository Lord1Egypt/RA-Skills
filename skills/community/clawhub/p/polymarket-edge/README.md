# Polymarket Edge

An OpenClaw skill that lets any AI agent browse Polymarket prediction markets, run a 5-minute BTC EMA crossover strategy, and optionally place live trades — with every API call billed via **SkillPay.me** (0.001 USDT / call).

> **Polymarket Edge** gives your agent a systematic, always-on trading edge on prediction markets — no manual research, no babysitting.

---

## Quick Start

```bash
cd polymarket-edge
cp .env.example .env          # edit SKILL_BILLING_API_KEY if needed
pip install -r requirements.txt
python main.py                # starts on http://localhost:8080
```

Open `http://localhost:8080/docs` for the interactive Swagger UI.

---

## Billing model

| Item | Value |
|------|-------|
| Platform | SkillPay.me (BNB Chain USDT) |
| Rate | 1 token per call |
| Token price | 1 USDT = 1000 tokens |
| Minimum top-up | 8 USDT |
| Withdrawal fee | 5% |

Every billed endpoint requires `?user_id=<your_id>`. If tokens run out the API returns `HTTP 402` with a `top_up_url`.

```
GET /balance?user_id=alice          → { balance: 3200, usdt_equivalent: 3.2 }
GET /topup?user_id=alice&amount=10  → { payment_url: "https://..." }
```

---

## Endpoints

### Free
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/balance` | Token balance |
| GET | `/topup` | Get USDT top-up link |

### Billed (1 token each)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/markets/search?q=bitcoin` | Search all markets |
| GET | `/markets/btc` | List active BTC markets |
| GET | `/market/{id}` | Single market details |
| GET | `/market/{token_id}/book` | Full order book |
| GET | `/market/{token_id}/price` | Mid-price + spread |
| GET | `/market/{token_id}/history` | 5-min OHLCV candles |
| POST | `/signal` | Run EMA crossover on BTC markets |
| GET | `/autotrader/status` | Is auto-trader running? |
| POST | `/autotrader/start` | Start 5-min BTC cycle |
| POST | `/autotrader/stop` | Stop auto-trader |
| GET | `/autotrader/log` | Last 50 trade log entries |
| GET | `/portfolio` | Open positions for a wallet |

---

## Strategy

Candle interval: **5 minutes**  
Signal: **EMA(5) / EMA(20) crossover** on the YES-token price

| Condition | Action |
|-----------|--------|
| EMA(5) crosses above EMA(20) | `BUY_YES` |
| EMA(5) crosses below EMA(20) | `BUY_NO` |
| No crossover | `HOLD` |
| Spread > 0.05 | `SKIP` (illiquid) |
| YES price < 0.15 or > 0.85 | `SKIP` (extreme) |

### Signal-only mode (default)
```bash
curl "http://localhost:8080/signal?user_id=alice"
```
Returns signals without placing any orders.

### Live trading mode
```bash
# 1. Set your wallet key
export POLYMARKET_PRIVATE_KEY=0x...

# 2. Install py-clob-client
pip install py-clob-client

# 3. Uncomment place_limit_order impl in polymarket_client.py

# 4. Start with auto_trade=true
curl -X POST "http://localhost:8080/autotrader/start?user_id=alice&auto_trade=true"
```

> ⚠️ Only use a burner wallet. Never commit your private key.

---

## Live trading integration (py-clob-client)

Replace the stub in `polymarket_client.py → place_limit_order()`:

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType

async def place_limit_order(token_id, side, price, size, order_type="GTC"):
    client = ClobClient(
        host="https://clob.polymarket.com",
        key=_PRIVATE_KEY,
        chain_id=137,           # Polygon mainnet
    )
    client.create_api_key()     # derive L2 credentials
    resp = client.create_and_post_order(
        OrderArgs(
            token_id=token_id,
            price=price,
            size=size,
            side=side,          # "BUY" / "SELL"
        )
    )
    return PlacedOrder(
        order_id=resp.orderID,
        status=resp.status,
        success=resp.success,
        error_msg=None,
    )
```

---

## Deploying to ClawHub

1. Push this folder to a public GitHub repo.
2. Register the skill at `clawhub.io` — point it at `main.py`.
3. Set env vars `SKILL_BILLING_API_KEY` and `SKILL_ID` in the ClawHub dashboard.
4. Users install the skill; SkillPay handles all payment collection.
5. Watch your balance grow at `skillpay.me/dashboard`. Withdraw anytime (5% fee, BNB Chain USDT).

---

## File structure

```
polymarket-edge/
├── main.py               FastAPI app — all routes
├── billing.py            SkillPay SDK (charge / balance / payment-link)
├── polymarket_client.py  Polymarket Gamma + CLOB REST wrappers
├── strategy.py           EMA crossover strategy + auto-trader loop
├── requirements.txt
├── .env.example
└── README.md
```
