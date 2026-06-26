# Streaming API Endpoints

## Connection Details
- **WebSocket:** `wss://streaming.goldrushdata.com/graphql`
- **Protocol:** `graphql-transport-ws`
- **Auth:** `GOLDRUSH_API_KEY` in `connection_init` payload

## Token Search Query

**Operation Identity:**
- Operation ID: `searchToken`
- GraphQL `graphql-query` → field: `searchToken`

**Role:** primary | **API Type:** graphql-query | **Status:** Beta

**Use Cases:** defi-dashboards, trading-intelligence, market-analytics

**Chains:** base-mainnet, eth-mainnet, bsc-mainnet, solana-mainnet, monad-mainnet, matic-mainnet, megaeth-mainnet

This GraphQL query lets you discover actively traded tokens that match a keyword or ticker symbol. Each result includes pricing, volume marketcap, and base/quote metadata. Use it to build comprehensive token search features.

**Credit Cost:** TBD

**Supported Chains:** - `BASE_MAINNET`
- `ETH_MAINNET`
- `BSC_MAINNET`
- `SOLANA_MAINNET`
- `MONAD_MAINNET`
- `POLYGON_MAINNET`
- `MEGAETH_MAINNET`

**This query is currently in Beta.** It is stable for testing and evaluation but may undergo changes in schema or behavior as we continue to improve it. **No API credits are currently charged.**

We welcome your feedback so please **reach out** to us directly to report issues or request features.

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | `string` | Yes | Free-form search string that matches token names or ticker symbols (case-insensitive) or token or pair contract address |
| `chain_name` | `enum` | No | Filter results to a specific chain. |

### Query

You can query the `searchToken` endpoint with:

- Free text (e.g. `"skitten"`)
- Token contract address (e.g. `0x4B6104755AfB5Da4581B81C552DA3A25608c73B8`)
- Token pair address (e.g. `0xa46d5090499eFB9c5dD7d95F7ca69F996b9Fb761`)

The response is sorted in descending order by volume (in USD).

#### Basic Query

```graphql
query {
  searchToken(query: "skitten") {
    pair_address
    chain_name
    quote_rate_usd
    volume_usd
    market_cap
  }
}
```

#### Complete Query

```graphql
query {
  searchToken(query: "skitten", chain_name: BASE_MAINNET) {
    pair_address
    chain_name
    quote_rate
    quote_rate_usd
    volume
    volume_usd
    market_cap
    base_token {
      contract_name
      contract_ticker_symbol
      contract_address
      contract_decimals
    }
    quote_token {
      contract_name
      contract_ticker_symbol
      contract_address
      contract_decimals
    }
  }
}
```

### Response Format

Here's an example of the response data structure:

```json
{
  "data": {
    "searchToken": [
      {
        "pair_address": "0xa46d5090499efb9c5dd7d95f7ca69f996b9fb761",
        "chain_name": "BASE_MAINNET",
        "quote_rate": 2.3637041719e-7,
        "quote_rate_usd": 0.0007961152019156508,
        "volume": 19888966.385959223,
        "volume_usd": 15833.908490251517,
        "market_cap": 786165.7030043972,
        "base_token": {
          "contract_name": "Ski Mask Kitten",
          "contract_ticker_symbol": "SKITTEN",
          "contract_address": "0x4b6104755afb5da4581b81c552da3a25608c73b8",
          "contract_decimals": 18
        },
        "quote_token": {
          "contract_name": "Wrapped Ether",
          "contract_ticker_symbol": "WETH",
          "contract_address": "0x4200000000000000000000000000000000000006",
          "contract_decimals": 18
        }
      }
    ]
  }
}
```

#### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `pair_address` | `string` | Liquidity pool contract that backs the result token/quote pair |
| `chain_name` | `enum` | The blockchain network where the token was created |
| `quote_rate` | `float` | Exchange rate between base and quote tokens |
| `quote_rate_usd` | `float` | USD value of the quote rate |
| `volume` | `float` | 24h trading volume for the pair in quote token units |
| `volume_usd` | `float` | 24h trading volume in USD. |
| `market_cap` | `float` | Estimated market capitalization in USD for the base token |
| `base_token` | `object` | Metadata for the searched token, including address, decimals, name, and ticker symbol |
| `quote_token` | `object` | Metadata for the paired quote asset |

---

## Top Trader Wallets for Token Query

**Operation Identity:**
- Operation ID: `upnlForToken`
- GraphQL `graphql-query` → field: `upnlForToken`

**Role:** specialized | **API Type:** graphql-query | **Status:** Beta

**Use Cases:** defi-dashboards, trading-intelligence, market-analytics, automation-and-agents

**Chains:** base-mainnet, eth-mainnet, bsc-mainnet, matic-mainnet, gnosis-mainnet, optimism-mainnet, megaeth-mainnet

This GraphQL query provides a list of wallets with the highest trading volume for a specific token over the last 30 days, along with detailed information about their holdings, transaction activity, realized and unrealized profit/loss metrics.

**Credit Cost:** TBD

**Supported Chains:** - `BASE_MAINNET`
- `ETH_MAINNET`
- `BSC_MAINNET`
- `POLYGON_MAINNET`
- `GNOSIS_MAINNET`
- `OPTIMISM_MAINNET`
- `MEGAETH_MAINNET`

**This query is currently in Beta.** It is stable for testing and evaluation but may undergo changes in schema or behavior as we continue to improve it. **No API credits are currently charged.**

We welcome your feedback so please **reach out** to us directly to report issues or request features.

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `chain_name` | `enum` | Yes | Chain name to filter events (e.g., `BASE_MAINNET`, `ETH_MAINNET`, `BSC_MAINNET`) |
| `token_address` | `string` | Yes | The deployed token contract address to query |

### Query

