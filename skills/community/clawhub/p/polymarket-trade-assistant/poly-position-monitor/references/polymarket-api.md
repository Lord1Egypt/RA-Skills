# Polymarket API Reference (Position Monitor)

## Overview

Four API surfaces are used. Positions, activity, and trades are public (no auth). Orders require CLOB L2 authentication.

## 1. Data API — Positions & Activity

**Base URL:** `https://data-api.polymarket.com`

### GET /positions

Current positions for a wallet address.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | string | **Required.** Wallet address (0x-prefixed) |
| `market` | string | Condition ID filter (mutually exclusive with eventId) |
| `eventId` | string | Event ID filter |
| `sizeThreshold` | number | Minimum token size (default: 1) |
| `limit` | int | 0–500 (default: 100) |
| `offset` | int | Pagination offset |
| `sortBy` | string | CURRENT, INITIAL, TOKENS, CASHPNL, PERCENTPNL, TITLE, PRICE, AVGPRICE |
| `sortDirection` | string | ASC or DESC |

**Response fields:** conditionId, assetId, title, outcome, size, avgPrice, currentValue, initialValue, cashPnl, percentPnl, curPrice, eventSlug, endDate, redeemable, mergeable.

### GET /activity

Onchain activity feed for a user.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | string | **Required.** Wallet or proxy address |
| `type` | string | TRADE, REDEEM, MERGE, SPLIT, REWARD, CONVERSION |
| `market` | string | Condition ID filter |
| `eventId` | string | Event ID filter |
| `start` | number | Unix timestamp lower bound |
| `end` | number | Unix timestamp upper bound |
| `side` | string | BUY or SELL |
| `limit` | int | 0–500 (default: 100) |
| `offset` | int | Pagination offset |
| `sortBy` | string | TIMESTAMP, TOKENS, CASH |

### GET /trades

Historical fills across markets.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | string | Filter by participant address |
| `market` | string[] | Condition ID(s) |
| `side` | string | BUY or SELL |
| `limit` | int | 0–10000 (default: 100) |
| `offset` | int | Pagination offset |

### GET /holders

Top token holders for a market.

| Parameter | Type | Description |
|-----------|------|-------------|
| `market` | string | Condition ID |

## 2. CLOB API — Prices & Orders

**Base URL:** `https://clob.polymarket.com`

### GET /prices-history

Historical price data.

| Parameter | Type | Description |
|-----------|------|-------------|
| `market` | string | **Required.** Token ID (asset_id) |
| `interval` | string | max, all, 1m, 1w, 1d, 6h, 1h |
| `fidelity` | int | Data resolution in minutes (default: 1) |
| `startTs` | number | Unix timestamp lower bound |
| `endTs` | number | Unix timestamp upper bound |

**Response:** `{"history": [{"t": unix_ts, "p": price_float}, ...]}`

### GET /orders (Authenticated)

Open orders for the authenticated user.

| Parameter | Type | Description |
|-----------|------|-------------|
| `market` | string | Condition ID filter |
| `asset_id` | string | Token ID filter |
| `next_cursor` | string | Pagination cursor |

**Authentication:** L2 HMAC-SHA256 via py-clob-client. Requires apiKey, secret, passphrase derived from wallet private key.

### GET /book

Full order book for a token.

| Parameter | Type | Description |
|-----------|------|-------------|
| `token_id` | string | **Required.** CLOB token ID |

## 3. Gamma API — Market Discovery

**Base URL:** `https://gamma-api.polymarket.com`

### GET /public-profile

| Parameter | Type | Description |
|-----------|------|-------------|
| `address` | string | Wallet address |

Returns: display name, bio, X username, proxy wallet, profile image.

## Authentication

Only `GET /orders` requires authentication. All other endpoints are public.

To get API credentials:
```python
from py_clob_client.client import ClobClient
client = ClobClient("https://clob.polymarket.com", chain_id=137, key=PRIVATE_KEY)
creds = client.create_or_derive_api_creds()
# Returns: {"apiKey": "...", "secret": "...", "passphrase": "..."}
```

Credentials are deterministically derived and only need to be generated once.
