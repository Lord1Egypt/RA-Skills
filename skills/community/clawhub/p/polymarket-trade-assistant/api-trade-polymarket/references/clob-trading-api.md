# Polymarket CLOB Trading API Reference

Base URL: `https://clob.polymarket.com`
Chain: Polygon (chain ID 137)

## Authentication

### Create or Derive API Key

The `@polymarket/clob-client` handles authentication automatically via `createOrDeriveApiKey()`.

Flow:
1. Create a temporary `ClobClient` with signer (wallet)
2. Call `client.createOrDeriveApiKey()` — returns `{ apiKey, secret, passphrase }`
3. Recreate `ClobClient` with credentials, signatureType, and funderAddress

```typescript
const signer = new Wallet(privateKey);
const temp = new ClobClient(HOST, CHAIN_ID, signer);
const creds = await temp.createOrDeriveApiKey();
const client = new ClobClient(HOST, CHAIN_ID, signer, creds, signatureType, funderAddress);
```

### Signature Types
- `0` — EOA (Externally Owned Account, direct wallet)
- `1` — Proxy (MagicLink / Polymarket proxy wallet)
- `2` — Gnosis Safe (multisig)

## Order Endpoints

### Place Limit Order (GTC)

```typescript
const resp = await client.createAndPostOrder(
  { tokenID, price, size, side: Side.BUY | Side.SELL },
  undefined,  // options
  OrderType.GTC,
);
// resp: { orderID: string, status: string }
```

Parameters:
- `tokenID` — CLOB token ID for the outcome
- `price` — limit price (0 to 1, e.g., 0.068)
- `size` — number of shares
- `side` — `Side.BUY` or `Side.SELL`

### Place Market Order (FOK)

```typescript
const resp = await client.createAndPostMarketOrder(
  { tokenID, amount, side: Side.BUY | Side.SELL },
  undefined,
  OrderType.FOK,
);
// resp: { orderID: string, status: string }
```

Parameters:
- `tokenID` — CLOB token ID
- `amount` — USD amount to spend
- `side` — `Side.BUY` or `Side.SELL`

### Order Statuses
- `delayed` — order submitted, not yet confirmed
- `live` — order on the book (GTC)
- `matched` — order partially or fully matched
- `filled` — order fully filled
- `canceled` / `cancelled` — order cancelled

## Cancel Endpoints

### Cancel Single Order

```typescript
await client.cancelOrder({ orderID: "0x..." });
```

### Cancel All Orders

```typescript
await client.cancelAll();
```

## Query Endpoints

### Get Order

```typescript
const order = await client.getOrder(orderID);
// order: { id, status, side, price, size, ... }
```

### Get Order Book

```typescript
const book = await client.getOrderBook(tokenID);
// book: { bids: [{ price, size }], asks: [{ price, size }] }
```

Bids are sorted highest-first, asks lowest-first.

## Balance Endpoint

### Get Balance and Allowance

```typescript
const resp = await client.getBalanceAllowance();
// resp: { balance: string, allowance: string }
```

Returns USDC balance and CTF exchange allowance.

## Positions Endpoint

### Get Positions

```
GET https://clob.polymarket.com/positions?address=<wallet_address>
```

Returns array of position objects with `asset` (token ID), `size`, and `avg_price`.

## Market Resolution

### Gamma API — Market Lookup

```
GET https://gamma-api.polymarket.com/events?slug=<event_slug>
```

Returns event data including markets with `clobTokenIds` mapped to outcomes (Yes/No).

## Rate Limits

- Order placement: ~10 req/s
- Order book reads: ~30 req/s
- Positions/balance: ~10 req/s

Use appropriate delays between rapid sequential calls.

## Error Handling

Common error patterns:
- `INSUFFICIENT_BALANCE` — not enough USDC
- `INVALID_PRICE` — price out of range (must be 0.001 to 0.999)
- `INVALID_SIZE` — size too small (minimum ~1 share)
- `ORDER_NOT_FOUND` — invalid order ID for cancel
- `UNAUTHORIZED` — API key expired or invalid, re-derive
