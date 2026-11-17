---
name: nft-floor-sweep-calculator
description: Calculates the total cost of sweeping N items off an NFT collection's floor, pulling live floor prices from Magic Eden (Solana collections) or CoinGecko's free NFT API (EVM collections) with no API key required, then applying marketplace fees and a configurable naive price-step slippage curve to estimate total spend, average price per item, and subtotal before fees. Useful for NFT trading, crypto whale-style bulk buying, defi and passive income research, python developers, and ai agent operators who want a quick pre-trade cost estimate before executing a floor sweep. Not an execution engine — it does not place orders or touch a wallet, purely a cost calculator for planning purposes on Solana and EVM NFT collections.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# NFT Floor Sweep Calculator

Pulls a collection's current floor price and estimates the total cost of
buying N items off the floor, including marketplace fees and a naive
per-item price-step assumption (since free public APIs don't expose full
order-book depth).

## When to use this skill

- The user wants to know "how much would it cost to sweep 5 items off
  collection X right now" before actually placing orders.
- The user is comparing sweep cost across a few candidate collections.
- The user wants a rough total-cost-including-fees number, not just the
  bare floor price.

## How to run it

```bash
# Solana collection via Magic Eden (use the collection's Magic Eden symbol)
python3 scripts/floor_sweep.py floor degods --sweep 5

# EVM collection via CoinGecko's NFT API (use the CoinGecko nft id)
python3 scripts/floor_sweep.py evm-floor autoglyphs --sweep 3

# JSON output, custom slippage/fee assumptions
python3 scripts/floor_sweep.py floor degods --sweep 5 --slippage 4 --fee 1.5 --json
```

To find a CoinGecko NFT id, the collection's slug is usually the lowercased
name with no spaces (verify with `GET
https://api.coingecko.com/api/v3/nfts/list`). Magic Eden slugs are the
collection's symbol shown in its Magic Eden URL.

## What it does

1. Fetches the current floor price from Magic Eden (`/v2/collections/{slug}/stats`)
   or CoinGecko (`/nfts/{id}`).
2. Applies a configurable per-item slippage step (default 3%/item) to model
   walking up the order book — this is a naive approximation, not real
   depth data.
3. Adds a configurable marketplace fee percentage (defaults: 2% Magic Eden,
   2.5% blended EVM estimate).
4. Reports per-item prices, subtotal, fee amount, total cost, and average
   price per item.

## Important limitation — read this before trusting the numbers

Free public APIs (Magic Eden's public stats endpoint, CoinGecko's NFT API)
do **not** expose full live order-book depth. The per-item slippage curve
is a configurable linear approximation, not a real simulation of the actual
listings you'd fill against. Royalties are also not included in the fee
estimate. Always check the live order book on the actual marketplace before
executing a real sweep — treat this tool's output as a ballpark, not a
quote.

## Requirements

- Python 3.8+, standard library only.
- Outbound HTTPS access to `api-mainnet.magiceden.dev` and/or
  `api.coingecko.com` (both free, no key for the endpoints used here).
