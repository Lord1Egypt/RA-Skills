# GoldRush Streaming API Overview

## Quick Reference

| Item | Value |
|------|-------|
| **WebSocket URL** | `wss://streaming.goldrushdata.com/graphql` |
| **Protocol** | GraphQL over WebSocket (`graphql-transport-ws`) |
| **Authentication** | API key via `connection_init` payload as `GOLDRUSH_API_KEY` |
| **SDK** | `@covalenthq/client-sdk` (TypeScript) |
| **Endpoint Types** | `subscription` (real-time push), `query` (one-time fetch) |
| **Chain Name Format** | `SCREAMING_SNAKE_CASE` (e.g. `ETH_MAINNET`, `BASE_MAINNET`) |

---

## Connection Details

  The Streaming API uses the [GraphQL over WebSocket](https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md) protocol. The recommended approach is to use the official [TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk) which manages all WebSocket connections automatically.

## Use Cases

  
**Trading Bots:** Power your bots with new pairs, pair liquidity changes, OHLCV pricing data,
    and wallet activity to copy trade.

  
**Gaming:** Stream inventory balances and onchain game state right into your game engine
    with no lag or polling.

  
**AI Agents:** Power your AI Agents with streaming wallet information to build novel
    co-pilot apps.

## Available Streams

The GoldRush Streaming API offers the following streams:

- ****OHLCV Tokens Stream****: Continuous price data feed providing Open, High, Low, Close, Volume values for one or many tokens at configurable intervals. Commonly used to execute trading strategies like take-profit, stop-loss and others.

- ****OHLCV Pairs Stream****: Continuous price data feed providing Open, High, Low, Close, Volume values for one or many token pairs at configurable intervals. Commonly used to execute trading strategies like take-profit, stop-loss and others.

- ****New DEX Pairs Stream****: Real-time updates on new pairs, pair liquidity changes, and other pair-related events across supported DEXes. Commonly used to build liquidity sniping bots.

- ****Update Pairs Stream****: Real-time price, liquidity, volume, and market cap updates for tracked token pairs. Commonly used to monitor portfolio exposure or trigger alerting workflows.

- ****Wallet Activity Stream****: Live tracking of wallet transactions, token transfers, and interactions with smart contracts. Commonly used to build copy trading bots.

## Price Feed Sources

Price feeds used in the GoldRush Streaming API are sourced in the following ways:

