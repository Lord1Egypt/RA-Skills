# DEX Concepts

Key concepts for understanding DEX integrations in the Indigo ecosystem.

## SteelSwap

SteelSwap is a DEX aggregator on Cardano that finds the best swap route across multiple liquidity sources. It:

- Aggregates liquidity from multiple Cardano DEXs
- Finds optimal routes (direct or multi-hop) for each trade
- Provides swap estimates with price impact before execution
- Supports all major Cardano tokens including iAssets and INDY

## Iris DEX

Iris is a decentralized exchange on Cardano with concentrated liquidity pools. Key features:

- **Liquidity pools** — paired token pools with configurable fee tiers
- **TVL tracking** — total value locked in each pool
- **Volume data** — 24-hour trading volume per pool

## Blockfrost

Blockfrost is a Cardano blockchain API that provides:

- Wallet balance queries by address
- Token metadata lookup
- Transaction history

The `get_blockfrost_balances` tool uses Blockfrost to retrieve all tokens held by a wallet.

## Token Identification

Cardano tokens are identified by:

| Field | Description | Example |
|-------|-------------|---------|
| Policy ID | Unique minting policy hash | `f0ff48...a3b2` |
| Asset name | On-chain name (hex encoded) | `695553442` (iUSD) |
| Ticker | Human-readable symbol | `iUSD` |

SteelSwap accepts both tickers and policy IDs for swap estimates.

## Price Impact

Price impact measures how much a trade moves the market price:

| Impact | Level | Guidance |
|--------|-------|----------|
| < 0.1% | Negligible | Safe to execute |
| 0.1-1% | Low | Normal for medium trades |
| 1-5% | Moderate | Consider splitting the trade |
| > 5% | High | Split into smaller trades or use limit orders |

## Swap Routing

SteelSwap may route swaps through intermediate tokens for better prices:

- **Direct route:** ADA → iUSD (single pool)
- **Multi-hop route:** ADA → USDC → iUSD (through two pools)

The aggregator automatically selects the most efficient route.
