# GoldRush Foundational API Overview

## Quick Reference

| Item | Value |
|------|-------|
| **Base URL** | `https://api.covalenthq.com/v1` |
| **Protocol** | HTTPS (REST) |
| **Authentication** | Bearer token in `Authorization` header |
| **API Key** | Sign up at goldrush.dev/platform (starts with `cqt_` or `ckey_`) |
| **SDK** | `@covalenthq/client-sdk` (TypeScript) |
| **Response Format** | JSON |
| **Rate Limits** | 4 RPS (Vibe Coding) / 50 RPS (Professional) |

---

## Use Cases

  
### Wallet API

Multichain token balances (ERC20, 721, 1155, native), token transfers and prices (spot and historical) for a wallet.

### Activity Feed API

Multichain historical transactions with human-readable event logs and historical prices. Includes transaction count and gas usage/spend summaries.

### NFT API

Media assets, metadata, sales, owners, trait and attribute filters, thumbnail previews.

### Bitcoin API

Bitcoin balances and transactions for x/y/zpub and non-HD addresses, including historical and spot prices.

### Security API

NFT and ERC20 token allowances, including value-at-risk.

### Block Explorer API

Block details, event logs by contract address or topic hash, gas prices, token prices & holders.

---

## Introduction

This quickstart guide walks through using the **GoldRush TypeScript SDK** to quickly build with multichain data leveraging the powerful GoldRush APIs. 

## Prerequisites

Using any of the GoldRush developer tools requires an API key.

### Vibe Coders

$10/mo — Built for solo builders and AI-native workflows.

### Teams

$250/mo — Production-grade with 50 RPS and priority support.

## Supported Chains

