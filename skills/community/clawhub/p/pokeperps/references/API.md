# PokePerps API Reference

Complete request/response schemas for all API endpoints.

Base URL: `https://backend.pokeperps.fun`

All endpoints return JSON. No authentication needed for read-only endpoints.

---

## Card Discovery & Research

### Search Cards

```
GET /api/cards/search?q={query}&limit={1-50}
```

Min query length: 2 chars.

**Response:**
```json
{
  "query": "charizard",
  "results": [
    {
      "product_id": 123456,
      "product_name": "Charizard ex - 223/197",
      "current_price": 45.67,
      "change_24h": 2.5,
      "change_30d": -5.3,
      "activity_score": 85.2,
      "min_price": 30.00,
      "max_price": 60.00,
      "mean_price": 42.50,
      "group": "Obsidian Flames",
      "sub_type": "Pokemon"
    }
  ],
  "count": 1
}
```

### Get Dashboard (Top Cards)

```
GET /api/dashboard?limit={1-200}
```

**Response:**
```json
{
  "overview": {
    "metadata": {
      "total_cards_analyzed": 5000,
      "avg_activity_score": 45.2,
      "high_activity_count": 120
    },
    "top_tradable": [
      {
        "product_id": 123456,
        "product_name": "Charizard ex",
        "current_price": 45.67,
        "change_24h": 2.5,
        "activity_score": 95.0
      }
    ]
  },
  "tradable_ids": [123456, 234567, 345678],
  "biggest_mover": {
    "product_id": 789012,
    "product_name": "Pikachu VMAX",
    "change_24h": 15.3
  }
}
```

### Browse Cards (Paginated)

```
GET /api/dashboard/bundles?limit={1-200}&offset={0+}
```

Returns card bundles with product details, month price history, and analysis.

### Explore Cards (with Trending)

```
GET /api/dashboard/explore?limit={1-200}&offset={0+}
```

Same as bundles but includes `is_trending` flag.

### Get Card Details

```
GET /api/cards/{product_id}
```

**Response:**
```json
{
  "product": {
    "product_id": 123456,
    "product_name": "Charizard ex - 223/197",
    "market_price": 45.67,
    "lowest_price": 40.00,
    "lowest_price_with_shipping": 43.50,
    "median_price": 44.00,
    "listings": 85,
    "sellers": 60,
    "set_name": "Obsidian Flames",
    "rarity_name": "Special Art Rare",
    "image_url": "https://tcgplayer-cdn.tcgplayer.com/product/...",
    "url": "https://www.tcgplayer.com/product/..."
  },
  "listings": [
    {
      "listing_id": "abc123",
      "seller_name": "CardShop",
      "condition": "Near Mint",
      "price": 42.00,
      "quantity": 3,
      "shipping_price": 0.99,
      "gold_seller": true
    }
  ],
  "recent_sales": [
    {
      "sale_id": "xyz789",
      "condition": "Near Mint",
      "price": 44.50,
      "quantity": 1,
      "order_date": "2025-01-15T10:30:00Z"
    }
  ],
  "price_history": {
    "product_id": 123456,
    "range_type": "month",
    "dates": ["2025-01-01", "2025-01-02"],
    "prices": [42.0, 43.5]
  },
  "analysis": {
    "product_id": 123456,
    "activity_score": 85.2,
    "change_24h": 2.5,
    "change_30d": -5.3,
    "current_price": 45.67,
    "min_price": 30.00,
    "max_price": 60.00,
    "mean_price": 42.50
  }
}
```

### Get Card Bundle (All Data)

```
GET /api/cards/{product_id}/bundle?include_listings=true&include_sales=true&include_history=true
```

Returns everything in one call: product, listings, sales, month + annual price history, analysis.

### Get Price History

```
GET /api/cards/{product_id}/history?range=month
GET /api/cards/{product_id}/history?range=annual
```

### Get Quick Card Info (Lightweight)

```
GET /api/cards/{product_id}/quick
```

Fast endpoint, returns basic product + analysis if cached.

### Batch Card Fetch

