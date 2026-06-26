# LLM Integration Guide

# GoldRush API - LLM Integration Guide (Condensed)

**Purpose:** Quick reference for LLMs and AI agents to correctly use the GoldRush API, focusing on error prevention and critical validation rules.

---

## Quick Reference

| Item | Value |
|------|-------|
| **Base URL** | `https://api.covalenthq.com/v1` |
| **Authentication** | Bearer token in `Authorization` header |
| **API Key** | Sign up at goldrush.dev/platform (starts with `cqt_` or `ckey_`) |
| **TypeScript SDK** | `@covalenthq/client-sdk` |
| **Response Format** | JSON |
| **Protocol** | HTTPS only (HTTP will fail) |

**Rate Limits:**
- Free 14 day trial: 25,000 API credits/month, 4 requests/second, no overages
- Vibe Coding tier: $10/month for 10,000 included API credits, 4 requests/second, overages at $0.001/credit
- Professional: $250/month for 300,000 included API credits, 50 requests/second, overages at $0.00077/credit
- x402 (Pay-Per-Request): No subscription required, 100 requests/minute per wallet, pay with stablecoins on Base

---

## Chain Names (CRITICAL)

Chain names use the format: `{network}-{environment}`. These are **case-sensitive** and must match exactly.

### Supported Chain Names Table

| Common Name | Chain Name (API Parameter) | Chain ID | Support Level |
|-------------|---------------------------|----------|---------------|
| Base | `base-mainnet` | 8453 | foundational |
| BNB Smart Chain (BSC) | `bsc-mainnet` | 56 | foundational |
| Ethereum | `eth-mainnet` | 1 | foundational |
| Gnosis | `gnosis-mainnet` | 100 | foundational |
| Optimism | `optimism-mainnet` | 10 | foundational |
| Polygon | `matic-mainnet` | 137 | foundational |
| ADI Chain | `adi-mainnet` | 36900 | frontier |
| ApeChain | `apechain-mainnet` | 33139 | frontier |
| Arbitrum | `arbitrum-mainnet` | 42161 | frontier |
| Arbitrum Nova | `arbitrum-nova-mainnet` | 42170 | frontier |
| Arc Testnet | `arc-testnet` | 5042002 | frontier |
| Avalanche C-Chain | `avalanche-mainnet` | 43114 | frontier |
| Axie/Ronin | `axie-mainnet` | 2020 | frontier |
| Berachain | `berachain-mainnet` | 80094 | frontier |
| Bitcoin | `btc-mainnet` | 20090103 | frontier |
| HyperCore | `hypercore-mainnet` | na | frontier |
| HyperEVM | `hyperevm-mainnet` | 999 | frontier |
| Ink | `ink-mainnet` | 57073 | frontier |
| Linea | `linea-mainnet` | 59144 | frontier |
| Mantle | `mantle-mainnet` | 5000 | frontier |
| MegaETH | `megaeth-mainnet` | 4326 | frontier |
| Monad | `monad-mainnet` | 143 | frontier |
| Oasis Sapphire | `oasis-sapphire-mainnet` | 23294 | frontier |
| Plasma | `plasma-mainnet` | 9745 | frontier |
| Scroll | `scroll-mainnet` | 534352 | frontier |
| Sei | `sei-mainnet` | 1329 | frontier |
| Solana | `solana-mainnet` | 1399811149 | frontier |
| Sonic | `sonic-mainnet` | 146 | frontier |
| Taiko | `taiko-mainnet` | 167000 | frontier |
| Unichain | `unichain-mainnet` | 130 | frontier |
| Viction | `viction-mainnet` | 88 | frontier |
| World Chain | `world-mainnet` | 480 | frontier |
| zkSync Era | `zksync-mainnet` | 324 | frontier |
| Blast | `blast-mainnet` | 81457 | community |
| Canto | `canto-mainnet` | 7700 | community |
| Celo | `celo-mainnet` | 42220 | community |
| Covalent | `covalent-internal-network-v1` | 1131378225 | community |
| Cronos zkEVM | `cronos-zkevm-mainnet` | 388 | community |
| Fantom | `fantom-mainnet` | 250 | community |
| Manta Pacific Testnet | `manta-sepolia-testnet` | 3441006 | community |
| Moonbeam | `moonbeam-mainnet` | 1284 | community |
| Moonriver | `moonbeam-moonriver` | 1285 | community |
| Oasis | `emerald-paratime-mainnet` | 42262 | community |
| opBNB | `bnb-opbnb-mainnet` | 204 | community |
| Redstone | `redstone-mainnet` | 690 | community |
| ZetaChain | `zetachain-mainnet` | 7000 | community |
| Cronos | `cronos-mainnet` | 25 | archived |
| Harmony | `harmony-mainnet` | 1666600000 | archived |

