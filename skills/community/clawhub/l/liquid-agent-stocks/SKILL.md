---
name: liquid-agent-stocks
description: Buy, hold, rebalance and sell a basket of Coinbase tokenized US stocks (NVDA, AAPL, META, GOOGL) on Base from $1 through the free Liquid Agent API. Use when a user asks to invest in stocks, buy an index or ETF on-chain, put USDC into equities, check or rebalance a stock portfolio, or cash out of stocks.
homepage: "https://api.liquidagent.ai"

metadata:
  openclaw:
    requires:
      bins: ["curl"]
---

# Liquid Agent — tokenized stock basket for agents

One HTTP API lets you open a self-custodied vault on Base that holds a band-rebalanced basket of
Coinbase's tokenized **NVDA, AAPL, META, GOOGL**, buy in from **$1 USDC**, rebalance, and sell any block.
No account, no API key, no project token, no oracle. The server never holds a key: every write
returns an **unsigned transaction** that *you* sign with your own wallet and broadcast on Base.

Base URL: `https://api.liquidagent.ai` · Chain: Base mainnet (`eip155:8453`)

## When to use this skill

- "Buy some stocks", "invest $50 in tech stocks", "get me NVDA and AAPL exposure", "buy an index / ETF on-chain"
- "How is my stock portfolio doing", "rebalance my stocks", "sell my stocks", "cash out to USDC"
- "Send my stock basket to <address>", "gift stocks to a friend's wallet"

If the user wants a single individual stock rather than the four-stock basket, say so and offer the basket anyway; the vault always holds all four at the target weights.

## What you need

- A wallet on Base that can sign transactions and EIP-712 typed data (`eth_signTypedData_v4`).
- **USDC on Base** for the purchase (min $1, 0.20% mint fee). USDC is `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`.
- **A little ETH on Base for gas — or none at all.** With no ETH, hand the unsigned tx to the gas sponsor: `POST /v1/gas {sender, calls:[tx]}` → the 402 is the exact USDC quote (from $0.03) → pay it and repeat → sign the returned `typedData` (+ EIP-7702 `authorization` the first time) → POST them back to `/v1/gas`; the sponsor submits and pays the gas. Smart-wallet SDKs can use the same URL as an ERC-7677 paymaster. See `examples/gasless.js`.
- **Otherwise: a little ETH on Base for gas.** Deposits swap precompile tokens and need an explicit gas limit of about **3,000,000**; at Base fees that is usually well under $0.05, but a wallet with zero ETH cannot buy. Check ETH first and tell the user if it is missing.
- Amounts in requests are **USDC-6 integers**: `2000000` = $2.00. Weights are basis points summing to 10000.

## The flow (run top to bottom the first time)

Always start with the free guide if anything is unclear: `GET /v1/guide`.

1. **Discover the basket** — `GET /v1/basket` → constituents with live prices, fees, `minDepositUsdc`.
2. **Quote (optional)** — `GET /v1/quote?usdc=2000000` → shares, `mintFeeUsdc`, `netUsdc`. Show this to the user before spending.
3. **Do you already have a vault?** — `GET /v1/balance/<yourAddress>`. If `vaultCount > 0`, use `vaults[0].vault` and **skip step 4**. Creating a second vault is almost never what the user wants.
4. **Create your vault (once)** — `POST /v1/create-vault` body `{}` → `{to,data,value,chainId}`. Sign, broadcast, wait for the receipt, then re-run step 3 to get the vault address.
5. **Custom weights (optional)** — `POST /v1/set-weights` body `{"vault":"0x…","weightsBps":[4000,2000,2000,2000]}` → unsigned tx. Order is NVDA, META, AAPL, GOOGL. Each weight can move at most 2000 bps per call. Default is 2500 each.
6. **Buy** — two calls, one on-chain transaction:
   - `POST /v1/buy` body `{"vault":"0x…","usdc":"2000000","permit":true,"owner":"0xYourAddress"}` → `{typedData}`.
   - Sign `typedData` off-chain with `eth_signTypedData_v4` (free, no gas).
   - `POST /v1/buy` again with `{"vault":"0x…","usdc":"2000000","permit":{"deadline":<typedData.message.deadline>,"signature":"0x…"}}` → ONE unsigned `depositWithPermit` tx. Sign and broadcast with gas limit ~3,000,000.
   - No `approve` step is needed. Omit `permit` entirely only if your wallet cannot sign typed data; then you get `{steps:[approve, deposit]}` to send in order.
