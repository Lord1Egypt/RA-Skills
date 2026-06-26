---
name: polymarket-prediction-trades
description: >
  Real-time streaming Polymarket prediction trades on Polygon (matic) with live USD pricing.
  Subscribe to a live stream of Polymarket prediction market trades over WebSocket: outcome trades
  (buyer, seller, amount, collateral in USD, price, order ID), market metadata (question title,
  resolution source, outcome labels), and transaction details — streamed in real time from the
  Bitquery GraphQL API. Covers all Polymarket markets including sports odds, Bitcoin Up or Down
  (and other crypto up/down markets), and general prediction markets.
requires:
  env:
    - name: BITQUERY_API_KEY
      required: true
      description: Your Bitquery API token (required for WebSocket connection)
---

# Polymarket Prediction Trades — real-time streaming on Polygon

This skill gives you a **real-time streaming Polymarket prediction trade feed** over WebSocket on **Polygon (matic)**. Every event is a **successful prediction trade** with outcome token amounts, collateral in USD, price in USD, buyer/seller addresses, market question, outcome label (e.g. "Up" / "Down"), and transaction hash.

Trades are filtered to `TransactionStatus.Success: true`. The stream uses Bitquery's `EVM.PredictionTrades` subscription so downstream code can build dashboards, track order flow, or monitor specific markets.