You can query the `upnlForToken` endpoint to retrieve top wallet trading data.

#### Basic Query

```graphql
query {
 upnlForToken(
    chain_name: ETH_MAINNET
    token_address: "0x7ABc8A5768E6bE61A6c693a6e4EAcb5B60602C4D"
  ) {
    token_address
    wallet_address
    volume
    balance
    pnl_realized_usd
    pnl_unrealized_usd
  }
}
```

#### Complete Query

```graphql
query {
 upnlForToken(
    chain_name: ETH_MAINNET
    token_address: "0x7ABc8A5768E6bE61A6c693a6e4EAcb5B60602C4D"
  ) {
    token_address
    wallet_address
    volume
    transactions_count
    pnl_realized_usd
    balance
    balance_pretty
    pnl_unrealized_usd
    contract_metadata {
      contract_address
      contract_name
      contract_ticker_symbol
      contract_decimals
    }
  }
}
```

### Response Format

Here's an example of the response data structure:

```json
{
  "data": {
    "upnlForToken": [
      {
        "token_address": "0x7abc8a5768e6be61a6c693a6e4eacb5b60602c4d",
        "wallet_address": "0x91d40e4818f4d4c57b4578d9eca6afc92ac8debe",
        "volume": "56708716",
        "transactions_count": 554,
        "pnl_realized_usd": -43239.81,
        "balance": "32944375440228563000000000",
        "balance_pretty": "32944375.4402",
        "pnl_unrealized_usd": 535182,
        "contract_metadata": {
          "contract_address": "0x7ABc8A5768E6bE61A6c693a6e4EAcb5B60602C4D",
          "contract_name": "Covalent X Token",
          "contract_ticker_symbol": "CXT",
          "contract_decimals": 18
        }
      },
      {
        "token_address": "0x7abc8a5768e6be61a6c693a6e4eacb5b60602c4d",
        "wallet_address": "0xfe97b0c517a84f98fc6ede3cd26b43012d31992a",
        "volume": "39102028",
        "transactions_count": 241,
        "pnl_realized_usd": 8799.58,
        "balance": "323138960338677960000000000",
        "balance_pretty": "323138960.3387",
        "pnl_unrealized_usd": 6417132,
        "contract_metadata": {
          "contract_address": "0x7ABc8A5768E6bE61A6c693a6e4EAcb5B60602C4D",
          "contract_name": "Covalent X Token",
          "contract_ticker_symbol": "CXT",
          "contract_decimals": 18
        }
      }
    ]
  }
}
```

#### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `token_address` | `string` | Token contract address (lowercase, 0x-prefixed) |
| `wallet_address` | `string` | Wallet address of the trader (lowercase, 0x-prefixed) |
| `volume` | `string` | Total token volume transferred in the past 30 days |
| `transactions_count` | `integer` | Transaction count for this wallet and token (past 30 days) |
| `pnl_realized_usd` | `float` | Realized PnL in USD from completed trades |
| `balance` | `string` | Current token balance in raw format |
| `balance_pretty` | `string` | Human-readable balance (4 decimal places) |
| `pnl_unrealized_usd` | `float` | Unrealized PnL in USD at the current token price |
| `contract_metadata` | `object` | Token contract metadata |

---

## Wallet PnL by Token Query

**Operation Identity:**
- Operation ID: `upnlForWallet`
- GraphQL `graphql-query` → field: `upnlForWallet`

**Role:** specialized | **API Type:** graphql-query | **Status:** Beta

**Use Cases:** trading-intelligence, accounting-tax-reporting, portfolio-tracking

**Chains:** base-mainnet, eth-mainnet, bsc-mainnet, matic-mainnet, gnosis-mainnet, optimism-mainnet, megaeth-mainnet

This GraphQL query provides detailed financial metrics, including unrealized and realized profit and loss (PnL), current balance, and transaction insights for each token held by a specific wallet address.

**Credit Cost:** TBD

**Supported Chains:** - `BASE_MAINNET`
- `ETH_MAINNET`
- `BSC_MAINNET`
- `POLYGON_MAINNET`
- `GNOSIS_MAINNET`
- `OPTIMISM_MAINNET`
- `MEGAETH_MAINNET`

**This query is currently in Beta.** It is stable for testing and evaluation but may undergo changes in schema or behavior as we continue to improve it. **No API credits are currently charged.**

We welcome your feedback so please **reach out** to us directly to report issues or request features.

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `chain_name` | `enum` | Yes | Chain name to filter events (e.g., `BASE_MAINNET`, `ETH_MAINNET`, `BSC_MAINNET`) |
| `wallet_address` | `string` | Yes | The wallet address to query |

### Query

You can query the `upnlForWallet` endpoint to retrieve detailed PnL metrics for a wallet.

#### Basic Query

```graphql
query {
 upnlForWallet(
    chain_name: ETH_MAINNET
    wallet_address: "0xfe97b0C517a84F98fc6eDe3CD26B43012d31992a"
  ) {
    token_address
    cost_basis
    current_price
    pnl_realized_usd
    pnl_unrealized_usd
    net_balance_change
  }
}
```

#### Complete Query

```graphql
query{
upnlForWallet(
    chain_name:ETH_MAINNET,
    wallet_address:"0xfe97b0C517a84F98fc6eDe3CD26B43012d31992a"
  ) {
    token_address
    cost_basis
    current_price
    pnl_realized_usd
    pnl_unrealized_usd
    net_balance_change
    marketcap_usd
    contract_metadata {
      contract_address
      contract_name
      contract_ticker_symbol
      contract_decimals
    }
  }
}
```

### Response Format

Here's an example of the response data structure:

