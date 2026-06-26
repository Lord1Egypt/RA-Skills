# Streaming API SDK Guide

With the official [TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk), developers can access the Streaming API and leverage the following advanced features described in this guide. 

```bash
npm install @covalenthq/client-sdk
```

## Basic Subscription
The following code sample shows how to set up a subscription to the OHLCV Pairs stream: 

```typescript GoldRush SDK
import {
  GoldRushClient,
  StreamingChain,
  StreamingInterval,
  StreamingTimeframe,
  StreamingProtocol,
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

// Subscribe to OHLCV data for trading pairs
const unsubscribeOhlcvPairs = client.StreamingService.subscribeToOHLCVPairs(
  {
    chain_name: StreamingChain.BASE_MAINNET,
    pair_addresses: ["0x9c087Eb773291e50CF6c6a90ef0F4500e349B903"],
    interval: StreamingInterval.ONE_MINUTE,
    timeframe: StreamingTimeframe.ONE_HOUR,
  },
  {
    next: (data) => {
      console.log("Received OHLCV pair data:", data);
    },
    error: (error) => {
      console.error("Streaming error:", error);
    },
    complete: () => {
      console.log("Stream completed");
    },
  }
);

// Unsubscribe when done
unsubscribeOhlcvPairs();

// Disconnect from streaming service when finished
await client.StreamingService.disconnect();
```

## Multiple Subscriptions
The SDK uses a singleton WebSocket client internally, allowing you to create multiple subscriptions through the same GoldRushClient.

```typescript GoldRush SDK
import {
  GoldRushClient,
  StreamingChain,
  StreamingInterval,
  StreamingTimeframe,
  StreamingProtocol,
} from "@covalenthq/client-sdk";

// Create a single client
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

// Create multiple subscriptions through the same connection
const unsubscribePairs = client.StreamingService.subscribeToOHLCVPairs(
  {
    chain_name: StreamingChain.BASE_MAINNET,
    pair_addresses: ["0x9c087Eb773291e50CF6c6a90ef0F4500e349B903"],
    interval: StreamingInterval.ONE_MINUTE,
    timeframe: StreamingTimeframe.ONE_HOUR,
  },
  {
    next: (data) => console.log("OHLCV Pairs:", data),
  }
);

const unsubscribeTokens = client.StreamingService.subscribeToOHLCVTokens(
  {
    chain_name: StreamingChain.BASE_MAINNET,
    token_addresses: ["0x4B6104755AfB5Da4581B81C552DA3A25608c73B8"],
    interval: StreamingInterval.ONE_MINUTE,
    timeframe: StreamingTimeframe.ONE_HOUR,
  },
  {
    next: (data) => console.log("OHLCV Tokens:", data),
  }
);

const unsubscribeWallet = client.StreamingService.subscribeToWalletActivity(
  {
    chain_name: StreamingChain.BASE_MAINNET,
    wallet_addresses: ["0xbaed383ede0e5d9d72430661f3285daa77e9439f"],
  },
  {
    next: (data) => console.log("Wallet Activity:", data),
  }
);

// Unsubscribe from individual streams when needed
unsubscribePairs();
unsubscribeTokens();
unsubscribeWallet();

// Or disconnect from all streams at once
await client.StreamingService.disconnect();
```

## React Integration
For React applications, use the `useEffect` hook to properly manage subscription lifecycle:

```typescript GoldRush SDK
useEffect(() => {
  const unsubscribe = client.StreamingService.rawQuery(
    `subscription {
        ohlcvCandlesForPair(
          chain_name: BASE_MAINNET
          pair_addresses: ["0x9c087Eb773291e50CF6c6a90ef0F4500e349B903"],
          interval: StreamingInterval.ONE_MINUTE,
          timeframe: StreamingTimeframe.ONE_HOUR,
        ) {
          open
          high
          low
          close
          volume
          price_usd
          volume_usd
          chain_name
          pair_address
          interval
          timeframe
          timestamp
        }
      }`,
    {},
    {
      next: (data) => console.log("Received streaming data:", data),
      error: (err) => console.error("Subscription error:", err),
      complete: () => console.info("Subscription completed"),
    }
  );

  // Cleanup function - unsubscribe when component unmounts
  return () => {
    unsubscribe();
  };
}, []);
```