```
POST /api/cards/batch
Content-Type: application/json

{
  "productIds": [123456, 234567, 345678],
  "include": ["analysis", "listings", "sales", "history"]
}
```

Fetch up to 50 cards in a single request.

**Response:**
```json
{
  "cards": [
    {
      "productId": 123456,
      "found": true,
      "product": { "product_name": "...", "market_price": 45.67 },
      "analysis": { "activity_score": 85, "change_24h": 2.5 },
      "listings": [],
      "recentSales": [],
      "priceHistory": { "dates": [], "prices": [] }
    }
  ],
  "count": 3,
  "notFound": []
}
```

### Trading Signals

```
GET /api/cards/{product_id}/signals
```

**Response:**
```json
{
  "productId": 123456,
  "productName": "Charizard ex - 223/197",
  "currentPrice": 45.67,
  "signals": {
    "momentum": { "score": 0.75, "direction": "increasing" },
    "meanReversion": { "zScore": 1.2, "signal": "overbought" },
    "supply": { "listingCount": 45, "signal": "neutral" },
    "activity": { "score": 85, "signal": "high" },
    "priceChange": { "change24h": 2.5, "change30d": -5.3 }
  },
  "recommendation": {
    "action": "long",
    "confidence": 0.72,
    "suggestedLeverage": 5,
    "riskLevel": "medium",
    "bullishFactors": ["Positive momentum", "High trading activity"],
    "bearishFactors": ["Overbought (mean reversion risk)"]
  },
  "priceRange": {
    "min": 30.0,
    "max": 60.0,
    "mean": 42.5,
    "current": 45.67
  }
}
```

**Signal meanings:**

| Signal | Description |
|---|---|
| `momentum.direction` | `increasing`, `decreasing`, or `neutral` based on 7-day trend |
| `meanReversion.signal` | `oversold` (z < -1.5), `overbought` (z > 1.5), or `neutral` |
| `supply.signal` | `bullish` (<20 listings), `bearish` (>80 listings), `neutral` |
| `activity.signal` | `high` (>70), `medium` (40-70), `low` (<40) |

---

## Price & Oracle Data

### Get All Oracle Prices

```
GET /api/oracle/prices
```

**Response:**
```json
{
  "timestamp": 1705312345,
  "network": "mainnet-beta",
  "total": 25,
  "prices": [
    {
      "product_id": 123456,
      "price_usd": 45.67,
      "price_scaled": 4567000000,
      "age_seconds": 3
    }
  ]
}
```

### Get Router Prices (Best Available)

```
GET /api/oracle/router/prices
```

Returns the best available price for each product (on-chain or backend cached), with source info.

### Get Single Oracle Price

```
GET /api/trading/oracle/{product_id}
```

**Response:**
```json
{
  "productId": 123456,
  "price": 45.67,
  "updatedAt": 1705312345,
  "ageSeconds": 3,
  "source": "onchain",
  "onChain": { "price": 45.67, "updatedAt": 1705312345 },
  "backend": { "price": 45.65, "updatedAt": 1705312340 }
}
```

### Get Batch Oracle Prices

```
POST /api/trading/oracle/prices
Content-Type: application/json

{ "productIds": [123456, 234567, 345678] }
```

### Get Oracle Status

```
GET /api/oracle/status
```

---

## Trading & Positions

### Get Trading Config

```
GET /api/trading/config
```

**Response:**
```json
{
  "programId": "8hH5CWo14R5QhaFUuXpxJytchS6NgrhRLHASyVeriEvN",
  "usdcMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "network": "mainnet-beta",
  "maxLeverage": 50,
  "minPositionSize": 1,
  "tradingFeeBps": 5,
  "maintenanceMarginBps": 100
}
```

### Get Exchange State

```
GET /api/trading/exchange
```

**Response:**
```json
{
  "admin": "...",
  "usdcMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "vault": "...",
  "insuranceFund": "...",
  "marketCount": 25,
  "totalDeposits": 1250.0,
  "totalVolume": "50000000000",
  "totalFeesCollected": 2500.0,
  "insuranceBalance": 100.0,
  "paused": false
}
```

### Get Tradable Products