```json
{
  "data": {
    "upnlForWallet": [
      {
        "token_address": "0x7abc8a5768e6be61a6c693a6e4eacb5b60602c4d",
        "cost_basis": 0.03219392,
        "current_price": 0.032418,
        "pnl_realized_usd": null,
        "pnl_unrealized_usd": 318.22842,
        "net_balance_change": "1420158",
        "marketcap_usd": "32418001.4431",
        "contract_metadata": {
          "contract_address": "0x7abc8a5768e6be61a6c693a6e4eacb5b60602c4d",
          "contract_name": "Covalent X Token",
          "contract_ticker_symbol": "CXT",
          "contract_decimals": 18
        }
      }
    ]
  }
}
```

#### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `token_address` | `string` | Token contract address (lowercase, 0x-prefixed) |
| `cost_basis` | `float` | Average cost basis per token in USD |
| `current_price` | `float` | Current market price per token in USD |
| `pnl_realized_usd` | `float` | Realized PnL in USD from completed trades |
| `pnl_unrealized_usd` | `float` | Unrealized PnL in USD at the latest price |
| `net_balance_change` | `string` | Net token movement (inflow minus outflow, past 7 days) |
| `marketcap_usd` | `string` | Estimated market capitalization in USD |
| `contract_metadata` | `object` | Token contract metadata |

---

## New DEX Pairs Stream

**Operation Identity:**
- Operation ID: `newPairs`
- GraphQL `graphql-subscription` → field: `newPairs`
- SDK: `StreamingService.subscribeToNewPairs()`

**Role:** primary | **API Type:** graphql-subscription | **Status:** Beta

**Use Cases:** trading-intelligence, price-discovery-feeds, defi-dashboards, automation-and-agents

**Chains:** base-mainnet, eth-mainnet, bsc-mainnet, sonic-mainnet, solana-mainnet, monad-mainnet, hyperevm-mainnet, matic-mainnet, megaeth-mainnet

The New DEX Pairs stream provides real-time updates when **new liquidity pairs** are created on decentralized exchanges (DEXes). This documentation follows our standard streaming API structure.

**Credit Cost:** TBD

**Supported Chains:** - `BASE_MAINNET`
- `ETH_MAINNET`
- `BSC_MAINNET`
- `SONIC_MAINNET`
- `SOLANA_MAINNET`
- `MONAD_MAINNET`
- `HYPEREVM_MAINNET`
- `POLYGON_MAINNET`
- `MEGAETH_MAINNET`

**This stream is currently in Beta.** It is stable for testing and evaluation but may undergo changes in schema or behavior as we continue to improve it. **No API credits are currently charged.** 

We welcome your feedback so please **reach out** to us directly to report issues or request features.

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `chain_name` | `enum` | Yes | Chain name to filter events (e.g., `BASE_MAINNET`, `ETH_MAINNET`, `BSC_MAINNET`, `SOLANA_MAINNET`) |
| `protocols` | `array` | Yes | List of protocol name enums to filter events (e.g.,`[UNISWAP_V2, RAYDIUM_AMM]`); see **supported DEXes** for the full list. |

### Subscription

You can subscribe to the `newPairs` endpoint to receive events.

#### Basic Subscription Query

```graphql
subscription {
  newPairs(chain_name: BASE_MAINNET, protocols: [UNISWAP_V2, UNISWAP_V3]) {
    chain_name
    protocol
    protocol_version
    tx_hash
    block_signed_at
  }
}
```

#### Complete Subscription Query

```graphql
subscription {
  newPairs(chain_name: BASE_MAINNET, protocols: [UNISWAP_V2, UNISWAP_V3]) {
    chain_name
    protocol
    protocol_version
    pair_address
    deployer_address
    tx_hash
    block_signed_at
    liquidity
    supply
    market_cap
    event_name
    quote_rate
    quote_rate_usd
    base_token {
      contract_address
      contract_decimals
      contract_name
      contract_ticker_symbol
    }
    pair {
      contract_address
      contract_decimals
      contract_name
      contract_ticker_symbol
    }
    quote_token {
      contract_address
      contract_decimals
      contract_name
      contract_ticker_symbol
    }
  }
}
```

### Response Format

Here's an example of the response data structure:

```json
{
  "data": {
    "newPairs": [
      {
        "chain_name": "base",
        "protocol": "uniswap",
        "protocol_version": "3",
        "pair_address": "0xa7dfb58a6e0d675c19f76dfd3b8b80a3a4814728",
        "deployer_address": "0x33128a8fc17869897dce68ed026d694621f6fdfd",
        "tx_hash": "0x5374c0182580ff2b3e868f58bdce697f3e4256baebc6f6e8db008fadb32d6253",
        "block_signed_at": "2025-05-28T22:01:41Z",
        "liquidity": 177.50267302070574,
        "supply": 1000000000,
        "market_cap": 6153.261270529,
        "event_name": "PoolCreated",
        "quote_rate": 0.000006153261270529,
        "quote_rate_usd": 0.000006153261270529,
        "base_token": {
          "contract_address": "0x8ac05571b525dd555320df58a40a0c0ab6d807c7",
          "contract_decimals": 18,
          "contract_name": "GOAT",
          "contract_ticker_symbol": "GOAT"
        },
        "quote_token": {
          "contract_address": "0x1111111111166b7fe7bd91427724b487980afc69",
          "contract_decimals": 18,
          "contract_name": "Zora",
          "contract_ticker_symbol": "ZORA"
        },
        "pair": {
          "contract_address": "0xa7dfb58a6e0d675c19f76dfd3b8b80a3a4814728",
          "contract_decimals": 18,
          "contract_name": "GOAT-ZORA Pool",
          "contract_ticker_symbol": "GOAT-ZORA"
        }
      }
    ]
  }
}
```

#### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `chain_name` | `string` | The blockchain network where the pair was created |
| `protocol` | `string` | DEX protocol name (e.g., "uniswap", "pancakeswap") |
| `protocol_version` | `string` | Version of the DEX protocol |
| `pair_address` | `string` | Address of the new pair contract |
| `deployer_address` | `string` | Address that deployed the pair contract |
| `tx_hash` | `string` | Transaction hash of the pair creation |
| `block_signed_at` | `string` | ISO timestamp of when the block was signed |
| `liquidity` | `float` | Initial liquidity amount (in USD) |
| `supply` | `integer` | Total supply of the pair token |
| `market_cap` | `float` | Market capitalization in USD |
| `event_name` | `string` | Name of the contract event (e.g., "PoolCreated") |
| `quote_rate` | `float` | Exchange rate between base and quote tokens |
| `quote_rate_usd` | `float` | USD value of the quote rate |
| `base_token` | `object` | Metadata for the base token including contract address, decimals, name, and symbol |
| `quote_token` | `object` | Metadata for the quote token including contract address, decimals, name, and symbol |
| `pair` | `object` | Metadata for the pair including contract address, decimals, name, and symbol |

---

## OHLCV Pairs Stream

**Operation Identity:**
- Operation ID: `ohlcvCandlesForPair`
- GraphQL `graphql-subscription` → field: `ohlcvCandlesForPair`
- SDK: `StreamingService.subscribeToOHLCVPairs()`

**Role:** primary | **API Type:** graphql-subscription | **Status:** Beta

**Use Cases:** price-discovery-feeds, trading-intelligence, automation-and-agents

**Chains:** sonic-mainnet, base-mainnet, bsc-mainnet, eth-mainnet, solana-mainnet, monad-mainnet, hyperevm-mainnet, matic-mainnet, megaeth-mainnet

The OHLCV Pairs stream provides real-time updates on the Open, High, Low, Close prices and Volume of ** one or many token pairs** at configurable intervals. This documentation follows our standard streaming API structure.

**Credit Cost:** TBD

**Supported Chains:** - `SONIC_MAINNET`
- `BASE_MAINNET`
- `BSC_MAINNET`
- `ETH_MAINNET`
- `SOLANA_MAINNET`
- `MONAD_MAINNET`
- `HYPEREVM_MAINNET`
- `POLYGON_MAINNET`
- `MEGAETH_MAINNET`

**This stream is currently in Beta.** It is stable for testing and evaluation but may undergo changes in schema or behavior as we continue to improve it. **No API credits are currently charged.** 

We welcome your feedback so please **reach out** to us directly to report issues or request features.

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `chain_name` | `enum` | Yes | Chain name to filter events (e.g. `BASE_MAINNET`, `ETH_MAINNET`, `BSC_MAINNET`, `SOLANA_MAINNET`) |
| `pair_addresses` | `array` | Yes | Array of pair addresses on **supported DEXes** and chains to track |
| `interval` | `enum` | Yes | Frequency of OHLCV data updates, ranging from sub-second to one day |
| `timeframe` | `enum` | Yes | Historical lookback period for OHLCV data, ranging from one minute to one month |
| `limit` | `int` | No | Maximum number of items returned per stream message to control payload size |

### Subscription

You can subscribe to the `ohlcvCandlesForPair` endpoint to receive the pricing events.

#### Basic Subscription Query

```graphql
subscription {
  ohlcvCandlesForPair(
    chain_name: BASE_MAINNET
    pair_addresses: ["0x9c087Eb773291e50CF6c6a90ef0F4500e349B903"]
    interval: ONE_MINUTE
    timeframe: ONE_HOUR
  ) {
    chain_name
    pair_address
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
  }
}
```

#### Complete Subscription Query

```graphql
subscription {
  ohlcvCandlesForPair(
    chain_name: BASE_MAINNET
    pair_addresses: [
      "0x9c087Eb773291e50CF6c6a90ef0F4500e349B903"
      "0x4b0Aaf3EBb163dd45F663b38b6d93f6093EBC2d3"
    ]
    interval: ONE_MINUTE
    timeframe: ONE_HOUR
    limit: 1000
  ) {
    chain_name
    pair_address
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
    quote_token {
      contract_name
      contract_address
      contract_decimals
      contract_ticker_symbol
    }
  }
}
```

### Response Format

Here's an example of the response data structure:

```json
{
  "data": {
    "ohlcvCandlesForPair": [
      {
        "chain_name": "BASE_MAINNET",
        "pair_address": "0x4b0Aaf3EBb163dd45F663b38b6d93f6093EBC2d3",
        "interval": "ONE_MINUTE",
        "timeframe": "ONE_HOUR",
        "timestamp": "2025-05-29T19:53:00Z",
        "open": 4113151.389790023,
        "high": 4196665.022060752,
        "low": 4113151.389790023,
        "close": 4196665.022060752,
        "volume": 325.7615900713698,
        "volume_usd": 0.2079461510855417,
        "quote_rate": 4196665.022060752,
        "quote_rate_usd": 0.0006319231563715365,
        "quote_token": {
          "contract_name": "Wrapped Ether",
          "contract_symbol": "WETH",
          "contract_address": "0x4200000000000000000000000000000000000006",
          "contract_decimals": 18
        },
        "base_token": {
          "contract_name": "Toshi",
          "contract_symbol": "TOSHI",
          "contract_address": "0xac1bd2486aaf3b5c0fc3fd868558b082a531b2b4",
          "contract_decimals": 18
        }
      }
    ]
  }
}
```

#### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `chain_name` | `string` | The blockchain network where the pair exists |
| `pair_address` | `string` | The address of the DEX pair |
| `interval` | `enum` | The candle interval |
| `timeframe` | `enum` | The requested timeframe |
| `timestamp` | `string` | ISO timestamp for the candle |
| `open` | `float` | Opening price for the interval |
| `high` | `float` | Highest price during the interval |
| `low` | `float` | Lowest price during the interval |
| `close` | `float` | Closing price for the interval |
| `volume` | `float` | Trading volume during the interval |
| `volume_usd` | `float` | Trading volume in USD |
| `quote_rate` | `float` | Exchange rate between base and quote tokens |
| `quote_rate_usd` | `float` | USD value of the quote rate |
| `base_token` | `object` | Information about the base token in the pair |
| `quote_token` | `object` | Information about the quote token in the pair |

---

## OHLCV Tokens Stream

**Operation Identity:**
- Operation ID: `ohlcvCandlesForToken`
- GraphQL `graphql-subscription` → field: `ohlcvCandlesForToken`
- SDK: `StreamingService.subscribeToOHLCVTokens()`

**Role:** primary | **API Type:** graphql-subscription | **Status:** Beta

**Use Cases:** price-discovery-feeds, trading-intelligence, automation-and-agents

**Chains:** sonic-mainnet, base-mainnet, bsc-mainnet, eth-mainnet, solana-mainnet, monad-mainnet, hypercore-mainnet, hyperevm-mainnet, matic-mainnet, megaeth-mainnet

The OHLCV Tokens stream provides real-time updates on the Open, High, Low, Close prices and Volume of **one or many tokens** at configurable intervals. This documentation follows our standard streaming API structure.

**Credit Cost:** TBD

**Supported Chains:** - `SONIC_MAINNET`
- `BASE_MAINNET`
- `BSC_MAINNET`
- `ETH_MAINNET`
- `SOLANA_MAINNET`
- `MONAD_MAINNET`
- `HYPERCORE_MAINNET`
- `HYPEREVM_MAINNET`
- `POLYGON_MAINNET`
- `MEGAETH_MAINNET`

**This stream is currently in Beta.** It is stable for testing and evaluation but may undergo changes in schema or behavior as we continue to improve it. **No API credits are currently charged.** 

We welcome your feedback so please **reach out** to us directly to report issues or request features.

### Supported Token Price Feeds

In addition to DEX-sourced prices, this stream supports institutional-grade price feeds from the following providers:

| Provider | Description |
|---|---|
| [Redstone Bolt](https://redstone.finance/) | Ultra-low-latency CEX price feeds updated every **2.4 ms** (~400 updates/sec). Bolt nodes are co-located with chain sequencer infrastructure and aggregate prices from **Binance, Coinbase, OKX, Bitget, and Kraken**. |

Pass the feed name in the `token_addresses` array with `chain_name` set to the feed's chain name.

| Feed Name | Asset | Chain Name |
|---|---|---|
| `REDSTONE-BTC` | Bitcoin | `MEGAETH_MAINNET` |
| `REDSTONE-ETH` | Ethereum | `MEGAETH_MAINNET` |
| `REDSTONE-SOL` | Solana | `MEGAETH_MAINNET` |
| `REDSTONE-BNB` | BNB | `MEGAETH_MAINNET` |
| `REDSTONE-XRP` | XRP | `MEGAETH_MAINNET` |
| `REDSTONE-ADA` | Cardano | `MEGAETH_MAINNET` |
| `REDSTONE-DOGE` | Dogecoin | `MEGAETH_MAINNET` |
| `REDSTONE-USDT` | Tether | `MEGAETH_MAINNET` |
| `REDSTONE-USDC` | USD Coin | `MEGAETH_MAINNET` |

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `chain_name` | `enum` | Yes | Chain name to filter events (e.g. `BASE_MAINNET`, `ETH_MAINNET`, `BSC_MAINNET`, `SOLANA_MAINNET`) |
| `token_addresses` | `array` | Yes | Array of token addresses on **supported DEXes** and chains to track |
| `interval` | `enum` | Yes | Frequency of OHLCV data updates, ranging from sub-second to one day |
| `timeframe` | `enum` | Yes | Historical lookback period for OHLCV data, ranging from one minute to one month |
| `limit` | `int` | No | Maximum number of items returned per stream message to control payload size |

### Subscription

You can subscribe to the `ohlcvCandlesForToken` endpoint to receive the pricing events.

#### Basic Subscription Query

```graphql
subscription {
  ohlcvCandlesForToken(
    chain_name: BASE_MAINNET
    token_addresses: ["0x4B6104755AfB5Da4581B81C552DA3A25608c73B8"]
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
```

#### Complete Subscription Query

```graphql
subscription {
  ohlcvCandlesForToken(
    chain_name: BASE_MAINNET
    token_addresses: [
      "0x4B6104755AfB5Da4581B81C552DA3A25608c73B8"
    ]
    interval: ONE_MINUTE
    timeframe: ONE_HOUR
    limit: 1000
  ) {
    chain_name
    pair_address
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
    quote_token {
      contract_name
      contract_address
      contract_decimals
      contract_ticker_symbol
    }
  }
}
```

### Response Format

Here's an example of the response data structure:

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

#### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `chain_name` | `string` | The blockchain network where the token exists |
| `pair_address` | `string` | The address of the primary DEX pool with the most liquidity for the token |
| `interval` | `enum` | The candle interval |
| `timeframe` | `enum` | The requested timeframe |
| `timestamp` | `string` | ISO timestamp for the candle |
| `open` | `float` | Opening price for the interval |
| `high` | `float` | Highest price during the interval |
| `low` | `float` | Lowest price during the interval |
| `close` | `float` | Closing price for the interval |
| `volume` | `float` | Trading volume during the interval |
| `volume_usd` | `float` | Trading volume in USD |
| `quote_rate` | `float` | Exchange rate between base and quote tokens |
| `quote_rate_usd` | `float` | USD value of the quote rate |
| `base_token` | `object` | Information about the queried token |
| `quote_token` | `object` | Information about the paired token of the primary DEX pool |

---

## Update Pairs Stream

**Operation Identity:**
- Operation ID: `updatePairs`
- GraphQL `graphql-subscription` → field: `updatePairs`
- SDK: `StreamingService.subscribeToUpdatePairs()`

**Role:** primary | **API Type:** graphql-subscription | **Status:** Beta

**Use Cases:** price-discovery-feeds, trading-intelligence, defi-dashboards, automation-and-agents

**Chains:** base-mainnet, eth-mainnet, bsc-mainnet, sonic-mainnet, solana-mainnet, monad-mainnet, hyperevm-mainnet, matic-mainnet, megaeth-mainnet

The Update Pairs stream provides real-time updates on the prices, volumes, market cap and liquidity of ** one or many token pairs**. This documentation follows our standard streaming API structure.

**Credit Cost:** TBD

**Supported Chains:** - `BASE_MAINNET`
- `ETH_MAINNET`
- `BSC_MAINNET`
- `SONIC_MAINNET`
- `SOLANA_MAINNET`
- `MONAD_MAINNET`
- `HYPEREVM_MAINNET`
- `POLYGON_MAINNET`
- `MEGAETH_MAINNET`

**This stream is currently in Beta.** It is stable for testing and evaluation but may undergo changes in schema or behavior as we continue to improve it. **No API credits are currently charged.** 

We welcome your feedback so please **reach out** to us directly to report issues or request features.

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `chain_name` | `enum` | Yes | Chain name to filter events (e.g. `BASE_MAINNET`, `ETH_MAINNET`, `BSC_MAINNET`, `SOLANA_MAINNET`) |
| `pair_addresses` | `array` | Yes | Array of pair addresses on **supported DEXes** and chains to track |

### Subscription

You can subscribe to the `updatePairs` endpoint to receive the events.

#### Basic Subscription Query

```graphql
subscription {
  updatePairs(
    chain_name: BASE_MAINNET
    pair_addresses: ["0x9c087Eb773291e50CF6c6a90ef0F4500e349B903"]
  ) {
    chain_name
    pair_address
    timestamp
    quote_rate
    quote_rate_usd
    volume
    volume_usd
    market_cap
    liquidity
  }
}
```

#### Complete Subscription Query

```graphql
subscription {
  updatePairs(
    chain_name: BASE_MAINNET
    pair_addresses: [
      "0x9c087Eb773291e50CF6c6a90ef0F4500e349B903"
      "0x4b0Aaf3EBb163dd45F663b38b6d93f6093EBC2d3"
    ]
  ) {
    chain_name
    pair_address
    timestamp
    quote_rate
    quote_rate_usd
    volume
    volume_usd
    market_cap
    liquidity
    base_token {
      contract_name
      contract_address
      contract_decimals
      contract_ticker_symbol
    }
    quote_token {
      contract_name
      contract_address
      contract_decimals
      contract_ticker_symbol
    }
    price_deltas {
      last_5m
      last_1hr
      last_6hr
      last_24hr
    }
    swap_counts {
      last_5m
      last_1hr
      last_6hr
      last_24hr
    }
  }
}
```

### Response Format

Here's an example of the response data structure:

```json
{
  "data": {
    "updatePairs": [
      {
        "chain_name": "BASE_MAINNET",
        "pair_address": "0x9c087Eb773291e50CF6c6a90ef0F4500e349B903",
        "quote_rate": 0.0002962,
        "quote_rate_usd": 1.39,
        "volume": 0.2079461510855417,
        "volume_usd": 975.515187,
        "quote_token": {
          "contract_name": "Wrapped Ether",
          "contract_symbol": "WETH",
          "contract_address": "0x4200000000000000000000000000000000000006",
          "contract_decimals": 18
        },
        "base_token": {
          "contract_name": "Virtual",
          "contract_symbol": "VIRTUAL",
          "contract_address": "0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b",
          "contract_decimals": 18
        },
        "swap_counts": {
          "last_5m": 10,
          "last_1hr": 100,
          "last_6hr": 1000,
          "last_24hr": 10000
        },
        "price_deltas": {
          "last_5m": 1.2,
          "last_1hr": 1.9,
          "last_6hr": 2.7,
          "last_24hr": -9.1
        }
      }
    ]
  }
}
```

#### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `chain_name` | `string` | The blockchain network where the pair exists |
| `pair_address` | `string` | The address of the DEX pair |
| `quote_rate` | `float` | Exchange rate between base and quote tokens |
| `quote_rate_usd` | `float` | Exchange rate between base and quote tokens in USD |
| `volume` | `float` | Trading volume during the interval |
| `volume_usd` | `float` | Trading volume in USD |
| `base_token` | `object` | Information about the base token in the pair |
| `quote_token` | `object` | Information about the quote token in the pair |
| `swap_counts` | `object` | Swap counts for last 5m, 1hr, 6hr, 24hr |
| `price_deltas` | `object` | Price deltas for last 5m, 1hr, 6hr, 24hr |

---

## Wallet Activity Stream

**Operation Identity:**
- Operation ID: `walletTxs`
- GraphQL `graphql-subscription` → field: `walletTxs`
- SDK: `StreamingService.subscribeToWalletActivity()`

**Role:** primary | **API Type:** graphql-subscription | **Status:** Beta

**Use Cases:** trading-intelligence, automation-and-agents, onchain-gaming-infrastructure, defi-dashboards

**Chains:** base-mainnet, eth-mainnet, bsc-mainnet, sonic-mainnet, monad-mainnet, hypercore-mainnet, hyperevm-mainnet, matic-mainnet, megaeth-mainnet

The Wallet Activity stream provides real-time updates on wallet **transactions, token transfers, and interactions with smart contracts **. This documentation follows our standard Streaming API structure.

**Credit Cost:** TBD

**Supported Chains:** - `BASE_MAINNET`
- `ETH_MAINNET`
- `BSC_MAINNET`
- `SONIC_MAINNET`
- `MONAD_MAINNET`
- `HYPERCORE_MAINNET`
- `HYPEREVM_MAINNET`
- `POLYGON_MAINNET`
- `MEGAETH_MAINNET`

**This stream is currently in Beta.** It is stable for testing and evaluation but may undergo changes in schema or behavior as we continue to improve it. **No API credits are currently charged.** 

We welcome your feedback so please **reach out** to us directly to report issues or request features.

### Supported Actions

All transactions are returned as raw data, but the following transaction types are decoded:

- **Transfer**
- **Swap**
- **Bridge**
- **Deposit**
- **Withdraw**
- **Approve**

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `chain_name` | `enum` | Yes | Chain name to filter events (e.g. `BASE_MAINNET`, `ETH_MAINNET`, `BSC_MAINNET`) |
| `wallet_addresses` | `array` | Yes | Addresses to track |

### Subscription

You can subscribe to the `walletTxs` endpoint to receive events.

#### Basic Subscription Query

```graphql
subscription {
  walletTxs(
    chain_name: BASE_MAINNET,
    wallet_addresses: [
        "0x4200000000000000000000000000000000000006",
        "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    ]) {
        block_signed_at
        block_height
        tx_hash
        tx_offset
        successful
        decoded_type
  }
}
```

#### Complete Subscription Query

```graphql
subscription {
  walletTxs(
    chain_name: BASE_MAINNET,
    wallet_addresses: [
      "0x198ef79f1f515f02dfe9e3115ed9fc07183f02fc",
      "0x4200000000000000000000000000000000000006"
    ]
  ) {
    tx_hash
    from_address
    to_address
    value
    chain_name
    block_signed_at
    block_height
    block_hash
    miner_address
    gas_used
    tx_offset
    successful
    decoded_type

    decoded_details {
      ... on TransferTransaction {
        from
        to
        amount
        quote_usd
        quote_rate_usd
        contract_metadata {
          contract_name
          contract_address
          contract_decimals
          contract_ticker_symbol
        }
      }
      ... on SwapTransaction {
        token_in {
          contract_address
          contract_decimals
          contract_ticker_symbol
        }
        token_out {
          contract_address
          contract_decimals
          contract_ticker_symbol
        }
        amount_in
        amount_out
      }
      ... on BridgeTransaction {
        type
        typeString
        from
        to
        amount
        quote_usd
        quote_rate_usd
        contract_metadata {
          contract_name
          contract_address
          contract_decimals
          contract_ticker_symbol
        }
      }
      ... on DepositTransaction {
        from
        to
        amount
        quote_usd
        quote_rate_usd
        contract_metadata {
          contract_name
          contract_address
          contract_decimals
          contract_ticker_symbol
        }
      }
      ... on WithdrawTransaction {
        from
        to
        amount
        quote_usd
        quote_rate_usd
        contract_metadata {
          contract_name
          contract_address
          contract_decimals
          contract_ticker_symbol
        }
      }
      ... on ApproveTransaction {
        spender
        amount
        quote_usd
        quote_rate_usd
        contract_metadata {
          contract_name
          contract_address
          contract_decimals
          contract_ticker_symbol
        }
      }
      ... on ErrorDetails {
        message
      }
    }

    logs {
      emitter_address
      log_offset
      data
      topics
    }
  }
}
```

### Response Format

Here's an example of the response data structure:

```json
{
  "data": {
    "walletTxs": [
      {
        "tx_hash": "0x23a4f9710c23678a8c6ae25d7e3aa75a82866231e9bd541114046c5a710a8355",
        "from_address": "0xd2216ed62a5c84f285a051839e808902fe8fc90b",
        "to_address": "0x198ef79f1f515f02dfe9e3115ed9fc07183f02fc",
        "value": 0,
        "chain_name": "base-mainnet",
        "block_signed_at": "2025-05-29T19:27:25Z",
        "block_height": 30878749,
        "block_hash": "0x2435aec7c20678ee82ae251ab1066e15ed3dac7ff0ea086c44ee8476a721abde",
        "miner_address": "0x4200000000000000000000000000000000000011",
        "gas_used": 195861,
        "tx_offset": 118,
        "successful": true,
        "decoded_type": "SWAP",
        "decoded": {
          "token_in": {
            "contract_address": "0x4200000000000000000000000000000000000006",
            "contract_decimals": 18,
            "contract_ticker_symbol": "WETH"
          },
          "token_out": {
            "contract_address": "0x14b2f229097df3c92b43ea871860e3fae08d7f06",
            "contract_decimals": 18,
            "contract_ticker_symbol": "EXAMPLE"
          },
          "amount_in": "258844786659364206700114",
          "amount_out": "66094025142553271"
        },
        "logs": [
          {
            "emitter": "0x4200000000000000000000000000000000000006",
            "topics": [
              "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
              "0x000000000000000000000000286f3add5dd41ba6e208f9f9a68533107fd0d0fa",
              "0x000000000000000000000000198ef79f1f515f02dfe9e3115ed9fc07183f02fc"
            ]
          },
          {
            "emitter": "0x14b2f229097df3c92b43ea871860e3fae08d7f06",
            "topics": [
              "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
              "0x000000000000000000000000d2216ed62a5c84f285a051839e808902fe8fc90b",
              "0x000000000000000000000000286f3add5dd41ba6e208f9f9a68533107fd0d0fa"
            ]
          },
          {
            "emitter": "0x286f3add5dd41ba6e208f9f9a68533107fd0d0fa",
            "topics": [
              "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
              "0x000000000000000000000000198ef79f1f515f02dfe9e3115ed9fc07183f02fc",
              "0x000000000000000000000000198ef79f1f515f02dfe9e3115ed9fc07183f02fc"
            ]
          },
          {
            "emitter": "0x4200000000000000000000000000000000000006",
            "topics": [
              "0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65",
              "0x000000000000000000000000198ef79f1f515f02dfe9e3115ed9fc07183f02fc"
            ]
          }
        ]
      }
    ]
  }
}
```

#### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `tx_hash` | `string` | The transaction hash |
| `from_address` | `string` | The sender's address |
| `to_address` | `string` | The recipient's address |
| `value` | `integer` | The transaction value in native currency |
| `chain_name` | `string` | The blockchain network where the transaction occurred |
| `block_signed_at` | `string` | ISO timestamp of when the block was signed |
| `block_height` | `integer` | The block number where the transaction was included |
| `block_hash` | `string` | The hash of the block containing the transaction |
| `miner_address` | `string` | The address of the block miner |
| `gas_used` | `integer` | The amount of gas used by the transaction |
| `tx_offset` | `integer` | The position of the transaction in the block |
| `successful` | `boolean` | Whether the transaction was successful |
| `decoded_type` | `string` | The type of decoded event (e.g., "SWAP") |
| `decoded` | `object` | The decoded event data (varies by event type) |
| `logs` | `array` | Array of event logs emitted during the transaction |

### Decoded Events

Note from the [Complete Subscription Query](#complete-subscription-query), this stream decodes events which you can fetch with fragment spreads. See the full schema of available **decoded events**.

---

# Decoded Events

The following events are decoded in the GoldRush Streaming API:

- [Transfer](#transfer-event)
- [Swap](#swap-event)
- [Bridge](#bridge-event)
- [Deposit](#deposit-event)
- [Withdraw](#withdraw-event)
- [Approve](#approve-event)

## Transfer Event

| Field                  | Type     | Description                                        |
| ---------------------- | -------- | -------------------------------------------------- |
| `from`           | `string` | The source address  |
| `to`             | `string` | The destination address |
| `amount`     | `string` | Unscaled token amount (scale by `metadata.contract_decimals`) |
| `quote_rate_usd`     | `string` | Exchange rate of the token in USD             |
| `quote_usd`     | `string` | The quote amount of the token in USD            |
| `contract_metadata` | `object` | Contract details including `contract_name`, `contract_address`, `contract_decimals`, and `contract_ticker_symbol` |

## Swap Event

| Field                  | Type     | Description                                        |
| ---------------------- | -------- | -------------------------------------------------- |
| `token_in`           | `object` | The input token details including `contract_address`, `contract_decimals`, and `contract_ticker_symbol` |
| `token_out`             | `object` | The output token details including `contract_address`, `contract_decimals`, and `contract_ticker_symbol` |
| `amount_in`     | `string` | The amount of input tokens |
| `amount_out`     | `string` | The amount of output tokens |

## Bridge Event

| Field                  | Type     | Description                                        |
| ---------------------- | -------- | -------------------------------------------------- |
| `type`           | `string` | The bridge transaction type |
| `typeString`             | `string` | Human-readable bridge transaction type |
| `from`     | `string` | The source address |
| `to`     | `string` | The destination address |
| `amount`     | `string` | Unscaled token amount (scale by `metadata.contract_decimals`) |
| `quote_rate_usd`     | `string` | Exchange rate of the token in USD |
| `quote_usd`     | `string` | The quote amount of the token in USD |
| `contract_metadata` | `object` | Contract details including `contract_name`, `contract_address`, `contract_decimals`, and `contract_ticker_symbol` |

## Deposit Event

| Field                  | Type     | Description                                        |
| ---------------------- | -------- | -------------------------------------------------- |
| `from`           | `string` | The source address |
| `to`             | `string` | The destination address |
| `amount`     | `string` | Unscaled token amount (scale by `metadata.contract_decimals`) |
| `quote_rate_usd`     | `string` | Exchange rate of the token in USD |
| `quote_usd`     | `string` | The quote amount of the token in USD |
| `contract_metadata` | `object` | Contract details including `contract_name`, `contract_address`, `contract_decimals`, and `contract_ticker_symbol` |

## Withdraw Event

| Field                  | Type     | Description                                        |
| ---------------------- | -------- | -------------------------------------------------- |
| `from`           | `string` | The source address |
| `to`             | `string` | The destination address |
| `amount`     | `string` | Unscaled token amount (scale by `metadata.contract_decimals`) |
| `quote_rate_usd`     | `string` | Exchange rate of the token in USD |
| `quote_usd`     | `string` | The quote amount of the token in USD |
| `contract_metadata` | `object` | Contract details including `contract_name`, `contract_address`, `contract_decimals`, and `contract_ticker_symbol` |

## Approve Event

| Field                  | Type     | Description                                        |
| ---------------------- | -------- | -------------------------------------------------- |
| `spender`           | `string` | The address approved to spend tokens |
| `amount`     | `string` | Unscaled token amount (scale by `metadata.contract_decimals`) |
| `quote_rate_usd`     | `string` | Exchange rate of the token in USD |
| `quote_usd`     | `string` | The quote amount of the token in USD |
| `contract_metadata` | `object` | Contract details including `contract_name`, `contract_address`, `contract_decimals`, and `contract_ticker_symbol` |

## Transaction Logs

| Field                  | Type     | Description                                        |
| ---------------------- | -------- | -------------------------------------------------- |
| `emitter_address`           | `string` | The address that emitted the log |
| `log_offset`             | `integer` | The offset of the log in the transaction |
| `data`     | `string` | The raw log data |
| `topics`     | `array` | Array of log topics |

## Error Details

| Field                  | Type     | Description                                        |
| ---------------------- | -------- | -------------------------------------------------- |
| `message`           | `string` | Error message describing what went wrong |