**Official docs:** [Polymarket API — Get Prices, Trades & Market Data](https://docs.bitquery.io/docs/examples/polymarket-api/) (Bitquery).

---

## What to consider before installing

This skill's code implements the described Polymarket stream and contacts only Bitquery. Before installing:

1. **Required credential**: This skill requires `BITQUERY_API_KEY` (your Bitquery API token). The registry metadata **must** declare this credential so installers are prompted to provide it. Verify the registry entry lists `BITQUERY_API_KEY` as a required environment variable.

2. **⚠️ Critical security risk — Token in WebSocket URL**: Bitquery's API does **not** support header-based auth or any method other than embedding the token in the WebSocket URL as `?token=...`. This is an **inherent design limitation** of the API, not a bug in this skill. However, it creates a **significant leakage risk**:
   - The token will **always** be present in the connection URL in memory and in any logs or captured network traffic
   - If the URL is printed, logged, captured in shell history, IDE history, proxy logs, firewall logs, or monitoring systems, the token is **exposed**
   - Once exposed, anyone with the token can impersonate your account and consume your quota
   - **Mitigation**: Store the key **only** in a secure environment variable; never print or log the full URL; rotate the key **immediately** if you suspect exposure; run in a sandboxed environment (virtualenv/container) to limit logging surface

3. **Sandbox first**: Before using this skill in production or in shared environments, test it in an isolated environment (virtualenv, container, or dedicated machine) to confirm the logging behavior and ensure the URL is not captured by system monitoring or logging tools you have enabled.

4. **Source and publisher**: Verify the publisher's identity and source control access. Review the code in `scripts/stream_polymarket.py` to confirm the script does not log the full URL before use.

---

## Security Checklist

**Before running this skill, confirm:**

- [ ] You have set `BITQUERY_API_KEY` in your environment: `export BITQUERY_API_KEY=your_token_here`
- [ ] You are running in a **sandboxed or isolated environment** (virtualenv, Docker, or dedicated machine)
- [ ] **Logging and shell history are disabled or monitored** to prevent URL capture: check `HISTFILE`, `.bash_history`, system logs, IDE debug output
- [ ] You understand that the WebSocket URL will contain your API token in plaintext in memory
- [ ] You have a plan to rotate your key if it is ever exposed
- [ ] You will **not** print, log, or commit the full URL to any file or logging system

If any of these cannot be confirmed, do not proceed with this skill until those conditions are met.

---

## Prerequisites

- **Environment**: `BITQUERY_API_KEY` — your Bitquery API token (required).

**⚠️ URL-only authentication (Bitquery API limitation):** Bitquery's streaming endpoint accepts the token **only in the WebSocket URL** as a query parameter (`?token=...`). It does **not** support header-based auth or Bearer tokens. This design choice means:
  - The token is embedded in the connection URL and will be present in memory, network traces, and any logs that capture the full URL
  - **Never print, log, or emit the full WebSocket URL in any context**
  - Always construct the URL from the environment variable and pass it only to the WebSocket transport
  - If the URL appears in shell history, logs, IDE debugger, or network monitoring, the token is compromised
  - **Rotate your API key immediately** if you suspect it was logged or captured
  - Run this script only in controlled environments where logging and monitoring are configured securely

- **Runtime**: Python 3.8+ and `pip`. Install the dependency: `pip install 'gql[websockets]'`.

---

## Trader Use Cases

These are the key reasons a trader would use this feed:

**1. Order flow / market activity**
Monitor every filled order: buyer, seller, collateral in USD, price in USD, and outcome (Yes/No or Up/Down). Identify which markets are most active and which side (buy vs sell) is dominant.

**2. Whale / large-trade detection**
Filter by `CollateralAmountInUSD` or `Amount` to surface large prediction-market trades. Useful for following smart-money flow into specific outcomes.

**3. Market-specific monitoring**
Use `Question.MarketId`, `Question.Title`, or `Question.Id` to filter the stream to a single market (e.g. "Ethereum Up or Down - March 10") and track all trades for that market in real time.

**4. Outcome imbalance**
Aggregate trades by `Outcome.Label` (e.g. "Up" vs "Down") and `IsOutcomeBuy` to see net buying pressure per outcome — useful for sentiment or momentum.

**5. Resolution source / data markets**
Use `Question.ResolutionSource` and `Question.Title` to focus on data or oracle-driven markets (e.g. Chainlink streams) and monitor trading around resolution.

**6. Entry / exit timing**
Stream `PriceInUSD` and `CollateralAmountInUSD` per trade to see where size is trading and at what price — helps time entries and exits in prediction markets.

**7. Protocol / marketplace verification**
`Marketplace.ProtocolName` and `ProtocolFamily` (e.g. "polymarket", "Gnosis_CTF") confirm the trade is from Polymarket on Polygon; use to avoid mixing with other protocols.

**8. Audit trail**
Each event includes `Transaction.Hash`, `Block.Time`, `Call.Signature.Name` (e.g. "matchOrders"), and `Log.Signature.Name` (e.g. "OrderFilled") for full on-chain audit.

---

## Step 1 — Check API Key

```python
import os
api_key = os.getenv("BITQUERY_API_KEY")
if not api_key:
    print("ERROR: BITQUERY_API_KEY environment variable is not set.")
    print("Run: export BITQUERY_API_KEY=your_token")
    exit(1)
```

If the key is missing, tell the user and stop. Do not proceed without it.

---

## Step 2 — Run the stream

Install the WebSocket dependency once:

```bash
pip install 'gql[websockets]'
```

Use the streaming script:

```bash
python ~/.openclaw/skills/polymarket-prediction-trades/scripts/stream_polymarket.py
```

Optional: stop after N seconds:

```bash
python ~/.openclaw/skills/polymarket-prediction-trades/scripts/stream_polymarket.py --timeout 60
```

Or subscribe inline with Python:

```python
import asyncio, os
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

async def main():
    token = os.environ["BITQUERY_API_KEY"]
    url = f"wss://streaming.bitquery.io/graphql?token={token}"
    transport = WebsocketsTransport(
        url=url,
        headers={"Sec-WebSocket-Protocol": "graphql-ws"},
    )
    async with Client(transport=transport) as session:
        sub = gql("""
            subscription MyQuery {
              EVM(network: matic) {
                PredictionTrades(where: { TransactionStatus: { Success: true } }) {
                  Block { Time }
                  Call { Signature { Name } }
                  Log { Signature { Name } SmartContract }
                  Trade {
                    OutcomeTrade {
                      Buyer
                      Seller
                      Amount
                      CollateralAmount
                      CollateralAmountInUSD
                      OrderId
                      Price
                      PriceInUSD
                      IsOutcomeBuy
                    }
                    Prediction {
                      CollateralToken { Name Symbol SmartContract AssetId }
                      ConditionId
                      OutcomeToken { Name Symbol SmartContract AssetId }
                      Marketplace { SmartContract ProtocolVersion ProtocolName ProtocolFamily }
                      Question { Title ResolutionSource Image MarketId Id CreatedAt }
                      Outcome { Id Index Label }
                    }
                  }
                  Transaction { From Hash }
                }
              }
            }
        """)
        async for result in session.subscribe(sub):
            for trade in (result.get("EVM") or {}).get("PredictionTrades") or []:
                q = (trade.get("Trade") or {}).get("Prediction") or {}
                q = q.get("Question") or {}
                ot = (trade.get("Trade") or {}).get("OutcomeTrade") or {}
                pred = (trade.get("Trade") or {}).get("Prediction") or {}
                outcome = pred.get("Outcome") or {}
                print(
                    f"{q.get('Title', '?')} | "
                    f"Outcome: {outcome.get('Label', '?')} | "
                    f"${float(ot.get('CollateralAmountInUSD') or 0):.2f}"
                )

asyncio.run(main())
```

---

## Step 3 — Key fields on every trade

| Field | What it means for traders |
|-------|----------------------------|
| `Trade.OutcomeTrade.Buyer` | Taker buyer address |
| `Trade.OutcomeTrade.Seller` | Maker seller address |
| `Trade.OutcomeTrade.Amount` | Outcome token amount (raw) |
| `Trade.OutcomeTrade.CollateralAmount` | Collateral token amount |
| `Trade.OutcomeTrade.CollateralAmountInUSD` | Notional in USD — use for size/whale filter |
| `Trade.OutcomeTrade.OrderId` | Order identifier |
| `Trade.OutcomeTrade.Price` | Price in collateral (0–1 typical for binary) |
| `Trade.OutcomeTrade.PriceInUSD` | Price in USD — entry/exit reference |
| `Trade.OutcomeTrade.IsOutcomeBuy` | True = buyer bought the outcome (Yes/Up) |
| `Trade.Prediction.Question.Title` | Market question (e.g. "Ethereum Up or Down - ...") |
| `Trade.Prediction.Question.MarketId` | Market ID for filtering |
| `Trade.Prediction.Question.ResolutionSource` | Resolution source (e.g. Chainlink URL) |
| `Trade.Prediction.Outcome.Label` | Outcome label (e.g. "Up", "Down") |
| `Trade.Prediction.Marketplace.ProtocolName` | e.g. "polymarket" |
| `Block.Time` | Trade timestamp (ISO) |
| `Transaction.Hash` | On-chain tx hash for audit |
| `Call.Signature.Name` | e.g. "matchOrders" |
| `Log.Signature.Name` | e.g. "OrderFilled" |

---

## Step 4 — Format output for traders

When presenting prediction trades to a trader, use this layout:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Polymarket  [matic]  Protocol: polymarket (Gnosis_CTF)
Time: 2026-03-10T13:21:11Z  Tx: 0x9566...f2da
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Question: Ethereum Up or Down - March 10, 9:15AM-9:30AM ET
MarketId: 1537455  |  Outcome: Down  (Index 1)
Resolution: https://data.chain.link/streams/eth-usd
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OutcomeTrade
  Side:       BUY outcome (IsOutcomeBuy: true)
  Buyer:      0x22dc...91bb  →  Seller: 0x86a2...73a8
  Collateral: 0.316471 USDC  (USD: $0.32)
  Price:      0.632942  (USD: $0.633)
  Amount:     500000 (outcome tokens)
  OrderId:    44433632...
Call: matchOrders  |  Log: OrderFilled @ 0x4bfb...982e
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error handling

- **Missing BITQUERY_API_KEY**: Tell user to export the variable and stop
- **WebSocket connection failed / 401**: Token invalid or expired (auth is via URL `?token=` only — do not pass the token in headers)
- **Subscription errors in payload**: Log the error and stop cleanly (send complete, close transport)
- **No events received**: Polygon prediction activity can be bursty; wait a few seconds or check that Polymarket has recent activity on matic
- **Empty PredictionTrades**: Ensure filter is `TransactionStatus: { Success: true }` and network is `matic`

---

## Reference

- **Bitquery Polymarket API docs:** [Polymarket API - Get Prices, Trades & Market Data](https://docs.bitquery.io/docs/examples/polymarket-api/)
- Full field reference is in `references/graphql-fields.md`. Use it to add filters or request extra fields (e.g. by MarketId, ConditionId, or date) in the subscription.
