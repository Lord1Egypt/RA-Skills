---
name: api
description: Complete Hyperliquid API reference — /info reads, /exchange signed actions, WebSocket subscriptions. The definitive guide for AI agents building on Hyperliquid.
---

# Hyperliquid API Reference

## Architecture

```
POST /info      — Reads (no auth, no signing required)
POST /exchange  — Writes (signed L1 actions required)
WS  /ws         — Subscriptions (real-time data)
```

**Mainnet:**
- REST: `https://api.hyperliquid.xyz`
- WebSocket: `wss://api.hyperliquid.xyz/ws`

**Testnet:**
- REST: `https://api.hyperliquid-testnet.xyz`
- WebSocket: `wss://api.hyperliquid-testnet.xyz/ws`

---

## Critical: Asset IDs

Asset IDs are required for all order actions. Get them wrong and orders fail silently or go to the wrong market.

```
Perps:     asset = index in meta.universe array
Spot:      asset = 10000 + index in spotMeta.universe array
HIP-3:     asset = 100000 + (perp_dex_index * 10000) + index_in_perp_meta
```

Always fetch `meta` and `spotMeta` at startup and cache them. Never hardcode asset IDs.

```python
from hyperliquid.info import Info
from hyperliquid.utils import constants

info = Info(constants.MAINNET_API_URL)
meta = info.meta()

# Build asset ID lookup
ASSET_IDS = {m['name']: i for i, m in enumerate(meta['universe'])}
print(ASSET_IDS['BTC'])  # e.g., 0
print(ASSET_IDS['ETH'])  # e.g., 1
```

---

## POST /info — Read Endpoints

### Market Data

```python
# All perp markets
info.meta()
# Returns: { universe: [{ name, szDecimals, maxLeverage, onlyIsolated, ... }] }

# All spot assets
info.spot_meta()
# Returns: { universe: [{ name, tokens: [...] }], tokens: [...] }

# All current mid prices
info.all_mids()
# Returns: { "BTC": "95000.0", "ETH": "3500.0", ... }

# Order book (L2 snapshot)
info.l2_snapshot("BTC")
# Returns: { coin: "BTC", levels: [[{px, sz, n}...], [{px, sz, n}...]], time: 1234 }
# levels[0] = bids (descending), levels[1] = asks (ascending)

# OHLCV candles
info.candles_snapshot("BTC", "1h", start_time_ms, end_time_ms)
# Returns: [{ t, o, h, l, c, v }]

# Recent trades
info.recent_trades("BTC")
# Returns: [{ coin, side, px, sz, time, hash }]

# Funding rate history
info.funding_history("BTC", start_time_ms)
# Returns: [{ coin, fundingRate, premium, time }]

# Meta and asset contexts (prices, OI, funding)
info.meta_and_asset_ctxs()
# Returns: [meta, [assetCtx per market]]
```

### Account Data

```python
# Perp account state
info.user_state(address)
# Returns: { assetPositions, marginSummary, withdrawable, time }

# Spot account state
info.spot_user_state(address)
# Returns: { balances: [{ coin, hold, total, entryNtl }] }

# Open orders
info.open_orders(address)
# Returns: [{ coin, side, limitPx, sz, oid, timestamp, ... }]

# Fill history
info.user_fills(address)
# Returns: [{ coin, px, sz, side, time, startPosition, closedPnl, fee, hash, ... }]

# Fill history since a timestamp
info.user_fills_by_time(address, start_time_ms)

# Order status by order ID
info.order_status(address, order_id)
# Returns: { order: {...}, status: "open"|"filled"|"canceled"|"rejected" }

# Referral state
info.referral(address)

# User funding history
info.user_funding(address, start_time_ms)

# Portfolio (cross-margin and isolated positions)
info.portfolio(address)
```

---

## POST /exchange — Signed Actions

All exchange actions require:
1. Build the action payload
2. Sign with EIP-712 or agent wallet
3. POST to `/exchange` with `{ action, nonce, signature }`

**Use the official SDK.** Signing correctly from scratch is error-prone.

### Nonces

Hyperliquid uses a **rolling nonce window**, not linear nonces like Ethereum.

```python
# Best practice: use millisecond timestamps
import time
nonce = int(time.time() * 1000)  # milliseconds
```