**Note:** Always use the "Chain Name (API Parameter)" value in API calls. Using common names will result in errors.


**Chain Support Levels:**

Chains are categorized into four support levels. See [Chain Documentation](#chain-documentation) for complete definitions.

- **Foundational** (6 chains) - Full feature parity including historical balances, token holders at any block, and DEX spot prices
- **Frontier** (28 chains) - Core features with expanding coverage; includes all non-EVM chains
- **Community** (14 chains) - Growing integration with all core onchain data
- **Archived** (5 chains) - Limited data availability, no live data

---

## Parameter Naming Convention

GoldRush uses different naming conventions depending on the context:

| Context | Convention | Example |
|---------|-----------|----------|
| TypeScript SDK | camelCase | `chainName`, `walletAddress` |
| REST API Path Parameters | camelCase | `{chainName}`, `{walletAddress}` |
| REST API Query Parameters | kebab-case | `quote-currency`, `block-height` |
| JSON Response Fields | snake_case | `chain_id`, `updated_at` |

### Parameter Mapping (SDK ↔ REST API)

| SDK Parameter | REST Query Parameter |
|--------------|---------------------|
| chainName | N/A (path parameter) |
| walletAddress | N/A (path parameter) |
| quoteCurrency | quote-currency |
| blockHeight | block-height |
| noLogs | no-logs |
| withInternal | with-internal |
| withState | with-state |
| withInputData | with-input-data |

---

## Input Validation Rules

### Ethereum Addresses

- **Format:** `0x` followed by 40 hexadecimal characters
- **Regex:** `^0x[a-fA-F0-9]{40}$`
- **Case:** Insensitive (both `0xabc...` and `0xABC...` are valid)
- **Special Values:** Also accepts ENS names (e.g., `vitalik.eth`), RNS, Lens Handles, Unstoppable Domains

**Examples:**
- ✅ Valid: `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`
- ✅ Valid: `vitalik.eth`
- ❌ Invalid: `d8dA6BF26964aF9D7eEd9e03E53415D37aA96045` (missing 0x)
- ❌ Invalid: `0xd8dA6BF` (too short)

### Chain Names

- **Format:** Exact match from supported chains table (case-sensitive)

**Examples:**
- ✅ Valid: `eth-mainnet`
- ❌ Invalid: `ethereum` (use `eth-mainnet`)
- ❌ Invalid: `Eth-Mainnet` (case-sensitive)
- ❌ Invalid: `eth_mainnet` (use hyphen, not underscore)

### Block Heights

- **Type:** Integer ≥ 0
- **Special Value:** `"latest"` for current block
- **Maximum:** Current chain height (varies by chain)

**Examples:**
- ✅ Valid: `12345678`
- ✅ Valid: `latest`
- ❌ Invalid: `-1`

### Quote Currency

- **Type:** String (case-insensitive)
- **Supported Values:** `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, `GBP`
- **Default:** `USD`

### Pagination

- **Page Numbers:** 0-indexed (first page is `0`)
- **Page Size:** 100 items per page (default, not configurable for most endpoints)
- **End Detection:**
  - If returned page has < 100 items, it's the last page
  - Check `has_more` field in response (where available)
  - Use `links.next` for next page URL (where available)

---

## Understanding Balance Fields

```json
{
  "contract_decimals": 18,
  "balance": "1500000000000000000",
  "quote_rate": 2500.50,
  "quote": 3750.75,
  "pretty_quote": "$3,750.75"
}
```

**Field Explanations:**
- `balance`: Raw token amount as string (to handle large numbers/BigInt). This is **NOT** the human-readable value.
- `contract_decimals`: Number of decimal places for this token
- `quote_rate`: Current price of 1 token in quote currency (e.g., USD)
- `quote`: Total value of this token holding in quote currency
- `pretty_quote`: Formatted currency string for display

**To get human-readable balance:**

```javascript
const humanReadable = parseFloat(balance) / Math.pow(10, contract_decimals);
// Example: "1500000000000000000" / 10^18 = 1.5 tokens
```

---

## Understanding Transaction Fields

```json
{
  "successful": true,
  "value": "0",
  "gas_spent": 21000,
  "gas_price": 50000000000,
  "fees_paid": "1050000000000000",
  "gas_quote": 2.75,
  "gas_quote_rate": 2500.00
}
```

**Field Explanations:**
- `successful`: Boolean indicating if transaction succeeded
- `value`: Amount of native token transferred (as string, in wei for EVM chains)
- `gas_spent`: Actual gas units consumed
- `gas_price`: Gas price in wei (for EVM chains)
- `fees_paid`: Total fee in wei (`gas_spent × gas_price`)
- `gas_quote`: Total fee in quote currency (e.g., USD)
- `gas_quote_rate`: Native token price used for conversion

---

## Error Responses

All error responses follow this schema:

```json
{
  "data": null,
  "error": true,
  "error_message": "Human-readable error description",
  "error_code": 401
}
```

### Common Error Codes

| HTTP Status | error_code | Meaning | Solution |
|------------|-----------|---------|----------|
| 401 | 401 | Invalid or missing API key | Check Authorization header format: `Bearer YOUR_API_KEY` |
| 400 | 400 | Invalid request parameters | Verify chain name, address format, or other parameters |
| 404 | 404 | Resource not found | Check if chain name is valid or address has activity |
| 429 | 429 | Rate limit exceeded | Reduce request frequency or upgrade plan |
| 500 | 500 | Internal server error | Retry request, contact support if persists |

---

## Best Practices for LLMs

### 1. Always Validate Chain Names

```typescript
const VALID_CHAINS = [
  "eth-mainnet", "matic-mainnet", "base-mainnet",
  "arbitrum-mainnet", "optimism-mainnet", "bsc-mainnet"
];

function isValidChain(chainName: string): boolean {
  return VALID_CHAINS.includes(chainName);
}
```

### 2. Handle BigInt Balance Values Correctly

```typescript
// ❌ WRONG
const balance = parseInt(item.balance); // Will overflow for large values

// ✅ CORRECT
const balance = parseFloat(item.balance) / Math.pow(10, item.contract_decimals);
```

### 3. Implement Pagination Properly

```typescript
// ✅ CORRECT
let page = 0;
let allItems = [];
let hasMore = true;

while (hasMore) {
  const resp = await fetchPage(page);
  allItems.push(...resp.items);
  hasMore = resp.items.length === 100; // Full page = more data likely exists
  page++;
}
```

### 4. Use Appropriate Error Handling

```typescript
const resp = await client.BalanceService.getTokenBalancesForWalletAddress(
  chainName,
  address
);

if (resp.error) {
  // Handle error - don't try to access resp.data
  console.error(resp.error_message);
  return;
}

// Safe to access resp.data here
const balances = resp.data.items;
```

---

## Common Mistakes to Avoid

### ❌ Using Wrong Chain Name Format

```typescript
// WRONG
const chain = "ethereum";
const chain = "polygon";

// CORRECT
const chain = "eth-mainnet";
const chain = "matic-mainnet";
```

### ❌ Treating Balance as Number

```typescript
// WRONG
const balance = parseInt(item.balance); // Overflow!

// CORRECT
const balance = parseFloat(item.balance) / Math.pow(10, item.contract_decimals);
```

### ❌ Forgetting to Check Error Response

```typescript
// WRONG
const resp = await client.getSomething();
const data = resp.data.items; // May crash if error

// CORRECT
const resp = await client.getSomething();
if (!resp.error) {
  const data = resp.data.items;
}
```

### ❌ Not Handling Pagination

```typescript
// WRONG - only gets first 100 transactions
const resp = await client.getTransactions(chain, address, { page: 0 });

// CORRECT - gets all transactions
let page = 0;
let allTxs = [];
while (true) {
  const resp = await client.getTransactions(chain, address, { page });
  if (resp.error || resp.data.items.length === 0) break;
  allTxs.push(...resp.data.items);
  if (resp.data.items.length < 100) break;
  page++;
}
```

### ❌ Missing Bearer Prefix in Authorization

```bash
# WRONG
curl -H "Authorization: YOUR_API_KEY"

# CORRECT
curl -H "Authorization: Bearer YOUR_API_KEY"
```

### ❌ Using HTTP Instead of HTTPS

```bash
# WRONG
http://api.covalenthq.com/v1/...

# CORRECT
https://api.covalenthq.com/v1/...
```

---

## Frequently Asked Questions (LLM-Specific)

### Q: How do I convert balance to human-readable format?

**A:** Divide the balance string by 10^contract_decimals:

```typescript
const humanReadable = parseFloat(balance) / Math.pow(10, contract_decimals);
// Example:
// balance = "1500000000000000000"
// contract_decimals = 18
// humanReadable = 1.5 tokens
```

### Q: What's the difference between `quote` and `quote_rate`?

**A:**
- `quote_rate`: Price of 1 token in quote currency (e.g., $2,500.50 per ETH)
- `quote`: Total value of the balance in quote currency (balance × quote_rate)

### Q: How do I know which chains support internal transactions?

**A:** Only Foundational chains support tracing features (`with-internal`, `with-state`, `with-input-data`). Currently, only `eth-mainnet` fully supports all tracing features. Check the endpoint documentation for "Foundational Chains" support.

### Q: How do I handle ENS names?

**A:** Just pass the ENS name directly as the wallet address. GoldRush automatically resolves it:

```typescript
const resp = await client.BalanceService.getTokenBalancesForWalletAddress(
  "eth-mainnet",
  "vitalik.eth" // Automatically resolved
);
```

### Q: What's the difference between `balances_v2` and `balances_native`?

**A:**
- `balances_v2`: Returns ALL tokens (native + ERC20 + NFTs)
- `balances_native`: Returns ONLY the native token (ETH, MATIC, etc.)

Use `balances_native` for lightweight queries when you only need the native token balance.

### Q: How do I filter out spam tokens?

**A:** Use the `no-spam` query parameter:

```bash
curl "https://api.covalenthq.com/v1/eth-mainnet/address/0x.../balances_v2/?no-spam=true"
```

### Q: When should I use the SDK vs direct REST calls?

**A:**
- **Use SDK:** TypeScript/JavaScript projects, automatic pagination, type safety
- **Use REST:** Python, Go, or any other language; curl testing; maximum flexibility

### Q: How often does data update?

**A:**
- Real-time endpoints: 30 seconds or 2 blocks (whichever is faster)
- Historical data: Indexed from genesis block
- NFT metadata: Cached, use `with-uncached=true` to force refresh

---

## Quick Reference: Endpoint URL Patterns

| Data Type | URL Pattern |
|-----------|------------|
| Token Balances | `/v1/{chain}/address/{address}/balances_v2/` |
| Native Balance Only | `/v1/{chain}/address/{address}/balances_native/` |
| Transaction History | `/v1/{chain}/address/{address}/transactions_v3/page/{page}/` |
| Single Transaction | `/v1/{chain}/transaction_v2/{txHash}/` |
| NFT Metadata | `/v1/{chain}/tokens/{contract}/nft_metadata/{tokenId}/` |
| Token Holders | `/v1/{chain}/tokens/{contract}/token_holders_v2/` |
| Cross-Chain Activity | `/v1/address/{address}/activity/` |
| Security Approvals | `/v1/{chain}/approvals/{address}/` |
| ERC20 Transfers | `/v1/{chain}/address/{address}/transfers_v2/` |
| Historical Prices | `/v1/pricing/historical_by_address/{chain}/{contract}/` |

---

## Additional Resources

- **Full API Documentation:** https://goldrush.dev/docs/
- **API Reference:** https://goldrush.dev/docs/api-reference/
- **Guides & Tutorials:** https://goldrush.dev/guides/
- **Supported Chains:** https://goldrush.dev/docs/chains/overview
- **Status Page:** https://status.goldrush.dev/
- **Get API Key:** https://goldrush.dev/platform
- **Discord Community:** https://discord.gg/8ZWgu2pWY4
- **GitHub:** https://github.com/covalenthq

---

## System Prompt Suggestion for AI Agents

When building AI agents that use GoldRush API, include this in your system prompt:

```
You have access to the GoldRush API for blockchain data. Key points:

1. Chain names use format like "eth-mainnet", "matic-mainnet", "base-mainnet" - never use common names like "ethereum" or "polygon"
2. Balance fields are strings representing large numbers. Divide by 10^contract_decimals to get human-readable values
3. All requests require "Authorization: Bearer YOUR_API_KEY" header
4. Pagination returns 100 items per page. If result has 100 items, more pages likely exist
5. Base URL: https://api.covalenthq.com/v1
6. Always check resp.error before accessing resp.data
7. Ethereum addresses: 0x + 40 hex chars, or ENS names
8. For detailed integration guidance, refer to the LLM Integration Guide
```

---

**Last Updated:** January 2025
**API Version:** v1
**Documentation Version:** 2.0 (LLM-Optimized Condensed)


---

# Error Handling & Troubleshooting

Both the GoldRush Foundational API (REST) and the Streaming API (GraphQL/WebSocket) return structured errors when something goes wrong. This page is the single reference for understanding error codes, handling rate limits, implementing retries, and debugging common issues.

## Foundational API (REST) Errors

The Foundational API returns standard HTTP status codes along with a JSON error body.

| Code | Name | Common Cause |
| :--- | :--- | :--- |
| `400` | Bad Request | Malformed parameters, invalid address format |
| `401` | Unauthorized | Missing or incorrect API key |
| `402` | Payment Required | Credits exhausted — enable Flex Credits or upgrade tier |
| `403` | Forbidden | API key is valid but not authorized for the resource |
| `404` | Not Found | Unsupported chain, invalid endpoint |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Server-side failure |
| `503` | Service Unavailable | Maintenance or outage |

**Example error responses:**

```json 401 Unauthorized
{
  "error": true,
  "error_message": "No valid API key was provided.",
  "error_code": "401"
}
```

```json 429 Rate Limited
{
  "error": true,
  "error_message": "You are being rate-limited. Please reduce request frequency.",
  "error_code": "429"
}
```

## Streaming API (GraphQL/WebSocket) Errors

Authentication errors in the Streaming API are returned as GraphQL errors with specific extension codes:

| Code | Description |
| :--- | :--- |
| `MISSING_TOKEN` | No API key was provided in the `connection_init` payload. |
| `INVALID_TOKEN` | The provided API key is malformed or invalid. |
| `AUTH_SYSTEM_ERROR` | An internal server error occurred during authentication. |

**Example error response:**

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

  Auth errors only surface when a subscription starts, **not** on WebSocket connect. The server always sends a `connection_ack` response regardless of whether the API key is valid. You will only discover an invalid key when you attempt to subscribe.

## Rate Limits

The Foundational API enforces rate limits based on your plan tier:

| Plan | Rate Limit | API Credits |
| :--- | :--- | :--- |
| 14-day Free Trial | 4 RPS | 25,000 |
| Vibe Coding ($10/mo) | 4 RPS | 10,000 |
| Professional ($250/mo) | 50 RPS | 300,000 |
| Inner Circle | Custom (up to 100+ RPS) | Custom SLA |

Rate limits are enforced **per API key and IP address**. When you exceed your limit, you'll receive a `429 Too Many Requests` response. Back off and retry using the strategies below.

## Retry Strategies

### Exponential Backoff with Jitter

For transient errors (`429`, `500`, `503`), implement exponential backoff with random jitter to avoid thundering herd problems.

```typescript TypeScript
async function fetchWithRetry(
  url: string,
  options: RequestInit,
  maxRetries = 5
): Promise {
  for (let attempt = 0; attempt  setTimeout(r, baseDelay + jitter));
      continue;
    }

    throw new Error(`Request failed: ${response.status}`);
  }

  throw new Error("Max retries exceeded");
}
```

```python Python
import time
import random
import requests

