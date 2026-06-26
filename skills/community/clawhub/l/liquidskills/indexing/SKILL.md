---
name: indexing
description: How to read Hyperliquid data — HyperCore via /info API, HyperEVM events, WebSocket subscriptions. Why you cannot just loop through blocks, and what to use instead.
---

# Hyperliquid Data & Indexing

## What You Probably Got Wrong

**You try to loop through HyperEVM blocks for data.** Scanning blocks is slow and rate-limited. For HyperCore data (order fills, positions, funding), use the `/info` REST API — it's instant and comprehensive.

**You don't know the data lives in two places.** HyperCore (perps, spot, order books) has its own API at `api.hyperliquid.xyz`. HyperEVM has standard EVM events. They're different systems. Know which one has your data.

**You try to use `eth_getLogs` for HyperCore activity.** HyperCore trades, fills, and positions don't emit EVM events — they're protocol state. Query them via `POST /info`.

**You treat WebSocket subscriptions as optional.** For live trading data (order book, recent trades, fills), use WebSocket at `wss://api.hyperliquid.xyz/ws`. Polling the REST API for live data is slow and rude.

**You store index results onchain.** Leaderboards, activity feeds, analytics — these belong offchain. Emit events, index offchain. If you need onchain commitment, store a hash.

---

## Two Data Layers

```
┌─────────────────────────────────────────────────────────┐
│  HyperCore Data                                         │
│  ├── Perp positions, open orders, fills                 │
│  ├── Spot balances and trades                           │
│  ├── Funding rates, mark prices, oracle prices          │
│  ├── Account meta (leverage, margin type)               │
│  └── Query via: POST https://api.hyperliquid.xyz/info  │
├─────────────────────────────────────────────────────────┤
│  HyperEVM Data                                          │
│  ├── ERC-20 balances and transfers                      │
│  ├── Custom contract events (your contracts)            │
│  ├── Smart contract state                               │
│  └── Query via: JSON-RPC / eth_getLogs / event indexers │
└─────────────────────────────────────────────────────────┘
```

---

## Reading HyperCore Data

### POST /info — The Primary Read API

All reads go to `https://api.hyperliquid.xyz/info` (mainnet) or `https://api.hyperliquid-testnet.xyz/info` (testnet).

```javascript
import axios from 'axios';

const API = 'https://api.hyperliquid.xyz/info';

// Get all perpetual market data (no auth required)
async function getMeta() {
  const { data } = await axios.post(API, { type: 'meta' });
  return data;
  // Returns: { universe: [{ name, szDecimals, maxLeverage, ... }] }
}

// Get user's perpetual positions and account state
async function getClearinghouseState(address) {
  const { data } = await axios.post(API, {
    type: 'clearinghouseState',
    user: address
  });
  return data;
  // Returns positions, margin summary, withdrawable, etc.
}

// Get user's open orders
async function getOpenOrders(address) {
  const { data } = await axios.post(API, {
    type: 'openOrders',
    user: address
  });
  return data;
}

// Get user's fill history
async function getUserFills(address) {
  const { data } = await axios.post(API, {
    type: 'userFills',
    user: address
  });
  return data;
  // Returns: array of { coin, px, sz, side, time, fee, ... }
}

// Get L2 order book snapshot for a market
async function getL2Book(coin) {
  const { data } = await axios.post(API, {
    type: 'l2Book',
    coin
  });
  return data;
  // Returns: { coin, levels: [[bids], [asks]] }
}

// Get all mid prices
async function getAllMids() {
  const { data } = await axios.post(API, { type: 'allMids' });
  return data;
  // Returns: { BTC: "95000.0", ETH: "3500.0", ... }
}

// Get spot balances for a user
async function getSpotBalances(address) {
  const { data } = await axios.post(API, {
    type: 'spotClearinghouseState',
    user: address
  });
  return data;
}

// Get funding rate history
async function getFundingHistory(coin, startTime) {
  const { data } = await axios.post(API, {
    type: 'fundingHistory',
    coin,
    startTime
  });
  return data;
}
```

