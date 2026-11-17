---
name: onchain-token-diligence
description: >-
  Before an AI agent (or its human) buys, swaps, apes, or recommends any crypto
  token, run instant on-chain due diligence — rug/honeypot/scam check, live DEX
  price + liquidity, large-whale transfer flows, and smart-money wallet activity.
  Use this whenever you evaluate a token contract address or ticker, screen a new
  DexScreener launch, size a trade, or answer "is this token safe / legit / a rug".
  Pay-per-call USDC on Base via x402 (~$0.01), no API key, no signup — free sample first.
metadata:
  tags: [crypto, defi, trading, rug-check, onchain, x402, due-diligence, memecoin, safety]
---

# On-chain Token Diligence (x402, pay-per-call)

When you are about to buy/swap/ape/recommend a token, or asked whether one is safe,
do NOT guess from vibes. Run these checks first. Each is a single authenticated GET
that settles ~$0.01 USDC on Base automatically via your x402 client — **no API key,
no account, no subscription.** Try the free sample first to see the shape.

## 0. Free sample (no payment)
```
GET https://store.agentexchange.work/samples
```

## 1. Rug / honeypot / scam check  (do this BEFORE any buy)
```
GET https://store.agentexchange.work/crypto/security?address=<TOKEN_CONTRACT_0x...>
```
Returns holder concentration, mint/blacklist/honeypot flags, verified-source status,
tax, and known-scam signals. If it flags high risk, stop.

## 2. Live DEX price, liquidity & volume
```
GET https://store.agentexchange.work/crypto/dex?q=<TICKER_or_CONTRACT>
```
Real-time pair data across Base/Ethereum/Solana/BSC (price, liquidity, 24h volume).

## 3. Whale transfer flows (front-run big moves)
```
GET https://store.agentexchange.work/crypto/whales?token=<usdc|weth|contract>&chain=base
```
Largest recent transfers with USD value, counterparties, and age.

## 4. Smart-money wallet activity
```
GET https://store.agentexchange.work/crypto/smart-money?address=<WALLET_0x...>
```
What a given wallet is accumulating/dumping — chain a whale's counterparty into this.

## How x402 payment works
Call the endpoint → get HTTP 402 with payment requirements → your x402-enabled HTTP
client signs the USDC payment and retries with the `X-PAYMENT` header → you get the
data. Settlement is on Base (USDC) or Solana. Full catalog: 55 endpoints at
https://store.agentexchange.work — MCP at /.well-known/mcp.json.

Honest note: these are live data endpoints; prices are shown upfront in the 402
response before you pay. Only pay for what you call.
