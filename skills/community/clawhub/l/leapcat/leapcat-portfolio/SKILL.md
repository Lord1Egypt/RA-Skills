---
name: leapcat-portfolio
description: View portfolio overview and stock positions on Leapcat via the leapcat CLI.
homepage: https://leapcat.ai
---

# LeapCat Portfolio Skill

View portfolio overview and stock positions using the leapcat. These are read-only commands for checking the user's current holdings and performance.

## Prerequisites

- Node.js 18+ is required (commands use `npx leapcat@0.1.1` which auto-downloads the CLI)
- User must be authenticated — run `npx leapcat@0.1.1 auth login --email <email>` first

## Commands

### portfolio overview

Get a high-level summary of the user's portfolio including total value, profit/loss, and asset allocation.

```bash
npx leapcat@0.1.1 portfolio overview --json
```

### portfolio positions

List all current stock positions with details such as symbol, quantity, average cost, current price, and unrealized P&L.

```bash
npx leapcat@0.1.1 portfolio positions --json
```

## Workflow

1. **Check portfolio overview** — Run `portfolio overview --json` to get a summary of total portfolio value and performance.
2. **View positions** — Run `portfolio positions --json` to see individual stock holdings and their current status.
3. **Cross-reference with market data** — Use `market quote --symbol <symbol> --exchange <exchange> --json` to get real-time prices for specific positions.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `NOT_AUTHENTICATED` | Session expired | Re-authenticate with `auth login` |
| `TOKEN_EXPIRED` | Auth token has expired | Run `auth refresh --json` |
