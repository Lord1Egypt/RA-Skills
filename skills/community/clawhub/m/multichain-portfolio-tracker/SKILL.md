---
name: crypto-portfolio-tracker
version: 1.0.0
description: Track multi-chain crypto portfolio with real-time prices, P&L, and alerts. Supports EVM (Ethereum, Base, Arbitrum, Polygon, Optimism), Solana, and manual entries. No API keys needed for basic tracking (uses free public RPCs and CoinGecko). Use when checking wallet balances, portfolio value, token prices, P&L tracking, or setting price alerts.
---

# Crypto Portfolio Tracker

Track your crypto portfolio across multiple chains with real-time prices, P&L calculation, and optional alerts. Zero API keys needed for basic functionality.

## Quick Start

```bash
# Check a single wallet
bash scripts/check-wallet.sh 0xYourAddress ethereum

# Full portfolio scan (all configured wallets)
bash scripts/portfolio.sh

# Price check
bash scripts/price.sh BTC ETH SOL
```

## Configuration

Create `portfolio.json` in your workspace:

```json
{
  "wallets": [
    { "address": "0x...", "chain": "ethereum", "label": "Main" },
    { "address": "0x...", "chain": "base", "label": "Trading" },
    { "address": "0x...", "chain": "arbitrum", "label": "DeFi" },
    { "address": "C122gx...", "chain": "solana", "label": "SOL Wallet" }
  ],
  "manual": [
    { "token": "BTC", "amount": 0.5, "cost_basis": 30000 }
  ],
  "alerts": [
    { "token": "BTC", "above": 70000, "message": "BTC broke $70K!" },
    { "token": "ETH", "below": 2000, "message": "ETH dropped below $2K" }
  ]
}
```

## Features

### Portfolio Overview
```bash
bash scripts/portfolio.sh
```
Output:
```
📊 Portfolio — 31 Mar 2026

Wallet: Main (ethereum)
  0.5 ETH = $1,250.00
  1000 USDC = $1,000.00

Wallet: Trading (base)
  500 USDC = $500.00

Total: $2,750.00
24h Change: +$45.20 (+1.67%)
```

### Price Tracking
```bash
bash scripts/price.sh BTC ETH SOL MATIC
```
Uses CoinGecko free API (no key, 30 calls/min).

### Native Balance Check
```bash
# EVM chains (free public RPC)
bash scripts/check-wallet.sh 0xAddress ethereum|base|arbitrum|polygon|optimism

# Solana
bash scripts/check-wallet.sh SolAddress solana
```

### P&L Calculation
```bash
bash scripts/pnl.sh
```
Compares current value vs cost basis (from `portfolio.json` manual entries or historical snapshots).

### Price Alerts
```bash
bash scripts/alerts.sh
```
Checks configured alerts and outputs triggered ones. Run via cron for continuous monitoring.

## Supported Chains

| Chain | RPC | Token Standard |
|-------|-----|---------------|
| Ethereum | etherscan free / public RPC | ERC-20 |
| Base | basescan / public RPC | ERC-20 |
| Arbitrum | arbiscan / public RPC | ERC-20 |
| Polygon | polygonscan / public RPC | ERC-20 |
| Optimism | optimistic.etherscan / public RPC | ERC-20 |
| Solana | solana mainnet-beta RPC | SPL |

## Cron Integration

Add to OpenClaw cron for automated tracking:

```
Portfolio snapshot: bash ~/path/to/scripts/portfolio.sh --json >> ~/portfolio-history.jsonl
Price alerts: bash ~/path/to/scripts/alerts.sh
```

## Data Sources

- **Prices**: CoinGecko free API (no key, rate limited to 30/min)
- **EVM balances**: Public RPCs or Etherscan free tier
- **Solana balances**: solana CLI or public RPC
- **Token lists**: CoinGecko token list

## Limitations

- CoinGecko free tier: 30 calls/min, no historical data beyond 1 year
- Public RPCs may rate limit under heavy use
- ERC-20 token detection requires known token list (top 500 by market cap)
- For full token scanning, consider adding Moralis or Alchemy API keys