### Python with the Official SDK

```python
from hyperliquid.info import Info
from hyperliquid.utils import constants

# Mainnet
info = Info(constants.MAINNET_API_URL)

# Get all positions for a user
user_address = "0xYourAddress"
state = info.user_state(user_address)
print(state['assetPositions'])  # List of open positions

# Get order book
l2_data = info.l2_snapshot("BTC")
print(l2_data['levels'])  # [bids, asks]

# Get recent fills
fills = info.user_fills(user_address)
for fill in fills[:10]:
    print(f"{fill['coin']} {fill['side']} {fill['sz']} @ {fill['px']}")

# Get all mid prices
mids = info.all_mids()
print(f"BTC mid: {mids.get('BTC')}")
```

---

## WebSocket Subscriptions

For live data, use `wss://api.hyperliquid.xyz/ws`.

```javascript
import WebSocket from 'ws';

const ws = new WebSocket('wss://api.hyperliquid.xyz/ws');

ws.on('open', () => {
  // Subscribe to order book updates for BTC
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: { type: 'l2Book', coin: 'BTC' }
  }));

  // Subscribe to all mid prices (heartbeat every second)
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: { type: 'allMids' }
  }));

  // Subscribe to fills for a specific user
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: {
      type: 'userFills',
      user: '0xYourAddress'
    }
  }));
  
  // Subscribe to user events (orders, positions)
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: {
      type: 'userEvents',
      user: '0xYourAddress'
    }
  }));
});

ws.on('message', (raw) => {
  const msg = JSON.parse(raw);
  
  if (msg.channel === 'l2Book') {
    const { coin, levels } = msg.data;
    const [bids, asks] = levels;
    console.log(`${coin} best bid: ${bids[0]?.px}, best ask: ${asks[0]?.px}`);
  }
  
  if (msg.channel === 'userFills') {
    for (const fill of msg.data.fills) {
      console.log(`Fill: ${fill.coin} ${fill.side} ${fill.sz} @ ${fill.px}`);
    }
  }
  
  if (msg.channel === 'userEvents') {
    // Order updates, position changes
    console.log('User event:', msg.data);
  }
});

// Heartbeat to keep connection alive
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ method: 'ping' }));
  }
}, 30000);
```

---

## Reading HyperEVM Events (Your Contracts)

For data from your own Solidity contracts, use standard EVM event indexing.

### Design Events First

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TokenLaunch {
    event TokenLaunched(
        address indexed token,
        address indexed creator,
        string name,
        string symbol,
        uint256 timestamp
    );
    
    event Trade(
        address indexed token,
        address indexed trader,
        bool isBuy,
        uint256 hypeAmount,      // HYPE in (buy) or out (sell)
        uint256 tokenAmount,     // tokens out (buy) or in (sell)
        uint256 price,           // current price after trade
        uint256 timestamp
    );
    
    event Graduated(
        address indexed token,
        uint256 totalHypeRaised,
        address lpAddress,
        uint256 timestamp
    );
}
```

### Querying Events with viem

```javascript
import { createPublicClient, http, parseAbiItem } from 'viem';
import { defineChain } from 'viem/chains';

const hyperEVM = defineChain({
  id: 999,
  name: 'HyperEVM',
  nativeCurrency: { name: 'HYPE', symbol: 'HYPE', decimals: 18 },
  rpcUrls: { default: { http: ['https://rpc.hyperliquid.xyz/evm'] } },
});

const client = createPublicClient({
  chain: hyperEVM,
  transport: http(),
});

const CONTRACT = '0xYourContractAddress';

// Get all Trade events
const trades = await client.getLogs({
  address: CONTRACT,
  event: parseAbiItem('event Trade(address indexed token, address indexed trader, bool isBuy, uint256 hypeAmount, uint256 tokenAmount, uint256 price, uint256 timestamp)'),
  fromBlock: 0n,
  toBlock: 'latest',
});