## GraphQL Queries
You can also use raw GraphQL queries for more streamlined and selective data scenarios:
```typescript GoldRush SDK
const unsubscribeNewPairs = client.StreamingService.rawQuery(
  `subscription {
       newPairs(
         chain_name: BASE_MAINNET,
         protocols: [UNISWAP_V2, UNISWAP_V3]
       ) {
         chain_name
         protocol
         pair_address
         tx_hash
         liquidity
         base_token_metadata {
           contract_name
           contract_ticker_symbol
         }
         quote_token_metadata {
           contract_name
           contract_ticker_symbol
         }
       }
     }`,
  {},
  {
    next: (data) => console.log("Raw new pairs data:", data),
    error: (error) => console.error("Error:", error),
  }
);

// Raw query for token OHLCV data
const unsubscribeTokenOHLCV = client.StreamingService.rawQuery(
  `subscription {
      ohlcvCandlesForToken(
        chain_name: BASE_MAINNET
        token_addresses: ["0x4B6104755AfB5Da4581B81C552DA3A25608c73B8"]
        interval: ONE_MINUTE
        timeframe: ONE_HOUR
      ) {
        open
        high
        low
        close
        volume
        volume_usd
        quote_rate
        quote_rate_usd
        timestamp
        base_token {
          contract_name
          contract_ticker_symbol
        }
      }
    }`,
  {},
  {
    next: (data) => console.log("Raw token OHLCV data:", data),
    error: (error) => console.error("Error:", error),
  }
);
```

---

# GraphQL Endpoints Reference

## List of endpoints

|Functionality|Endpoint Type||
|---|---|---|
|**OHLCV Tokens Stream**|`subscription`|```subscription { ohlcvCandlesForToken { ... }  }```|
|**OHLCV Pairs Stream**|`subscription`|```subscription { ohlcvCandlesForPair { ... }  }```|
|**New DEX Pairs Stream**|`subscription`|```subscription { newPairs { ... }  }```|
|**Update Pairs Stream**|`subscription`|```subscription { updatePairs { ... }  }```|
|**Wallet Activity Stream**|`subscription`|```subscription { walletTxs { ... }  }```|
|**Token Search Query**|`query`|```query { searchToken { ... }  }```|
|**Top Trader Wallets for Token Query**|`query`|```query { upnlForToken { ... }  }```|
|**Wallet PnL by Token Query**|`query`|```query { upnlForWallet { ... }  }```|

## Fetching the schema

```graphql
query IntrospectionQuery {
  __schema {
    queryType {
      name
    }
    mutationType {
      name
    }
    subscriptionType {
      name
    }
    types {
      ...FullType
    }
    directives {
      name
      description

      locations
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description

  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type {
    ...TypeRef
  }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## Streaming-Specific Troubleshooting

### WebSocket Connection Issues
- Verify URL: `wss://streaming.goldrushdata.com/graphql`
- Set protocol header: `Sec-WebSocket-Protocol: graphql-transport-ws`
- Auth errors only surface on subscription start, not on WebSocket connect

### Chain Name Format
- Streaming API uses `SCREAMING_SNAKE_CASE`: `ETH_MAINNET`, `BASE_MAINNET`
- Foundational API uses `kebab-case`: `eth-mainnet`, `base-mainnet`
- Using the wrong format will silently fail (no data received)

### Subscription Not Receiving Data
- Check chain supports Streaming (not all chains do)
- Verify chain name format (SCREAMING_SNAKE_CASE)
- Ensure API key is valid (connection_ack always succeeds regardless)