GoldRush can be used with any of the supported chains. See the full list, including chain categorization, at [Supported Chains](https://goldrush.dev/chains/).

Some data enrichments such as internal transactions and historical balance fetches are only available for Foundational Chains.

## Using the GoldRush TypeScript SDK

The GoldRush TypeScript SDK is the fastest way to integrate the GoldRush APIs for working with blockchain data. The SDK works with all supported chains including Mainnets and Testnets.

This SDK requires NodeJS v18 or above.

### Step 1. Install the SDK

```bash npm
npm install @covalenthq/client-sdk
```

```bash yarn
yarn add @covalenthq/client-sdk
```

See the package on [npmjs](https://www.npmjs.com/package/@covalenthq/client-sdk) for more details.

### Step 2. Import the Client

The `GoldRushClient` class provides typesafe, easy-to-use helper functions and classes to use the GoldRush APIs.

```typescript
import { GoldRushClient } from "@covalenthq/client-sdk";
```

### Step 3. Initialize the Client

```typescript
import { GoldRushClient } from "@covalenthq/client-sdk";

const ApiServices = async () => {
    const client = new GoldRushClient("YOUR_API_KEY"); 
};
```

### Step 4. Invoke the Service

In this quickstart, we use the `BalanceService` and `getTokenBalancesForWalletAddress()` function to fetch all token balances held by an address. This function takes a chain name and wallet address as required arguments. 

ENS resolution is supported for `eth-mainnet`.

```typescript
import { GoldRushClient } from "@covalenthq/client-sdk";

const ApiServices = async () => {
    // Replace with your GoldRush API key
    const client = new GoldRushClient("YOUR_API_KEY"); 
    const response = await client.BalanceService.getTokenBalancesForWalletAddress("eth-mainnet", "demo.eth"); 
    
    if (!response.error) {
        console.log(response.data);
    } else {
        console.log(response.error_message);
    }
};

ApiServices();
```

Example response:

```json
{
    "address": "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de",
    "chain_id": 1,
    "chain_name": "eth-mainnet",
    "quote_currency": "USD",
    "updated_at": "2024-11-05T22:18:41.522Z",
    "items": [
        {
            "contract_decimals": 6,
            "contract_name": "Tether USD",
            "contract_ticker_symbol": "USDT",
            "contract_address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "contract_display_name": "Tether USD",
            "supports_erc": [],
            "logo_url": "https://logos.covalenthq.com/tokens/1/0xdac17f958d2ee523a2206206994597c13d831ec7.png",
            "last_transferred_at": "2024-08-28T12:43:35.000Z",
            "native_token": false,
            "type": "stablecoin",
            "is_spam": false,
            "balance": "3007173042",
            "balance_24h": "3007173042",
            "quote_rate": 1,
            "quote_rate_24h": 0.9992,
            "quote": 3007.173,
            "quote_24h": 3004.7673,
            "pretty_quote": "$3,007.17",
            "pretty_quote_24h": "$3,004.77",
            "logo_urls": {},
            "protocol_metadata": null,
            "nft_data": null
        }
    ]
}
```

---

This document provides a comprehensive overview of the authentication process for the Foundational API. All APIs are protected and require a valid GoldRush API key to access. This guide covers how to obtain and use an API key, with examples for both our SDKs and direct REST API calls.

## Why is Authentication Required?

Authentication is essential to ensure that only authorized users can access the Foundational API. It allows us to manage access, track usage for billing, and ensure the security and stability of our services.

## 1. Obtaining a GoldRush API Key

To begin, register for an API key at the [GoldRush Platform](https://goldrush.dev/platform/auth/register/). This key will be required for all requests to the Foundational API.

### Vibe Coders

$10/mo — Built for solo builders and AI-native workflows.

### Teams

$250/mo — Production-grade with 50 RPS and priority support.

## 2. Supplying the API Key

The Foundational API offers flexible and powerful ways to access blockchain data. You can use one of our GoldRush SDKs for a streamlined experience, or make direct HTTP requests to the various REST APIs.

### Using SDKs (Recommended)

For easier integration and to take advantage of built-in features like automatic retries and rate limit handling, we recommend using the TypeScript Client SDK.

Initialize the client with your API key:
```typescript
import { GoldRushClient } from "@covalenthq/client-sdk";

const ApiServices = async () => {
    const client = new GoldRushClient("YOUR_API_KEY_HERE"); // Replace with your GoldRush API key
    const resp = await client.BalanceService.getTokenBalancesForWalletAddress({
        chainName: "eth-mainnet",
        walletAddress: "vitalik.eth"
    });
    
    if (!resp.error) {
        console.log(resp.data);
    } else {
        console.log(resp.error_message);
    }
};

ApiServices();
```

### Direct API Calls

You can also authenticate by including your API key in direct HTTP requests.

### Basic Authentication

Provide your API key as the Basic Auth username. You do not need to provide a password. The trailing colon (`:`) prevents `curl` from prompting for a password.

```bash
curl -X GET https://api.covalenthq.com/v1/eth-mainnet/address/demo.eth/balances_v2/ \
     -u YOUR_API_KEY_HERE: \
     -H 'Content-Type: application/json'
```

### Bearer Token

Provide your API key in an `Authorization` header with the `Bearer` scheme.

```bash
curl -X GET https://api.covalenthq.com/v1/eth-mainnet/address/demo.eth/balances_v2/ \
     -H 'Authorization: Bearer YOUR_API_KEY_HERE'
```

### Query Parameter

Include your API key as the `key` query parameter in the request URL.

```bash
curl -X GET "https://api.covalenthq.com/v1/eth-mainnet/address/demo.eth/balances_v2/?key=YOUR_API_KEY_HERE"
```

## Error Handling

If an authentication-related error occurs, the API will return a `4XX` HTTP status code and a JSON body with details.

| Code | Description |
| :--- | :--- |
| `401 - Unauthorized` | No valid API key was provided, or the key is incorrect. |
| `402 - Payment Required` | The account has consumed its allocated API credits. |
| `429 - Too Many Requests`| You are being rate-limited. |

For a complete guide to error codes, retry strategies, and debugging tips, see **Error Handling & Troubleshooting**.

## Frequently Asked Questions (FAQ)

- **Which authentication method should I use?**
  - We strongly recommend using our [SDKs](#using-sdks-recommended) for the best developer experience. If you must make direct API calls, **Basic Authentication** is preferred over other methods for its security. Placing API keys in URLs (query parameter) is generally discouraged.

- **Where can I find my API Key?**
  - You can find your API key on the [GoldRush Platform](https://goldrush.dev/platform/) after signing up or logging in.

- **Are the API keys the same for the different GoldRush products?**
  - Yes, the same API key is used to authenticate with all GoldRush products.