```
GET /api/trading/tradable
```

**Response:**
```json
{
  "tradableProductIds": [123456, 234567, 345678],
  "products": [
    {
      "productId": 123456,
      "hasMarket": true,
      "marketActive": true,
      "hasOraclePrice": true,
      "oraclePrice": 45.67
    }
  ]
}
```

### Get Market Info

```
GET /api/trading/market/{product_id}
```

**Response:**
```json
{
  "productId": 123456,
  "oraclePriceFeed": "...",
  "maxLeverage": 50,
  "maxOpenInterest": 10000.0,
  "longOpenInterest": 50.0,
  "shortOpenInterest": 30.0,
  "totalVolume": "1000.50",
  "lastFundingTime": 1705312345,
  "cumulativeFundingRateLong": 0.0001,
  "cumulativeFundingRateShort": -0.0001,
  "active": true
}
```

### Get Market Stats

```
GET /api/trading/market/{product_id}/stats
```

**Response:**
```json
{
  "productId": 123456,
  "longOpenInterest": 50.0,
  "shortOpenInterest": 30.0,
  "totalOpenInterest": 80.0,
  "maxOpenInterest": 10000.0,
  "utilizationPercent": 0.8,
  "imbalancePercent": 25.0,
  "totalVolume": "1000.00",
  "maxLeverage": 50,
  "oraclePrice": 45.67,
  "active": true
}
```

### Get Batch Market Stats

```
POST /api/trading/markets/stats
Content-Type: application/json

{ "productIds": [123456, 234567] }
```

### Get User Account

```
GET /api/trading/account/{wallet_address}
```

**Response:**
```json
{
  "exists": true,
  "owner": "YourWalletAddress...",
  "balance": 100.50,
  "totalDeposited": 500.00,
  "totalWithdrawn": 350.00,
  "totalRealizedPnl": -49.50,
  "totalFeesPaid": 2.50,
  "openPositionCount": 2,
  "positions": []
}
```

Note: `positions` is always empty here. Use the positions endpoint below.

### Get User Positions

```
GET /api/trading/account/{wallet_address}/positions
```

**Response:**
```json
{
  "owner": "YourWalletAddress...",
  "positions": [
    {
      "address": "PositionPDAPubkey...",
      "owner": "YourWalletAddress...",
      "productId": 123456,
      "side": "long",
      "size": 100.0,
      "entryPrice": 45.67,
      "leverage": 10,
      "margin": 10.0,
      "liquidationPrice": 41.10,
      "realizedPnl": 0,
      "entryFundingRate": 0,
      "openedAt": 1705312345,
      "lastUpdated": 1705312345
    }
  ],
  "count": 1
}
```

### Get Single Position

```
GET /api/trading/account/{wallet_address}/position/{product_id}
```

### Portfolio (Complete Account + Positions + PnL)

```
GET /api/trading/portfolio/{wallet_address}
```

**Response:**
```json
{
  "exists": true,
  "owner": "YourWalletAddress...",
  "account": {
    "balance": 100.50,
    "totalDeposited": 500.00,
    "totalWithdrawn": 350.00,
    "totalRealizedPnl": -49.50,
    "totalFeesPaid": 2.50,
    "openPositionCount": 2
  },
  "positions": [
    {
      "address": "PositionPDA...",
      "productId": 123456,
      "side": "long",
      "size": 100.0,
      "entryPrice": 45.67,
      "leverage": 10,
      "margin": 10.0,
      "liquidationPrice": 41.10,
      "computed": {
        "currentPrice": 47.50,
        "unrealizedPnl": 4.00,
        "unrealizedPnlPercent": 40.0,
        "marginRatio": 0.71,
        "effectiveLeverage": 14.0,
        "distanceToLiquidation": 8.5,
        "estimatedClosingFee": 0.05,
        "netPnl": 3.95,
        "holdingPeriodSeconds": 7200,
        "riskStatus": "safe"
      }
    }
  ],
  "summary": {
    "totalUnrealizedPnl": 4.00,
    "totalMargin": 10.0,
    "totalSize": 100.0,
    "totalEquity": 114.50,
    "marginUtilization": 8.73,
    "positionCount": 1,
    "positionsAtRisk": 0,
    "largestPosition": 100.0
  }
}
```

