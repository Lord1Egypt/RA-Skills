---
name: leapcat-trading
description: Place, monitor, and cancel stock trading orders on Leapcat via the leapcat CLI.
homepage: https://leapcat.ai
---

# LeapCat Stock Trading Skill

Place, monitor, and cancel stock trading orders using the leapcat.

## Prerequisites

- Node.js 18+ is required (commands use `npx leapcat@0.1.1` which auto-downloads the CLI)
- User must be authenticated — run `npx leapcat@0.1.1 auth login --email <email>` first
- KYC must be completed and approved
- Trade password must be set

## Commands

### trading place-order

Place a new stock order (buy or sell).

```bash
npx leapcat@0.1.1 trading place-order \
  --symbol <symbol> \
  --exchange <exchange> \
  --side <BUY|SELL> \
  --order-type <LIMIT|MARKET> \
  --quantity <qty> \
  [--price <price>] \
  [--source <source>] \
  [--stock-name <name>] \
  [--idempotency-key <key>] \
  --json
```

**Parameters:**
- `--symbol <symbol>` — Stock ticker symbol (e.g., `AAPL`, `9988.HK`)
- `--exchange <exchange>` — Exchange code (e.g., `NASDAQ`, `HKEX`)
- `--side <BUY|SELL>` — Order direction
- `--order-type <LIMIT|MARKET>` — Order type; use `LIMIT` for a specific price or `MARKET` for best available price
- `--quantity <qty>` — Number of shares
- `--price <price>` — Limit price (required for LIMIT orders, ignored for MARKET)
- `--source <source>` — Order source identifier (default: `CLI`)
- `--stock-name <name>` — Human-readable stock name (optional, for display purposes)
- `--idempotency-key <key>` — Unique key to prevent duplicate orders (optional but recommended)

### trading list-orders

List the user's orders with optional filters.

```bash
npx leapcat@0.1.1 trading list-orders [--status <status>] [--symbol <symbol>] --json
```

**Parameters:**
- `--status <status>` — Filter by order status (e.g., `PENDING`, `FILLED`, `CANCELLED`)
- `--symbol <symbol>` — Filter by stock symbol

### trading get-order

Get details of a specific order.

```bash
npx leapcat@0.1.1 trading get-order --order-id <id> --json
```

**Parameters:**
- `--order-id <id>` — The order identifier

### trading cancel-order

Cancel a pending order.

```bash
npx leapcat@0.1.1 trading cancel-order --order-id <id> --json
```

**Parameters:**
- `--order-id <id>` — The order identifier to cancel

## Workflow

1. **Get a market quote** — Use `npx leapcat@0.1.1 market quote --symbol <symbol> --exchange <exchange> --json` to check the current price.
2. **Place an order** — Run `trading place-order` with the desired parameters. For limit orders, set `--price` based on the quote data. Consider using `--idempotency-key` to avoid duplicate submissions.
3. **Monitor order status** — Run `trading get-order --order-id <id> --json` or `trading list-orders --json` to track the order.
4. **Cancel if needed** — Run `trading cancel-order --order-id <id> --json` to cancel a pending/unfilled order.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `NOT_AUTHENTICATED` | Session expired | Re-authenticate with `auth login` |
| `KYC_NOT_APPROVED` | KYC verification incomplete | Complete the KYC flow first |
| `TRADE_PASSWORD_NOT_SET` | Trade password required | Set via `auth trade-password set` |
| `INSUFFICIENT_BALANCE` | Not enough funds for the buy order | Deposit funds via wallet |
| `INVALID_SYMBOL` | Unrecognized stock symbol | Verify symbol with `market stocks --json` |
| `MARKET_CLOSED` | Market is not open for trading | Wait for market hours or place a limit order |
| `ORDER_NOT_FOUND` | Invalid order ID | Re-check with `trading list-orders --json` |
| `CANCEL_NOT_ALLOWED` | Order already filled or cancelled | No further action possible |
| `DUPLICATE_ORDER` | Idempotency key already used | Use a new idempotency key or check existing order |
