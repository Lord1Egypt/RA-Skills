# nft-floor-sweep-calculator

Estimates the total cost of sweeping N items off an NFT collection's floor,
using live floor prices from Magic Eden (Solana) or CoinGecko's free NFT
API (EVM), plus marketplace fees and a naive slippage curve.

## Why

Floor price alone doesn't tell you what a bulk buy actually costs — you pay
more as you eat through cheaper listings, plus marketplace fees. This gives
a quick ballpark before you go check the real order book.

## Usage

```bash
# Solana collection (Magic Eden symbol)
python3 scripts/floor_sweep.py floor degods --sweep 5

# EVM collection (CoinGecko NFT id)
python3 scripts/floor_sweep.py evm-floor autoglyphs --sweep 3

# Custom slippage-per-item and fee percentage
python3 scripts/floor_sweep.py floor degods --sweep 10 --slippage 5 --fee 1.5

# JSON output
python3 scripts/floor_sweep.py floor degods --json
```

## Requirements

- Python 3.8+, standard library only (`urllib`, `json`, `argparse`).
- Outbound HTTPS access to `api-mainnet.magiceden.dev` and/or
  `api.coingecko.com`.

## Notes

This is a cost estimator only — it does not place orders, does not hold or
require a wallet key, and does not have access to real order-book depth
(free tier APIs don't expose it). Always verify against the live book
before buying. See `SKILL.md` for the full limitation notes.