**Computed fields:**

| Field | Description |
|---|---|
| `unrealizedPnl` | Current profit/loss in USD |
| `unrealizedPnlPercent` | PnL as % of margin |
| `marginRatio` | `margin / (margin + pnl)` — health indicator |
| `effectiveLeverage` | Current leverage after PnL changes |
| `distanceToLiquidation` | % price move until liquidation |
| `riskStatus` | `safe` (>5%), `warning` (2-5%), `danger` (<2%) |

### Pre-Trade Validation

```
GET /api/trading/prepare-trade/{product_id}?wallet={wallet}&side={long|short}&size={usd}&leverage={1-50}
```

**Response:**
```json
{
  "productId": 123456,
  "canTrade": true,
  "errors": [],
  "warnings": ["High OI imbalance - expect negative funding"],
  "market": {
    "active": true,
    "maxLeverage": 50,
    "longOpenInterest": 50.0,
    "shortOpenInterest": 30.0,
    "maxOpenInterest": 1000000,
    "utilizationPercent": 0.8
  },
  "oracle": {
    "price": 45.67,
    "ageSeconds": 3,
    "isValid": true
  },
  "account": {
    "exists": true,
    "balance": 100.0,
    "hasExistingPosition": false
  },
  "simulation": {
    "side": "long",
    "size": 50.0,
    "leverage": 5,
    "entryPrice": 45.67,
    "margin": 10.0,
    "openingFee": 0.025,
    "marginRequired": 10.025,
    "liquidationPrice": 37.35,
    "distanceToLiquidation": 18.22,
    "wouldExceedOI": false,
    "fundingDirection": "longs pay shorts"
  }
}
```

### Trade Simulation

```
POST /api/trading/simulate
Content-Type: application/json

{
  "productId": 123456,
  "side": "long",
  "size": 100.0,
  "leverage": 10
}
```

**Response:**
```json
{
  "simulation": {
    "productId": 123456,
    "side": "long",
    "size": 100.0,
    "leverage": 10,
    "entryPrice": 45.67,
    "margin": 10.0,
    "openingFee": 0.05,
    "closingFee": 0.05,
    "totalFees": 0.10,
    "marginRequired": 10.05,
    "liquidationPrice": 41.56,
    "breakEvenPrice": 45.72,
    "distanceToLiquidation": 9.0
  },
  "scenarios": [
    { "priceChange": -10, "label": "-10%", "exitPrice": 41.10, "grossPnl": -10.0, "netPnl": -10.10, "roi": -50.37 },
    { "priceChange": -5, "label": "-5%", "exitPrice": 43.39, "grossPnl": -5.0, "netPnl": -5.10, "roi": -25.44 },
    { "priceChange": 0, "label": "0%", "exitPrice": 45.67, "grossPnl": 0, "netPnl": -0.10, "roi": -0.5 },
    { "priceChange": 5, "label": "+5%", "exitPrice": 47.95, "grossPnl": 5.0, "netPnl": 4.90, "roi": 24.44 },
    { "priceChange": 10, "label": "+10%", "exitPrice": 50.24, "grossPnl": 10.0, "netPnl": 9.90, "roi": 49.38 }
  ],
  "market": {
    "longOpenInterest": 5.0,
    "shortOpenInterest": 0,
    "maxOpenInterest": 1000000
  },
  "oracle": {
    "price": 45.67,
    "ageSeconds": 4
  }
}
```

### Market Movers

```
GET /api/trading/analytics/movers?limit={1-50}
```

**Response:**
```json
{
  "gainers": [
    { "productId": 123, "productName": "Charizard ex", "currentPrice": 50.0, "change24h": 15.3, "change30d": 10.5, "activityScore": 85.0 }
  ],
  "losers": [
    { "productId": 456, "productName": "Pikachu VMAX", "currentPrice": 20.0, "change24h": -8.5, "change30d": -5.2, "activityScore": 78.0 }
  ],
  "mostVolatile": [
    { "productId": 123, "productName": "Charizard ex", "currentPrice": 50.0, "change24h": 15.3, "change30d": 10.5, "activityScore": 85.0 }
  ],
  "biggestMover": { "productId": 123, "productName": "Charizard ex", "currentPrice": 50.0, "change24h": 15.3 },
  "timestamp": 1771404882514
}
```