// Get trades for a specific token
const tokenTrades = await client.getLogs({
  address: CONTRACT,
  event: parseAbiItem('event Trade(address indexed token, address indexed trader, bool isBuy, uint256 hypeAmount, uint256 tokenAmount, uint256 price, uint256 timestamp)'),
  args: { token: '0xSpecificToken' },
  fromBlock: 0n,
  toBlock: 'latest',
});

// Watch for new events in real-time
const unwatch = client.watchEvent({
  address: CONTRACT,
  event: parseAbiItem('event Trade(address indexed token, address indexed trader, bool isBuy, uint256 hypeAmount, uint256 tokenAmount, uint256 price, uint256 timestamp)'),
  onLogs: (logs) => {
    for (const log of logs) {
      console.log('New trade:', log.args);
    }
  },
});
```

### Building a Simple Indexer with Supabase

```javascript
import { createPublicClient, http } from 'viem';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
const client = createPublicClient({ chain: hyperEVM, transport: http() });

async function indexTrades(fromBlock, toBlock) {
  const logs = await client.getLogs({
    address: CONTRACT,
    events: [TRADE_ABI],
    fromBlock,
    toBlock,
  });
  
  const rows = logs.map(log => ({
    tx_hash: log.transactionHash,
    block_number: Number(log.blockNumber),
    token: log.args.token,
    trader: log.args.trader,
    is_buy: log.args.isBuy,
    hype_amount: log.args.hypeAmount.toString(),
    token_amount: log.args.tokenAmount.toString(),
    price: log.args.price.toString(),
    timestamp: Number(log.args.timestamp),
  }));
  
  if (rows.length > 0) {
    await supabase.from('trades').upsert(rows, { onConflict: 'tx_hash' });
  }
  
  return logs.length;
}

// Run indexer in chunks
async function runIndexer() {
  let fromBlock = await getLastIndexedBlock();
  const latestBlock = await client.getBlockNumber();
  
  for (let block = fromBlock; block <= latestBlock; block += 1000n) {
    const toBlock = block + 999n < latestBlock ? block + 999n : latestBlock;
    const count = await indexTrades(block, toBlock);
    console.log(`Indexed blocks ${block}-${toBlock}: ${count} events`);
    await saveLastIndexedBlock(toBlock);
  }
}
```

---

## Supabase Realtime for Live Feeds

Once you're writing events to Supabase, expose them via Realtime:

```javascript
// Subscribe to new trades in real-time
const channel = supabase
  .channel('trades')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'trades',
  }, (payload) => {
    console.log('New trade:', payload.new);
    updateUI(payload.new);
  })
  .subscribe();
```

---

## Key /info Endpoints Reference

| Type | Required Params | Returns |
|------|----------------|---------|
| `meta` | none | All perp markets and their properties |
| `spotMeta` | none | All spot assets |
| `allMids` | none | Current mid prices for all assets |
| `clearinghouseState` | `user` | Positions, margin, withdrawable |
| `spotClearinghouseState` | `user` | Spot token balances |
| `openOrders` | `user` | User's open orders |
| `userFills` | `user` | User's fill history |
| `orderStatus` | `user`, `oid` | Single order status |
| `l2Book` | `coin` | Order book snapshot |
| `candleSnapshot` | `coin`, `interval`, `startTime`, `endTime` | OHLCV candles |
| `fundingHistory` | `coin`, `startTime` | Funding rate history |
| `userFundingHistory` | `user`, `startTime` | User's funding payments |

---

## Rules

1. **HyperCore data → `/info` API.** Don't use EVM RPC for this.
2. **Live data → WebSocket.** Don't poll REST for live feeds.
3. **Your contract data → `eth_getLogs` + event indexer.**
4. **Store index offchain.** Supabase, PostgreSQL, or any database. Never onchain.
5. **Emit events for everything.** If your contract changes state, emit an event. No exceptions.
6. **Handle reconnects.** WebSocket connections drop. Reconnect with exponential backoff and re-subscribe.
7. **Chunk `eth_getLogs`.** Query in blocks of 1000-5000. Larger ranges timeout.