def fetch_with_retry(url, headers, max_retries=5):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)

        if response.ok:
            return response

        if response.status_code in (429, 500, 503):
            base_delay = (2 ** attempt)
            jitter = random.uniform(0, 1)
            time.sleep(base_delay + jitter)
            continue

        response.raise_for_status()

    raise Exception("Max retries exceeded")
```

### SDK Built-in Retries

The [GoldRush TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk) handles retries and rate limiting automatically — no manual retry logic needed when using the SDK.

### Streaming Reconnection

The GoldRush Client SDK manages WebSocket reconnection automatically. If you're using a custom [`graphql-ws`](https://github.com/enisdenjo/graphql-ws) client, configure the `shouldRetry` option:

```typescript
import { createClient } from "graphql-ws";

const client = createClient({
  url: "wss://gr-staging-v2.streaming.covalenthq.com/graphql",
  connectionParams: {
    GOLDRUSH_API_KEY: "YOUR_API_KEY_HERE",
  },
  shouldRetry: () => true,
  retryAttempts: 5,
});
```

## Debugging Tips

  
### Verify your API key format

GoldRush API keys follow the pattern `cqt_wF...` or `cqt_rQ...` (26 base58 characters after the prefix). Double-check for trailing whitespace or truncation.

  
### Check supported chains

A `404` error often means the chain is unsupported. See **Supported Chains** for the full list.

  
### Inspect the full error body

Don't rely on the HTTP status code alone. The JSON response body contains an `error_message` field with specific details about what went wrong.

  
### Test with curl or websocat

Isolate issues from your application code by testing directly:

    ```bash
    # Foundational API
    curl -X GET https://api.covalenthq.com/v1/eth-mainnet/address/demo.eth/balances_v2/ \
         -u YOUR_API_KEY_HERE: \
         -H 'Content-Type: application/json'
    ```

    For the Streaming API, use [websocat](https://github.com/vi/websocat) — see the **Streaming API Authentication** guide for setup steps.

  
### Monitor credit usage

Track your API credit consumption on the [GoldRush Platform dashboard](https://goldrush.dev/platform) to avoid unexpected `402` errors.

  
### Contact support for persistent 500/503 errors

If you're consistently hitting `500` or `503` errors, reach out to **support@covalenthq.com** with your API key prefix, the endpoint, and timestamps of the failures.

## Quick Reference

  
### Foundational API Auth

API key setup, authentication methods, and SDK usage.

### Streaming API Auth

WebSocket authentication and connection management.

### FAQ

Common questions about plans, rate limits, and features.

### Supported Chains

Full list of supported blockchains and endpoints.

---

# Frequently Asked Questions

## General Questions

### What is the GoldRush API?

GoldRush offers the most comprehensive Blockchain Data API suite for developers, analysts, and enterprises.

### What can I do with the GoldRush API?

The GoldRush API provides fast, accurate, and developer-friendly access to the essential onchain data for building DeFi dashboards, wallets, trading bots, AI Agents, tax and compliance platforms. 

### Do I need API keys to use GoldRush?
Yes, you need an API key to access the GoldRush API. Your API Key is available on the **GoldRush platform** when you sign up for an account.

### If a client asks how to verify that GoldRush API is real-time or low-latency, how can we demonstrate or prove that?

You can demonstrate real-time or low-latency capabilities through:
* Timestamp validation: Pull `/v1/{chain_id}/block_v2/latest/` and compare the block timestamp with the current time (should be sub-second to a few seconds behind depending on chain).
* Latency benchmarks: Use tools like curl or Postman to measure API response time. GoldRush's streaming endpoints often respond in under 400ms for supported chains.
* Streaming demos: If using the Streaming API, show live updates of token transfers or block finality in dev dashboards.

### Besides the common 401, 402, and 429 error codes, are there any other error responses we should be aware of?

Yes. Additional error codes include:

* `400 Bad Request` – Invalid parameters or malformed request.
* `402 Payment Required` – Alloted credits exceeded and need to enable Flex Credits or upgrade subscription tier.
* `403 Forbidden` – API key is valid but not authorized for the resource.
* `404 Not Found` – Endpoint or data not available (e.g. unsupported chain).
* `500 Internal Server Error` – Unexpected failure on GoldRush's side.
* `503 Service Unavailable` – Maintenance or backend issue.

Each error includes a descriptive JSON body for debugging. For a complete guide to error codes, retry strategies, and debugging tips, see **Error Handling & Troubleshooting**.

## Foundational API Questions

### What is the rate limit for API calls?

The GoldRush Foundational API enforces rate limits based on the user's plan:
* 14-day Free Trial: 4 requests per second (RPS), 25,000 API credits.
* Vibe Coding Plan ($10/mo): 4 RPS, 10,000 API credits.
* Professional Plan ($250/mo): 50 RPS, 300,000 API credits.
* Inner Circle: Custom limits, typically up to 100 RPS or higher, based on SLAs.

Rate limits are enforced per API key and IP, and requests exceeding limits receive a `429 Too Many Requests` error. For a complete guide to error codes, retry strategies, and debugging tips, see **Error Handling & Troubleshooting**.

### Which plan is right for me?

**Vibe Coding Plan ($10/mo)** is built for:
* Solo founders and indie hackers shipping fast
* Hackathon teams and weekend projects
* AI-native builders using Cursor, Windsurf, or Claude
* Prototyping and validating ideas before scaling

**Professional Plan ($250/mo)** is built for:
* Teams building production applications
* Apps that need higher rate limits (50 RPS)
* Projects requiring priority support
* Companies with compliance or reliability requirements

You can start with Vibe Coding and upgrade to Professional as your project scales.

### Can I upgrade from Vibe Coding to Professional?

Yes. You can upgrade at any time from the [GoldRush platform](https://goldrush.dev/platform). Your API key stays the same, so no code changes are needed.

## Streaming API Questions

### How does the Streaming API work?
The Streaming API uses WebSocket connections to provide real-time updates about blockchain events. It maintains a persistent connection and pushes structured data to subscribed clients as events occur.

### What are Redstone Bolt price feeds?

Redstone Bolt provides ultra-low-latency CEX price data for 9 major tokens on MegaETH, including BTC, ETH, SOL, BNB, XRP, ADA, DOGE, USDT, and USDC. Prices are updated every **2.4 ms** (~400 updates/sec), sourced from Binance, Coinbase, OKX, Bitget, and Kraken via Bolt nodes co-located with MegaETH sequencer infrastructure. Bolt-powered feeds use the `REDSTONE-` prefix (e.g. `REDSTONE-BTC`, `REDSTONE-ETH`). You can consume these prices through the **OHLCV Tokens Stream** on the `MEGAETH_MAINNET` chain — see that page for the full list of supported feeds.

### What types of events can I subscribe to?

See all available streams on the **Streaming API Overview**.