---

## Transaction Endpoints

These return Solana transaction parameters. You must build, sign, and submit the transaction yourself.

### Create Trading Account

```
POST /api/trading/tx/create-account
Content-Type: application/json

{ "owner": "YourWalletPublicKey" }
```

**Response:**
```json
{
  "success": true,
  "params": {
    "programId": "8hH5CWo14R5QhaFUuXpxJytchS6NgrhRLHASyVeriEvN",
    "instruction": "createUserAccount",
    "accounts": {
      "userAccount": "DerivedPDA...",
      "owner": "YourWalletPublicKey",
      "systemProgram": "11111111111111111111111111111111"
    }
  }
}
```

### Deposit USDC

```
POST /api/trading/tx/deposit
Content-Type: application/json

{
  "owner": "YourWalletPublicKey",
  "userTokenAccount": "YourUSDCTokenAccount",
  "amount": 100.0
}
```

Amount is in USD (e.g., 100.0 = $100 USDC). The backend converts to base units (6 decimals).

### Withdraw USDC

```
POST /api/trading/tx/withdraw
Content-Type: application/json

{
  "owner": "YourWalletPublicKey",
  "userTokenAccount": "YourUSDCTokenAccount",
  "amount": 50.0
}
```

### Open Position

```
POST /api/trading/tx/open-position
Content-Type: application/json

{
  "owner": "YourWalletPublicKey",
  "productId": 123456,
  "side": "long",
  "size": 100.0,
  "leverage": 10
}
```

- `side`: `"long"` or `"short"`
- `size`: Position size in USD ($1 min, $100k max)
- `leverage`: 1–50x

**Response includes a signed oracle price:**
```json
{
  "success": true,
  "params": {
    "programId": "...",
    "instruction": "openPosition",
    "accounts": { "...": "..." },
    "args": {
      "productId": 123456,
      "side": 0,
      "size": "100000000",
      "leverage": 10
    }
  },
  "oraclePrice": 45.67,
  "oracleAge": 2,
  "signedPrice": {
    "price": "4567000000",
    "timestamp": 1705312345,
    "signature": "base64...",
    "publicKey": "base64...",
    "message": "base64..."
  }
}
```

The `signedPrice` must be included as an Ed25519SigVerify precompile instruction. See [TRANSACTIONS.md](TRANSACTIONS.md) for details.

**Rate limit**: 2 requests per 10 seconds per IP per product.

### Close Position

```
POST /api/trading/tx/close-position
Content-Type: application/json

{
  "owner": "YourWalletPublicKey",
  "productId": 123456
}
```

Also returns `signedPrice` — same Ed25519 flow as open.

### Add Margin

```
POST /api/trading/tx/add-margin
Content-Type: application/json

{
  "owner": "YourWalletPublicKey",
  "productId": 123456,
  "amount": 10.0
}
```

### Close Trading Account

```
POST /api/trading/tx/close-account
Content-Type: application/json

{ "owner": "YourWalletPublicKey" }
```

Must have zero balance and no open positions.

---

## WebSocket Real-Time Feed

Connect to `wss://backend.pokeperps.fun/ws/trading`.

**Subscribe to products:**
```json
{ "type": "subscribe", "products": [123456, 234567] }
```

**Subscribe to account updates:**
```json
{ "type": "subscribe", "accounts": ["YourWalletAddress"] }
```

**Unsubscribe:**
```json
{ "type": "unsubscribe", "products": [123456] }
```

**Keep-alive (send every 30s):**
```json
{ "type": "ping" }
```

**Server messages:**

