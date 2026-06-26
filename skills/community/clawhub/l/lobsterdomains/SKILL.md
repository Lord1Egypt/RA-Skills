---
name: lobsterdomains
description: Register domain names via crypto payments (USDC, USDT, ETH, BTC). Check availability, get pricing across 1000+ TLDs, and complete registration with on-chain stablecoin payments on Ethereum, Arbitrum, Base, or Optimism.
homepage: https://lobsterdomains.xyz
emoji: 🦞
metadata:
  clawbot:
    primaryEnv: LOBSTERDOMAINS_API_KEY
    requires:
      bins: []
      env:
        - LOBSTERDOMAINS_API_KEY
---

# LobsterDomains — AI-Powered Domain Registration with Crypto

Register domain names using cryptocurrency payments. Supports USDC/USDT stablecoins on multiple chains (Ethereum, Arbitrum, Base, Optimism), native ETH, and Bitcoin.

## Authentication

Get your API key at https://lobsterdomains.xyz/api-keys (requires Ethereum wallet sign-in).

All requests require a Bearer token:

```
Authorization: Bearer ld_your_api_key_here
```

Set the environment variable:

```bash
export LOBSTERDOMAINS_API_KEY="ld_your_api_key_here"
```

## Base URL

```
https://lobsterdomains.xyz
```

## Tools

### 1. Check Domain Availability

Check if a domain is available and get pricing.

```
GET /api/v1/domains/check?domain={domain}
```

**Parameters:**
- `domain` (required): The domain name to check (e.g., `example.com`)

**Response:**
```json
{
  "available": true,
  "domain": "example.com",
  "price": "13.50",
  "currency": "USDC"
}
```

### 2. Get Current Prices

Retrieve current ETH and BTC prices in USD for payment conversion.

```
GET /api/v1/prices
```

### 3. Get TLD Pricing

View pricing for all supported TLDs.

```
GET https://lobsterdomains.xyz/pricing
```

### 4. Register a Domain

Complete a domain registration after on-chain payment.

```
POST /api/v1/domains/register
```

**Request Body:**
```json
{
  "domain": "example.com",
  "years": 1,
  "currency": "USDC",
  "chain": "base",
  "txHash": "0x...",
  "contact": {
    "firstName": "Jane",
    "lastName": "Doe",
    "organization": "Example Inc",
    "email": "jane@example.com",
    "phone": "+1.5551234567",
    "address": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "postalCode": "94105",
    "country": "US"
  },
  "nameservers": ["ns1.example.com", "ns2.example.com"]
}
```

**Fields:**
- `domain` (required): Domain name to register
- `years` (required): Registration period, 1–10
- `currency` (required): `USDC`, `USDT`, `ETH`, or `BTC`
- `chain` (required for stablecoins/ETH): `ethereum`, `arbitrum`, `base`, or `optimism`
- `txHash` (required): On-chain transaction hash proving payment
- `contact` (required): Registrant contact information with 2-letter country code
- `nameservers` (optional): Custom nameservers; defaults to afraid.org

**Response:**
```json
{
  "orderId": "abc123",
  "domain": "example.com",
  "status": "registered",
  "opensrsUsername": "...",
  "opensrsPassword": "...",
  "managementUrl": "https://..."
}
```

> **Important:** The response includes `opensrsUsername` and `opensrsPassword` for post-purchase DNS and transfer management. **Always present these credentials directly to the user** and instruct them to store the credentials securely (e.g., in a password manager). Never persist these credentials in conversation history, logs, or any file. These are sensitive third-party credentials that grant full control over the registered domain.

### 5. Query Orders

Retrieve order history.

```
GET /api/v1/orders
GET /api/v1/orders?domain={domain}
```

Returns up to 50 latest orders. Results may include OpenSRS management credentials — always present these to the user directly and remind them to store credentials securely.

## Payment Details

**Recommended method:** USDC or USDT stablecoins (6 decimal places)

**Receiving address:**
```
0x8939E62298779F5fE1b2acda675B5e85CfD594ab
```

**Supported chains:**
- Ethereum mainnet
- Arbitrum
- Base
- Optimism

Native ETH and Bitcoin are also accepted but require price verification via `/api/v1/prices`.

## Example Workflow

1. **Check availability:** `GET /api/v1/domains/check?domain=coolstartup.com`
2. **Confirm pricing** with the user
3. **User sends stablecoin payment** on their preferred chain
4. **Capture the transaction hash** from the user
5. **Register:** `POST /api/v1/domains/register` with tx hash and contact details
6. **Deliver credentials securely** — present OpenSRS management details to the user and remind them to save in a password manager