Requirements:
- Nonce must be unique per signer
- Must be within the valid time window (~60 seconds of current time)
- Using the same nonce twice = rejected
- Never share a signer across concurrent processes without atomic nonce allocation

### Place Order

```python
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
import eth_account

# Setup
private_key = "0x..."
account = eth_account.Account.from_key(private_key)
exchange = Exchange(account, constants.MAINNET_API_URL)

# Market buy BTC (coin = asset name, not ID — SDK handles ID lookup)
result = exchange.market_open(
    coin="BTC",
    is_buy=True,
    sz=0.001,        # size in BTC
    slippage=0.01,   # 1% max slippage
)
print(result)
# { status: "ok", response: { type: "order", data: { statuses: [...] } } }

# Limit order
result = exchange.order(
    coin="BTC",
    is_buy=True,
    sz=0.001,
    limit_px=90000.0,  # price
    order_type={"limit": {"tif": "Gtc"}},  # Good Till Cancel
)

# TIF options: "Gtc", "Alo" (add liquidity only), "Ioc" (immediate or cancel)

# Close position (market)
result = exchange.market_close(coin="BTC")

# Cancel order
result = exchange.cancel(coin="BTC", oid=order_id)

# Cancel all orders for a coin
result = exchange.cancel_by_cloid(coin="BTC", cloid="your-cloid")
```

### Order Types

```python
# Limit GTC
order_type = {"limit": {"tif": "Gtc"}}

# Limit ALO (maker only — rejects if would take)
order_type = {"limit": {"tif": "Alo"}}

# Limit IOC (immediate or cancel)
order_type = {"limit": {"tif": "Ioc"}}

# Trigger (stop loss / take profit)
order_type = {
    "trigger": {
        "isMarket": True,
        "triggerPx": "90000.0",
        "tpsl": "sl"   # "sl" = stop loss, "tp" = take profit
    }
}
```

### Batch Orders

```python
# Place multiple orders in one request (efficient — one IP hit, multiple actions)
orders = [
    {
        "coin": "BTC",
        "is_buy": True,
        "sz": 0.001,
        "limit_px": 90000.0,
        "order_type": {"limit": {"tif": "Gtc"}},
        "reduce_only": False,
    },
    {
        "coin": "ETH",
        "is_buy": False,
        "sz": 0.1,
        "limit_px": 3600.0,
        "order_type": {"limit": {"tif": "Gtc"}},
        "reduce_only": False,
    }
]

result = exchange.bulk_orders(orders)
```

### Account Management

```python
# Set leverage for a coin
exchange.update_leverage(leverage=10, coin="BTC", is_cross=True)

# Change margin type
exchange.update_isolated_margin(amount=100.0, coin="BTC")  # add $100 isolated margin

# Withdraw from perp to spot
exchange.withdraw_from_bridge(amount=100.0, destination=address)

# Transfer between subaccounts
exchange.usd_transfer(amount=100.0, destination=address)
```

### API Wallet (Agent Wallet)

API wallets sign on behalf of a master account. Use for automation to avoid using your main key.

```python
from hyperliquid.exchange import Exchange

# Register an API wallet
# (do this once, from your main account)
result = master_exchange.approve_agent(
    agent_address=api_wallet_address,
    agent_name="my-bot"
)

# Use API wallet for trading
api_account = eth_account.Account.from_key(api_private_key)
api_exchange = Exchange(
    api_account,
    constants.MAINNET_API_URL,
    vault_address=master_address  # trades credited to master
)

# Now trade as the master account
result = api_exchange.market_open("BTC", True, 0.001, 0.01)
```

---

## WebSocket Subscriptions