| Type | Data |
|---|---|
| `connected` | `{ clientId, clientCount }` |
| `pong` | `{ clientCount }` |
| `price_update` | `{ prices: [{ productId, price, source }] }` |
| `position_opened` | Position details |
| `position_closed` | Position details |
| `market_created` | Market details |
| `market_stats` | Stats update |
| `account_update` | Account balance change |

---

## Complete Error Reference

### On-Chain Program Errors

| Code | Name | Meaning |
|---|---|---|
| 6006 | OracleUnauthorized | Not the oracle authority |
| 6012 | InvalidAmount | Zero or negative amount |
| 6013 | InsufficientBalance | Not enough USDC in trading account |
| 6014 | ExchangePaused | Entire exchange is paused |
| 6015 | InvalidLeverage | Leverage out of 1-50 range |
| 6016 | PositionTooSmall | Below $1 minimum |
| 6017 | ProductMismatch | Position product ID doesn't match market |
| 6018 | MarketInactive | Market is paused/inactive |
| 6019 | MaxOpenInterestExceeded | Market open interest at capacity |
| 6020 | PositionNotLiquidatable | Position margin above maintenance |
| 6021 | InvalidOraclePrice | Oracle price invalid or zero |
| 6022 | MathOverflow | Arithmetic overflow |
| 6023 | FundingTooEarly | Funding rate already cranked this interval |
| 6024 | Unauthorized | Not the admin |
| 6025 | TooManyMarkets | 100,000 market limit hit |
| 6026 | HasBalance | Cannot close account with remaining balance |
| 6027 | HasOpenPositions | Cannot close account with open positions |
| 6030 | OraclePriceStale | Oracle price older than 15 seconds |
| 6031 | PositionTooLarge | Above $100k maximum |
| 6032 | InvalidTokenAccountOwner | Token account ownership mismatch |
| 6035 | InvalidEd25519Instruction | Ed25519 precompile instruction malformed or missing |
| 6036 | InvalidSignedPrice | Signed oracle price data is invalid |

Note: Error codes 6007-6011, 6028-6029, 6033-6034 are not used.

### Common API Errors

| Status | Cause | Fix |
|---|---|---|
| 400 | Invalid parameters | Check param types and ranges |
| 404 | Product/market/account not found | Verify product ID exists, check tradable list |
| 429 | Rate limited | Wait and retry (300 req/min global, 2 per 10s for oracle signing) |
| 500 | Server error | Retry after a moment |

---

## Decision-Making Data

| Data Point | Endpoint | Field | Significance |
|---|---|---|---|
| Current price | `GET /api/trading/oracle/{id}` | `price` | Real-time TCGPlayer price |
| 24h change | `GET /api/cards/{id}` | `analysis.change_24h` | Recent momentum |
| 30d change | `GET /api/cards/{id}` | `analysis.change_30d` | Medium-term trend |
| Activity score | `GET /api/cards/{id}` | `analysis.activity_score` | Trading volume/liquidity (0-100) |
| Price history | `GET /api/cards/{id}/history` | `dates` + `prices` | Time series for analysis |
| Listings count | `GET /api/cards/{id}` | `product.listings` | Supply available |
| Lowest listing | `GET /api/cards/{id}` | `product.lowest_price` | Floor price |
| Recent sales | `GET /api/cards/{id}` | `recent_sales[]` | Actual transaction prices |
| Long vs Short OI | `GET /api/trading/market/{id}/stats` | `longOpenInterest`, `shortOpenInterest` | Market sentiment |
| OI imbalance | `GET /api/trading/market/{id}/stats` | `imbalancePercent` | Funding rate direction |
| Utilization | `GET /api/trading/market/{id}/stats` | `utilizationPercent` | Market capacity |
| Biggest mover | `GET /api/dashboard` | `biggest_mover` | Highest 24h change |

## Cache Strategy

| Endpoint | Recommended TTL |
|---|---|
| `/api/trading/tradable` | 5 minutes |
| `/api/trading/config` | 1 hour |
| `/api/cards/{id}/bundle` | 2 minutes |
| `/api/trading/oracle/{id}` | 10 seconds |
| `/api/trading/portfolio` | 30 seconds |
| `/api/cards/{id}/signals` | 5 minutes |
