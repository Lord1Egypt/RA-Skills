# 🎯 Manual Trade Placement

Place trades on Polymarket through your AI agent. Say what you want to buy, and it handles market resolution, price discovery, and order execution.

Supports instant fills (FAK), limit orders (GTC), Simmer market IDs, and full Polymarket URLs with auto-import.

## Quick Start

```
> "Buy YES $10 on will-bitcoin-hit-100k"
> "Place a GTC limit NO $20 at 0.35 on [polymarket URL]"
```

## Example Output

```
=======================================================
🎯  Manual Trade Placement  [polymarket-manual-trade]
=======================================================
  ✅ Will Bitcoin reach $100,000 by June 2026?
     ID: abc123-def456
  Side: YES | Amount: $10.00 | Order: FAK | Venue: polymarket
  📊 Book: ask=0.62 bid=0.60 → auto-price=0.63

  🚀 Placing order...

=======================================================
  ✅ MATCHED | 15.87 shares | $10.00 spent
     Trade ID: trade_789xyz
=======================================================
```

## Arguments

| Flag | Description | Default |
|------|-------------|---------|
| `--market` / `-m` | Simmer market ID or full Polymarket URL | *(required)* |
| `--side` / `-s` | `YES` or `NO` | *(required)* |
| `--amount` / `-a` | Dollar amount | `$10` |
| `--order` / `-o` | `FAK`, `GTC`, or `FOK` | `FAK` |
| `--price` / `-p` | Limit price (auto if omitted) | auto |
| `--venue` / `-v` | `polymarket` or `sim` | `polymarket` |
| `--cancel` | Cancel all open orders on market | — |
| `--cancel-side` | Cancel only `yes` or `no` side | — |
| `--dry-run` | Preview without placing | — |

## Order Types

### FAK (Fill-and-Kill) — Default
Fills immediately at best ask + $0.01. Any unfilled remainder is cancelled. Use when you want in *now* at market price.

### GTC (Good-Til-Cancelled)
Places a limit order on the CLOB book at your specified price. Funds are locked on placement. The order stays live until the market reaches your price or you cancel. Use when you want a *specific* entry price.

### FOK (Fill-or-Kill)
Must fill the entire amount or nothing. Rarely needed — FAK is almost always better.

## Requirements

| Requirement | Details |
|------------|---------|
| `SIMMER_API_KEY` | Your Simmer API key |
| `WALLET_PRIVATE_KEY` | Polymarket wallet private key |
| `simmer-sdk` | `>= 0.8.32` |

## Tunables

Configure defaults in `clawhub.json`:

- **default_order_type** — `FAK` / `GTC` / `FOK`
- **default_amount** — dollar amount per trade
- **default_venue** — `polymarket` / `sim`

---

Built for [Simmer](https://www.simmer.markets/) — the AI trading agent platform for Polymarket and Kalshi.
