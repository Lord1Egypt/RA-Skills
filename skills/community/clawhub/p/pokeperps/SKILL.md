---
name: pokeperps
description: Trade perpetual futures on Pokemon TCG card prices via the PokePerps DEX on Solana. Search cards, analyze prices, simulate trades, open/close leveraged long/short positions, and manage portfolios. Use when the user asks about Pokemon card trading, perpetual futures, or PokePerps.
license: BUSL-1.1
compatibility: Requires network access to https://backend.pokeperps.fun. Optional Solana keypair for trade execution.
metadata:
  author: ankushKun
  version: "1.0"
  website: https://pokeperps.fun
  blockchain: solana
---

# PokePerps AI Agent Skill

> **Platform**: [PokePerps](https://pokeperps.fun) — Decentralized Perpetual Futures Exchange for Pokemon TCG Card Prices
> **Blockchain**: Solana (mainnet-beta)
> **Backend API**: `https://backend.pokeperps.fun`
> **WebSocket**: `wss://backend.pokeperps.fun/ws/trading`
> **Program ID**: `8hH5CWo14R5QhaFUuXpxJytchS6NgrhRLHASyVeriEvN`
> **Collateral**: USDC (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`)

PokePerps lets you trade **perpetual futures contracts** on real Pokemon Trading Card Game card prices. Prices are sourced from TCGPlayer marketplace in real-time and published on-chain via an Ed25519-signed oracle.

## MCP Server (Recommended)

The easiest way for AI agents to interact with PokePerps is via the **Model Context Protocol (MCP) server**.

**Read-only mode** (no wallet required):
```json
{
  "mcpServers": {
    "pokeperps": {
      "command": "npx",
      "args": ["@pokeperps/mcp"]
    }
  }
}
```

**With trade execution** (requires Solana keypair):
```json
{
  "mcpServers": {
    "pokeperps": {
      "command": "npx",
      "args": ["@pokeperps/mcp"],
      "env": {
        "POKEPERPS_KEYPAIR": "/path/to/your/keypair.json"
      }
    }
  }
}
```

### MCP Environment Variables

| Variable | Description | Default |
|---|---|---|
| `POKEPERPS_KEYPAIR` | Path to Solana keypair JSON | (none - read-only mode) |
| `POKEPERPS_API_URL` | Backend API URL | `https://backend.pokeperps.fun` |
| `POKEPERPS_RPC_URL` | Solana RPC URL | `https://api.mainnet-beta.solana.com` |

### MCP Tools

**Read-only tools** (always available):

| Tool | Description |
|---|---|
| `get_market_movers` | Top gainers, losers, and most volatile cards |
| `get_portfolio` | Complete portfolio with computed PnL for a wallet |
| `get_trading_signals` | Pre-computed trading signals and recommendations |
| `prepare_trade` | Validate a trade before opening (margin, fees, risks) |
| `simulate_trade` | Simulate PnL scenarios at different price levels |
| `search_cards` | Search Pokemon cards by name |
| `get_card_details` | Full card info with listings, sales, history |
| `batch_get_cards` | Fetch up to 50 cards in one request |
| `get_tradable_products` | List all product IDs with active markets |
| `get_trading_config` | Trading parameters (leverage, fees, etc.) |

**Execution tools** (require `POKEPERPS_KEYPAIR`):

| Tool | Description |
|---|---|
| `open_position` | Open a new long/short position |
| `close_position` | Close an existing position to realize PnL |
| `deposit` | Deposit USDC into trading account |
| `withdraw` | Withdraw USDC from trading account |
| `get_wallet_status` | Check wallet balance and execution status |

### MCP Resources

- `pokeperps://docs/trading-guide` — Trading guide and risk parameters
- `pokeperps://docs/api-reference` — Full OpenAPI specification

## Trading Parameters

| Parameter | Value |
|---|---|
| Max leverage | 50x |
| Min position size | $1 USDC |
| Max position per user | $100,000 USDC |
| Trading fee | 0.05% (5 bps) on open and close |
| Maintenance margin | 1% (100 bps) |
| Liquidation fee | 0.5% to liquidator + 0.5% to insurance |
| Funding interval | 8 hours |
| Funding rate cap | ±0.05% per interval |
| Oracle price max age | 15 seconds |
| Collateral | USDC (SPL Token) |

**What you can do:**
- Go **long** (bet price goes up) or **short** (bet price goes down)
- Use 1x–50x leverage
- Positions have no expiry (perpetual)
- Close anytime to realize PnL
- Prices track real TCGPlayer marketplace prices

## Architecture

```
Agent (you)
  │
  ├── REST API (https://backend.pokeperps.fun/api/...)
  │     ├── Read-only: card data, prices, markets, positions
  │     └── Transaction builders: returns params for Solana transactions
  │
  ├── WebSocket (wss://backend.pokeperps.fun/ws/trading)
  │     └── Real-time price updates, position events
  │
  └── Solana RPC (https://api.mainnet-beta.solana.com)
        └── Sign & send transactions built from API params
```

The backend does NOT sign or submit transactions. It provides instruction data and account addresses. You build, sign, and submit transactions client-side.

## Key API Endpoints

Base URL: `https://backend.pokeperps.fun`

### Card Discovery

| Method | Path | Description |
|---|---|---|
| GET | `/api/cards/search?q={query}&limit={1-50}` | Search cards by name |
| GET | `/api/dashboard?limit={1-200}` | Top tradable cards + biggest mover |
| GET | `/api/cards/{product_id}` | Full card details |
| GET | `/api/cards/{product_id}/bundle` | All card data in one call |
| GET | `/api/cards/{product_id}/history?range=month` | Price history |
| GET | `/api/cards/{product_id}/signals` | Trading signals & recommendations |
| POST | `/api/cards/batch` | Fetch up to 50 cards at once |

### Trading

| Method | Path | Description |
|---|---|---|
| GET | `/api/trading/tradable` | All tradable product IDs |
| GET | `/api/trading/config` | Trading parameters |
| GET | `/api/trading/exchange` | Exchange state |
| GET | `/api/trading/market/{product_id}` | Market state |
| GET | `/api/trading/market/{product_id}/stats` | Market statistics |
| GET | `/api/trading/account/{wallet}` | User account |
| GET | `/api/trading/account/{wallet}/positions` | User positions |
| GET | `/api/trading/portfolio/{wallet}` | Full portfolio with computed PnL |
| GET | `/api/trading/prepare-trade/{id}?wallet=X&side=Y&size=Z&leverage=W` | Pre-trade validation |
| POST | `/api/trading/simulate` | Trade simulation with scenarios |
| GET | `/api/trading/analytics/movers?limit={1-50}` | Top gainers, losers, volatile |

### Transaction Builders

| Method | Path | Description |
|---|---|---|
| POST | `/api/trading/tx/create-account` | Create trading account |
| POST | `/api/trading/tx/deposit` | Deposit USDC |
| POST | `/api/trading/tx/withdraw` | Withdraw USDC |
| POST | `/api/trading/tx/open-position` | Open long/short position |
| POST | `/api/trading/tx/close-position` | Close position |
| POST | `/api/trading/tx/add-margin` | Add margin to position |

### Oracle

| Method | Path | Description |
|---|---|---|
| GET | `/api/oracle/prices` | All current oracle prices |
| GET | `/api/oracle/router/prices` | Best available prices |
| GET | `/api/trading/oracle/{product_id}` | Single product price |
| POST | `/api/trading/oracle/prices` | Batch oracle prices |

See [references/API.md](references/API.md) for full request/response schemas.

## Optimized Trading Flow

```
1. GET /api/trading/analytics/movers       → Find opportunities
2. POST /api/cards/batch                   → Fetch details for candidates
3. GET /api/cards/{id}/signals             → Get trading recommendation
4. GET /api/trading/prepare-trade/{id}     → Validate trade
5. POST /api/trading/tx/open-position      → Execute trade
6. GET /api/trading/portfolio/{wallet}     → Monitor positions
```

This uses **6 API calls** instead of 15+ in the traditional flow.

## PnL Calculation

```
margin = size / leverage
fee = size * 0.0005  (0.05% on open, same on close)

For long:
  unrealized_pnl = size * (current_price - entry_price) / entry_price
  liquidation_price = entry_price * (1 - (margin - maintenance_margin) / size)

For short:
  unrealized_pnl = size * (entry_price - current_price) / entry_price
  liquidation_price = entry_price * (1 + (margin - maintenance_margin) / size)

Maintenance margin = size * 0.01 (1%)
```

## Decision-Making Signals

Use `/api/cards/{id}/signals` for pre-computed analysis:

**Bullish (go long):**
- Positive `change_24h` with high `activity_score`
- Recent sales trending above `market_price`
- Decreasing listing count (supply shrinking)
- High short OI relative to long (potential short squeeze)

**Bearish (go short):**
- Negative `change_24h` and `change_30d`
- Recent sales trending below `market_price`
- Increasing listing count (supply growing)
- High long OI relative to short (potential long squeeze)

## WebSocket

Connect to `wss://backend.pokeperps.fun/ws/trading`:

```json
{ "type": "subscribe", "products": [123456], "accounts": ["YourWallet"] }
{ "type": "ping" }
```

Events: `price_update`, `position_opened`, `position_closed`, `market_stats`, `account_update`

## Rate Limits

| Limit | Value |
|---|---|
| Global API rate limit | 300 requests/min per IP |
| Oracle price signing | 2 per 10 seconds per IP per product |
| WebSocket connections | 25 per IP, 1000 total |
| Max batch product IDs | 200 per request |

## Error Codes

| Code | Name | Meaning |
|---|---|---|
| 6012 | InvalidAmount | Zero or negative amount |
| 6013 | InsufficientBalance | Not enough USDC |
| 6014 | ExchangePaused | Exchange is paused |
| 6015 | InvalidLeverage | Outside 1-50 range |
| 6016 | PositionTooSmall | Below $1 minimum |
| 6018 | MarketInactive | Market disabled |
| 6019 | MaxOpenInterestExceeded | OI at capacity |
| 6030 | OraclePriceStale | Price older than 15s |
| 6031 | PositionTooLarge | Above $100k max |
| 6035 | InvalidEd25519Instruction | Ed25519 precompile malformed |

See [references/API.md](references/API.md) for full error reference.

## Agent Best Practices

### Minimize API Calls

| Instead of... | Use... |
|---|---|
| `GET /account` + `GET /positions` + oracle calls | `GET /api/trading/portfolio/{wallet}` (1 call) |
| Multiple `GET /api/cards/{id}` calls | `POST /api/cards/batch` (1 call for up to 50) |
| 5+ calls to validate a trade | `GET /api/trading/prepare-trade/{id}` (1 call) |
| Scanning all cards for movers | `GET /api/trading/analytics/movers` (1 call) |

### Position Management

1. Check `riskStatus` before opening new positions — avoid if `warning` or `danger`
2. Use `distanceToLiquidation` for stop-loss (conservative: close if <10%, moderate: <5%)
3. Monitor `fundingDirection` — avoid positions that pay funding
4. Check `wouldExceedOI` before large trades

### Security

- Always verify PDAs client-side before signing transactions
- Never expose private keys in API calls
- Validate `oracleAge` < 15 seconds before trading
- Check `canTrade` from `prepare-trade` before proceeding

## Additional References

- [references/API.md](references/API.md) — Full API request/response schemas
- [references/TRANSACTIONS.md](references/TRANSACTIONS.md) — On-chain transaction construction, PDA derivation, Ed25519 signing
- [references/EXAMPLES.md](references/EXAMPLES.md) — Complete code examples (TypeScript, Python, cURL)