1. **DEX swap events** — prices are derived from onchain trades in specific pools across the [supported DEXes](#supported-chains-&-dexes). Prices update with each swap event.
2. **Onchain oracle price feeds** — on select chains and for specific tokens, prices are pushed onchain by oracle providers (e.g. [Redstone Bolt](https://redstone.finance/) on MegaETH), delivering CEX-aggregated prices at much higher update frequencies.

See the **OHLCV Tokens Stream** for the full list of supported oracle price feeds.

## Access via GoldRush CLI

You can also access Streaming API data directly from your terminal using **GoldRush CLI** - no code or WebSocket setup required:

| CLI Command | Streaming API Equivalent |
| --- | --- |
| **`goldrush new_pairs`** | **New DEX Pairs Stream** |
| **`goldrush ohlcv_pairs`** | **OHLCV Pairs Stream** |
| **`goldrush watch`** | **Wallet Activity Stream** |
| **`goldrush traders`** | **uPnL for Token Query** |
| **`goldrush search`** | **Token Search Query** |

## Supported Chains & DEXes

---

## Supported Chains & DEXes

### Chain Name Format

The Streaming API uses `SCREAMING_SNAKE_CASE` enum names, unlike the REST API which uses `kebab-case`.

| REST API (kebab-case) | Streaming API (SCREAMING_SNAKE_CASE) |
|----------------------|--------------------------------------|
| `base-mainnet` | `BASE_MAINNET` |
| `bsc-mainnet` | `BSC_MAINNET` |
| `eth-mainnet` | `ETH_MAINNET` |
| `hypercore-mainnet` | `HYPERCORE_MAINNET` |
| `hyperevm-mainnet` | `HYPEREVM_MAINNET` |
| `megaeth-mainnet` | `MEGAETH_MAINNET` |
| `monad-mainnet` | `MONAD_MAINNET` |
| `matic-mainnet` | `MATIC_MAINNET` |
| `solana-mainnet` | `SOLANA_MAINNET` |
| `sonic-mainnet` | `SONIC_MAINNET` |

### Supported DEXes by Chain

| Chain | Supported DEXes |
|-------|----------------|
| `BASE_MAINNET` | `UNISWAP_V2`, `UNISWAP_V3`, `PANCAKESWAP_V2`, `PANCAKESWAP_V3`, `VIRTUALS_V2`, `CLANKER_V3` |
| `BSC_MAINNET` | `PANCAKESWAP_V2`, `PANCAKESWAP_V3` |
| `ETH_MAINNET` | `UNISWAP_V2`, `UNISWAP_V3` |
| `HYPEREVM_MAINNET` | `PROJECT_X` |
| `MEGAETH_MAINNET` | `UNISWAP_V2`, `UNISWAP_V3`, `JOE_V2`, `KUMBAYA_V1`, `PRISM_V1` |
| `MONAD_MAINNET` | `NAD_FUN`, `UNISWAP_V2`, `UNISWAP_V3` |
| `POLYGON_MAINNET` | `QUICKSWAP_V2`, `QUICKSWAP_V3`, `SUSHISWAP_V2` |
| `SOLANA_MAINNET` | `RAYDIUM_AMM`, `RAYDIUM_CPMM`, `RAYDIUM_CLMM`, `PUMP_FUN`, `PUMP_FUN_AMM`, `MOONSHOT`, `RAYDIUM_LAUNCH_LAB`, `METEORA_DAMM`, `METEORA_DLMM`, `METEORA_DBC`, `ORCA_WHIRLPOOL` |
| `SONIC_MAINNET` | `SHADOW_V2`, `SHADOW_V3` |

### Capabilities Matrix

| Chain | Chain Name | Chain ID | Block Time |
|-------|-----------|----------|------------|
| Base | `base-mainnet` | 8453 | 2s |
| BNB Smart Chain (BSC) | `bsc-mainnet` | 56 | 5s |
| Ethereum | `eth-mainnet` | 1 | 12s |
| HyperCore | `hypercore-mainnet` | na | 1s |
| HyperEVM | `hyperevm-mainnet` | 999 | 1s |
| MegaETH | `megaeth-mainnet` | 4326 | 1s |
| Monad | `monad-mainnet` | 143 | 1s |
| Polygon | `matic-mainnet` | 137 | 3s |
| Solana | `solana-mainnet` | 1399811149 | 1s |
| Sonic | `sonic-mainnet` | 146 | 1s |


---

## Prerequisites

Using any of the GoldRush developer tools requires an API key.

### Vibe Coders

$10/mo — Built for solo builders and AI-native workflows.

### Teams

$250/mo — Production-grade with 50 RPS and priority support.

## Connection
The Streaming API supports GraphQL subscriptions over WebSocket, using the [GraphQL over WebSocket](https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md) protocol.

The recommended approach is to use the official [TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk) which supports the Streaming API and manages all WebSocket connections.

```bash npm
npm install @covalenthq/client-sdk
```

```bash yarn
yarn add @covalenthq/client-sdk
```

You can also use a GraphQL over WebSocket protocol npm package like [`graphql-ws`](https://www.npmjs.com/package/graphql-ws). 

If you're not using the `graphql-ws` package, you must set the WebSocket protocol header:

`"Sec-WebSocket-Protocol" : "graphql-transport-ws"`

This header is required for the server to properly recognize and handle your GraphQL subscription requests.

## OHLCV Token Stream Code Samples
The following examples show how to connect and subscribe to the OHLCV Token stream using your preferred language or tool. Each sample connects to the WebSocket endpoint, authenticates with your API key, and streams real-time OHLCV updates for a token on Base Mainnet.

```typescript GoldRush SDK
import {
  GoldRushClient,
  StreamingChain,
  StreamingInterval,
  StreamingTimeframe
} from "@covalenthq/client-sdk";

const client = new GoldRushClient(
  "",
  {},
  {
    onConnecting: () => console.log("Connecting to streaming service..."),
    onOpened: () => console.log("Connected to streaming service!"),
    onClosed: () => console.log("Disconnected from streaming service"),
    onError: (error) => console.error("Streaming error:", error),
  }
);

client.StreamingService.subscribeToOHLCVTokens(
  {
    chain_name: StreamingChain.BASE_MAINNET,
    token_addresses: ["0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b"],
    interval: StreamingInterval.ONE_MINUTE,
    timeframe: StreamingTimeframe.ONE_HOUR,
  },
  {
    next: (data) => {
      console.log("Received OHLCV token data:", data);
    },
    error: (error) => {
      console.error("Streaming error:", error);
    },
    complete: () => {
      console.log("Stream completed");
    },
  }
);
```

```typescript TypeScript (graphql-ws)
import { createClient } from "graphql-ws";

const CONNECTION_URL = "wss://streaming.goldrushdata.com/graphql";

// Define your API key
const API_KEY = "";

const client = createClient({
  url: CONNECTION_URL,
  connectionParams: {
    GOLDRUSH_API_KEY: API_KEY,
  },
  shouldRetry: (retries) => retries  {
      console.log("⏳ WebSocket connecting...");
    },
    opened: () => {
      console.log("✅ WebSocket connection established");
    },
    closed: () => {
      console.log("❌ WebSocket connection closed");
    },
    error: (err) => {
      console.error("⚠️ WebSocket error:", err);
    },
  },
});

const SUBSCRIPTION_QUERY = `
  subscription {
    ohlcvCandlesForToken(
      chain_name: BASE_MAINNET
      token_addresses: ["0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b"]
      interval: ONE_MINUTE
      timeframe: ONE_HOUR
    ) {
      chain_name
      interval
      timeframe
      timestamp
      open
      high
      low
      close
      volume
      volume_usd
      quote_rate
      quote_rate_usd
      base_token {
        contract_name
        contract_address
        contract_decimals
        contract_ticker_symbol
      }
    }
  }
`;

client.subscribe(
  {
    query: SUBSCRIPTION_QUERY,
  },
  {
    next: (data) => {
      console.log("Received data:");
      console.log(JSON.stringify(data, null, 2));
    },
    error: (err) => {
      console.error("Subscription error:", err);
    },
    complete: () => {
      console.log("Subscription completed");
    },
  }
);
```
```python Python
import asyncio
from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport

# Replace with your actual API key
GOLDRUSH_API_KEY = ""

# GraphQL WebSocket endpoint
WS_URL = "wss://streaming.goldrushdata.com/graphql"

# Define the subscription query
SUBSCRIPTION_QUERY = gql("""
subscription {
  ohlcvCandlesForToken(
    chain_name: BASE_MAINNET
    token_addresses: ["0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b"]
    interval: ONE_MINUTE
    timeframe: ONE_HOUR
  ) {
    chain_name
    interval
    timeframe
    timestamp
    open
    high
    low
    close
    volume
    volume_usd
    quote_rate
    quote_rate_usd
    base_token {
      contract_name
      contract_address
      contract_decimals
      contract_ticker_symbol
    }
  }
}
""")

async def main():
    # Set up WebSocket transport with API key in connection init payload
    transport = WebsocketsTransport(
        url=WS_URL,
        init_payload={"apiKey": API_KEY}
    )

    # Create GraphQL client
    async with Client(
        transport=transport,
        fetch_schema_from_transport=False,
    ) as session:
        # Subscribe and print data
        async for result in session.subscribe(SUBSCRIPTION_QUERY):
            print("📡 Received data:")
            print(result)

# Run the async main function
asyncio.run(main())
```
```bash Terminal (websocat)
( echo '{"type":"connection_init","payload":{"GOLDRUSH_API_KEY":""}}'; \
  echo '{"type":"start","id":"1","payload":{"query":"subscription { ohlcvCandlesForToken(chain_name: BASE_MAINNET, token_addresses: [\"0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b\"], interval: ONE_MINUTE, timeframe: ONE_HOUR) { timestamp open high low close volume volume_usd quote_rate quote_rate_usd base_token { contract_name contract_address contract_decimals contract_ticker_symbol } } }"}}' \
) | websocat --header="Sec-WebSocket-Protocol: graphql-ws" wss://streaming.goldrushdata.com/graphql | jq
```

## Response Format
Here is an example of the response you should receive from the above code samples:
```json
{
  "data": {
    "ohlcvCandlesForToken": [
      {
        "chain_name": "BASE_MAINNET",
        "interval": "ONE_MINUTE",
        "timeframe": "ONE_HOUR",
        "timestamp": "2025-06-27T22:24:00Z",
        "open": 0.000604418526534047,
        "high": 0.000604638206820701,
        "low": 0.000604013151624892,
        "close": 0.000604638206820701,
        "volume": 1.4980526133065126,
        "volume_usd": 6004669.256018968,
        "quote_rate": 0.000604638206820701,
        "quote_rate_usd": 4007551.6142841205,
        "base_token": {
          "contract_name": "Virtual Protocol",
          "contract_address": "0x0b3e328455c4059eeb9e3f84b5543f74e24e7e1b",
          "contract_decimals": 18,
          "contract_ticker_symbol": "VIRTUAL"
        }
      }
    ]
  }
}
```

## GraphQL Playground

---

This document provides a comprehensive overview of the authentication process for GraphQL subscriptions with the Streaming API. It covers the rationale for authentication, how to obtain and use an API key, client-side implementation examples, server-side validation, error handling, and frequently asked questions.

## Why is Authentication Required?

Authentication is essential to ensure that only authorized users can access premium or rate-limited real-time data streams. **All clients must present a valid GoldRush API key to interact with the GraphQL subscription endpoints.**

## 1. Obtaining a GoldRush API Key

To begin, register for an API key at the [GoldRush Platform](https://goldrush.dev/platform/auth/register/). This key will be required for all authenticated requests to the Streaming API.

### Vibe Coders

$10/mo — Built for solo builders and AI-native workflows.

### Teams

$250/mo — Production-grade with 50 RPS and priority support.

## 2. Supplying the API Key from the Client

### Use the GoldRush Client SDK (recommended)

The recommended approach is to use the official [GoldRush TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk) which handles authentication automatically and provides a simplified interface for managing stream subscriptions.

```bash
npm install @covalenthq/client-sdk
```

```typescript
import {
  GoldRushClient,
  StreamingChain,
  StreamingInterval,
  StreamingTimeframe
} from "@covalenthq/client-sdk";

const client = new GoldRushClient(
  "", // Your GoldRush API key
  {},
  {
    onConnecting: () => console.log("Connecting to streaming service..."),
    onOpened: () => console.log("Connected to streaming service!"),
    onClosed: () => console.log("Disconnected from streaming service"),
    onError: (error) => console.error("Streaming error:", error),
  }
);

// Subscribe to OHLCV tokens stream
client.StreamingService.subscribeToOHLCVTokens(
  {
    chain_name: StreamingChain.BASE_MAINNET,
    token_addresses: ["0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b"],
    interval: StreamingInterval.ONE_MINUTE,
    timeframe: StreamingTimeframe.ONE_HOUR,
  },
  {
    next: (data) => {
      console.log("Received OHLCV token data:", data);
    },
    error: (error) => {
      console.error("Streaming error:", error);
    },
    complete: () => {
      console.log("Stream completed");
    },
  }
);
```

The SDK automatically handles:
- WebSocket connection management
- API key authentication
- Connection retry logic
- Error handling
- Type safety for parameters

### Use a GraphQL WebSocket Client

For direct WebSocket connections, you can use a package like [graphql-ws](https://github.com/enisdenjo/graphql-ws) library. Below is an example implementation in Node.js:

```js
import { createClient } from "graphql-ws";

const client = createClient({
  url: "wss://streaming.goldrushdata.com/graphql",
  connectionParams: {
    GOLDRUSH_API_KEY: "YOUR_API_KEY_HERE", // Replace with your GoldRush API key
  },
});

(async () => {
  await client.subscribe(
    {
      query: `subscription { newPairs { ...fields } }`,
    },
    {
      next: (data) => console.log("Received data:", data),
      error: (err) => console.error("Subscription error:", err),
      complete: () => console.log("Subscription complete"),
    }
  );
})();
```

> **Note:** The API key must be provided as `GOLDRUSH_API_KEY` within the `connectionParams` object.

### Use `websocat` for Manual WebSocket Testing

For manual testing or debugging, [websocat](https://github.com/vi/websocat) can be used to interact with the WebSocket endpoint directly from the command line.

  
```
websocat -H="Sec-WebSocket-Protocol: graphql-transport-ws" wss://streaming.goldrushdata.com/graphql
```
  
  
Send the following JSON as your first message, replacing `` with your actual API key:

```
{
    "type": "connection_init",
    "payload": { "GOLDRUSH_API_KEY": "" }
}
```

Wait for a `connection_ack` response from the server before proceeding.

  
  

You may now send a subscription query, for example:

```
{
    "id": "74bb224c-22c6-4a0f-ad85-d43a8c4e49ce",
    "type": "subscribe",
    "payload": {
        "query": "subscription {newPairs(chain_name: BASE_MAINNET) { chain_name protocol protocol_version event_name tx_hash block_signed_at pair_address pair_metadata { contract_name contract_address contract_decimals contract_ticker_symbol } base_token_metadata { contract_name contract_address contract_decimals contract_ticker_symbol } quote_token_metadata { contract_name contract_address contract_decimals contract_ticker_symbol } deployer_address quote_rate quote_rate_usd liquidity market_cap supply prices { last_5m last_1hr last_6hr last_24hr } swaps { last_5m last_1hr last_6hr last_24hr }}}"
    }
}
```

If authentication is successful, you will begin receiving real-time data for your subscription.

   

## 3. Server-Side Authentication Process

- The server **does not** validate the API key at the time of WebSocket connection establishment.
- Instead, authentication is enforced at the start of each GraphQL subscription resolver.
- If the API key is missing or invalid, the subscription will immediately terminate with an error message.

## 4. Error Handling

If authentication fails, the client will receive a GraphQL error with one of the following codes:

- `MISSING_TOKEN`: No API key was provided in the `connection_init` payload.
- `INVALID_TOKEN`: The provided API key is malformed or invalid.
- `AUTH_SYSTEM_ERROR`: An internal server error occurred during authentication.

**Example Error Response:**

```json
{
  "errors": [
    {
      "message": "Authentication required. Please provide a valid API key in the connection_init payload under 'GOLDRUSH_API_KEY' or 'Authorization' key.",
      "extensions": {
        "code": "MISSING_TOKEN"
      }
    }
  ]
}
```

For a complete guide to error codes, retry strategies, and debugging tips, see **Error Handling & Troubleshooting**.

## 5. Frequently Asked Questions (FAQ)

- **What is the client experience if the key is invalid?**
  - The client will always receive a `connection_ack` response, even if the API key is invalid. Authentication errors are only reported when a subscription is initiated.
- **Where is the API key expected?**
  - The API key is expected in the `payload` of the `connection_init` message with the key `GOLDRUSH_API_KEY`.
- **What API key formats are supported?**
  - `cqt_wF[26 base58 chars]` or `cqt_rQ[26 base58 chars]`
- **Why should I use the Client SDK?**
  - The Client SDK provides automatic authentication, connection management, retry logic, type safety, and a simplified API for all streaming operations.