7. **Check it** — `GET /v1/vault/<vault>` → `navUsdc`, current vs target `weightsBps`, `rebalanceNeeded`.
8. **Rebalance (optional)** — `POST /v1/rebalance` body `{"vault":"0x…"}` → unsigned tx. Only when `rebalanceNeeded` is true or after changing weights.
9. **Sell / cash out** — `POST /v1/redeem` body `{"vault":"0x…","shares":"<amount>","inKind":false}` → unsigned tx that burns shares and pays USDC. `inKind:true` returns the raw stock tokens instead and works even if pricing is unavailable. `shares` comes from step 3.
10. **Send / gift (optional)** — `POST /v1/send` body `{"vault":"0x…","to":"0xRecipient","shares":"<amount>"}` → unsigned tx. The recipient needs no vault and can redeem the shares themselves. Irreversible.

Every unsigned tx has the shape `{to, data, value, chainId}`. Sign it with the wallet that owns the funds and submit with `eth_sendRawTransaction` to any Base RPC (for example `https://mainnet.base.org`).

## Example: buy $5 into an existing vault

```bash
API=https://api.liquidagent.ai
ME=0xYourAddress
VAULT=$(curl -s $API/v1/balance/$ME | jq -r '.vaults[0].vault')
# 1) get the permit to sign
curl -s -X POST $API/v1/buy -H 'content-type: application/json' \
  -d "{\"vault\":\"$VAULT\",\"usdc\":\"5000000\",\"permit\":true,\"owner\":\"$ME\"}" > permit.json
# 2) sign permit.json .typedData with eth_signTypedData_v4 -> SIG, read DEADLINE from .typedData.message.deadline
# 3) get the single deposit tx
curl -s -X POST $API/v1/buy -H 'content-type: application/json' \
  -d "{\"vault\":\"$VAULT\",\"usdc\":\"5000000\",\"permit\":{\"deadline\":$DEADLINE,\"signature\":\"$SIG\"}}"
# -> {to,data,value,chainId}: sign + broadcast with gas limit 3000000
```

## Optional paid extras (x402, USDC on Base)

These return HTTP 402 with an x402 v2 challenge. If your runtime can pay x402 (agentcash, an x402 fetch wrapper, or the OpenClaw x402 skill), just retry with payment. Everything above stays free.

- `GET /v1/signals` — **$0.04**. The whole basket's rebalancing signal in one call: per-stock returns, volatility, RSI, trend, relative strength, correlation, and an inverse-volatility `suggestedWeightsBps` you can pass straight to `/v1/set-weights`. Add `?vault=<yours>` for your drift.
- `POST /v1/publish` body `{"vault":"0x…","label":"Alice's stocks"}` — **$0.25** flat. Mints a live shareable portfolio page at `https://api.liquidagent.ai/v/<slug>` for 24 hours; the user opens `viewUrl` with no wallet or login. Re-publish to keep it alive.

## Rules

- Never send a private key or seed phrase anywhere. This API never asks for one; it only returns data for you to sign locally.
- Confirm the USD amount with the user before broadcasting a buy, and report the tx hash after.
- Reuse the vault from `/v1/balance`. Create a new one only if `vaultCount` is 0.
- Wait for each transaction receipt before the next step (create → balance → buy).
- Redeem and send are final once mined.
- Signals are aggregated data, not investment advice; say so if you relay them.

More: `https://api.liquidagent.ai/v1/guide` (plain-English), `https://api.liquidagent.ai/openapi.json` (full spec), `https://api.liquidagent.ai/llms.txt`.