```javascript
import WebSocket from 'ws';

class HyperliquidWS {
  constructor(url = 'wss://api.hyperliquid.xyz/ws') {
    this.url = url;
    this.ws = null;
    this.subscriptions = new Map();
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.on('open', () => {
      console.log('Connected');
      // Re-subscribe after reconnect
      for (const [id, sub] of this.subscriptions) {
        this.ws.send(JSON.stringify({ method: 'subscribe', subscription: sub }));
      }
      // Heartbeat
      this.heartbeat = setInterval(() => {
        this.ws.send(JSON.stringify({ method: 'ping' }));
      }, 30000);
    });

    this.ws.on('close', () => {
      clearInterval(this.heartbeat);
      setTimeout(() => this.connect(), 1000); // reconnect
    });

    this.ws.on('message', (raw) => {
      const msg = JSON.parse(raw);
      this.handleMessage(msg);
    });
  }

  subscribe(subscription, handler) {
    const id = JSON.stringify(subscription);
    this.subscriptions.set(id, { subscription, handler });
    this.ws.send(JSON.stringify({ method: 'subscribe', subscription }));
  }

  handleMessage(msg) {
    if (msg.channel === 'pong') return;
    for (const [, { subscription, handler }] of this.subscriptions) {
      if (msg.channel === subscription.type) {
        handler(msg.data);
      }
    }
  }
}

// Usage
const hl = new HyperliquidWS();

// Order book updates
hl.subscribe({ type: 'l2Book', coin: 'BTC' }, (data) => {
  const [bids, asks] = data.levels;
  console.log(`BTC: ${bids[0]?.px} / ${asks[0]?.px}`);
});

// All mid prices (every second)
hl.subscribe({ type: 'allMids' }, (data) => {
  console.log('BTC mid:', data.mids?.BTC);
});

// User fills
hl.subscribe({ type: 'userFills', user: '0xYourAddress' }, (data) => {
  for (const fill of data.fills) {
    console.log(`Fill: ${fill.coin} ${fill.side} ${fill.sz} @ ${fill.px}`);
  }
});

// User events (order updates, position changes)
hl.subscribe({ type: 'userEvents', user: '0xYourAddress' }, (data) => {
  console.log('User event:', data);
});

// Trades feed for a market
hl.subscribe({ type: 'trades', coin: 'BTC' }, (data) => {
  for (const trade of data) {
    console.log(`Trade: ${trade.side} ${trade.sz} @ ${trade.px}`);
  }
});
```

### All WebSocket Subscription Types

| Type | Params | Data |
|------|--------|------|
| `allMids` | none | All mid prices, every second |
| `l2Book` | `coin` | Order book updates |
| `trades` | `coin` | Recent trades stream |
| `candle` | `coin`, `interval` | OHLCV candle updates |
| `userEvents` | `user` | Order updates, fills, liquidations |
| `userFills` | `user` | Fill notifications |
| `userFundings` | `user` | Funding payment notifications |
| `userNonFundingLedgerUpdates` | `user` | Deposits, withdrawals, transfers |
| `notification` | `user` | Liquidation warnings |
| `webData2` | `user` | Full user state snapshot |

---

## Rate Limits

**IP-level:**
- REST: weighted request limit per minute
- Batching orders helps IP budget but still counts per-action for address limits
- WebSocket: connection, subscription, and message limits apply

**Address-level:**
- Action throughput tied to account history and volume tier
- A batch of 10 orders = 1 IP request, but 10 address-level actions

Design around **both** limits, not just one.

---

## Error Handling

```python
result = exchange.market_open("BTC", True, 0.001, 0.01)

if result['status'] == 'ok':
    statuses = result['response']['data']['statuses']
    for status in statuses:
        if 'filled' in status:
            print(f"Filled at {status['filled']['avgPx']}")
        elif 'resting' in status:
            print(f"Resting order ID: {status['resting']['oid']}")
        elif 'error' in status:
            print(f"Order error: {status['error']}")
elif result['status'] == 'err':
    print(f"Exchange error: {result['response']}")
```

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Nonce too low` | Reused nonce, clock skew | Use `int(time.time() * 1000)`, ensure monotonic |
| `User or API wallet does not exist` | Wrong signing key or vault address | Check account registration, API wallet approval |
| `Insufficient margin` | Not enough collateral | Deposit more or reduce size |
| `Invalid sz` | Size violates `szDecimals` | Round to correct decimal places from `meta` |
| `Invalid px` | Price violates tick constraints | Use SDK's price normalization |
| `Post-only rejected` | ALO order would have taken | Market has moved; retry or switch to GTC |

---

## Pre-Integration Checklist

```
[ ] Fetched meta and built asset ID lookup
[ ] Using millisecond timestamps for nonces
[ ] Nonce allocator is atomic (no concurrent reuse)
[ ] API wallet registered (not using main key for automation)
[ ] Tested full order lifecycle on testnet
[ ] Error handling covers: fill, resting, error statuses
[ ] WebSocket reconnect logic implemented
[ ] Rate limit awareness (batch where possible)
[ ] Kill switch for repeated rejections
```
