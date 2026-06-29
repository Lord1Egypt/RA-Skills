---
name: gocreative-crypto
description: Crypto & DeFi market data for AI agents — spot prices, market data, DEX liquidity, DeFi protocol TVL, gas prices, Fear & Greed sentiment, trending coins, and stablecoin data. Use when an agent needs live crypto/web3 data for trading, research, or treasury decisions. Just $0.01/call in USDC via x402 — no API key, no signup.
tags: [crypto, web3, defi, prices, market-data, dex, tvl, gas, stablecoins, trading, onchain, sentiment, coingecko, defillama]
author: gocreative
version: 1.0.0
license: MIT
---

# GoCreative Crypto

> Live crypto & DeFi data for your agent — prices, DEX, TVL, gas, sentiment — **$0.01 a call**, no API key.

## When to use this
- A trading/research agent needs **live prices, market data, or DEX liquidity**.
- A DeFi agent needs **protocol TVL, gas prices, or chain data**.
- An agent wants **market sentiment** (Fear & Greed), **trending coins**, or **stablecoin** data.

## How it's paid (x402 — no key, no signup)
Plain HTTPS GET. First call returns **HTTP 402**; your OpenClaw wallet auto-pays the ~$0.01 USDC fee (Base) and retries, returning JSON.

## Tools (live endpoints — most are $0.01)
| Call | What you get |
|---|---|
| `GET https://api.gocreativeai.com/v1/crypto/price/{coin}` | Spot price + 24h change + market cap (CoinGecko id, e.g. `bitcoin`) |
| `GET https://api.gocreativeai.com/v1/crypto/market/{coin}` | Rich market data — price, market cap, rank |
| `GET https://api.gocreativeai.com/v1/crypto/dex/{token}` | Live DEX data: price, liquidity, 24h volume, FDV |
| `GET https://api.gocreativeai.com/v1/crypto/protocols/{any}` | Top DeFi protocols by TVL (chain, category, 1d/7d change) |
| `GET https://api.gocreativeai.com/v1/crypto/gas/{chain}` | Live gas (gwei) for ethereum/base/arbitrum/optimism/polygon |
| `GET https://api.gocreativeai.com/v1/crypto/fear-greed/7` | Fear & Greed Index (0-100) + 7-day history |
| `GET https://api.gocreativeai.com/v1/crypto/trending/now` | Trending coins right now |
| `GET https://api.gocreativeai.com/v1/bundle/crypto-360/{coin}` | **Crypto 360**: market data + spot + Fear&Greed fused (~$0.20) |

## Examples
- `GET /v1/crypto/price/ethereum` → spot price + 24h change.
- `GET /v1/crypto/gas/base` → current Base gas.
- `GET /v1/crypto/dex/0x...token` → DEX liquidity + volume.

## Why GoCreative
Clean, fused crypto/DeFi data (CoinGecko + DefiLlama + more) at **$0.01/call — undercutting premium on-chain data APIs that charge $0.05+** — with no API key and no signup. Bundle `crypto-360` for a one-call snapshot.

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com*
