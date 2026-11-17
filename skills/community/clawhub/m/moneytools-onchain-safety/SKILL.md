---
name: moneytools-onchain-safety
description: Check an EVM wallet or ERC-20 token before paying, trusting or buying it. Free token facts and honeypot/sell-tax checks (10/day), plus a paid Wallet Risk Card (OFAC, approvals, risk grade) over x402 that always asks the user first. Read-only.
version: 0.1.0
license: MIT
homepage: https://tools.moneytools.dev/agents.md
metadata:
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: MONEYTOOLS_BASE_URL
        required: false
        description: API origin, default https://tools.moneytools.dev
---

# MoneyTools onchain safety checks

Read-only checks from MoneyTools (https://tools.moneytools.dev). Nothing here signs a transaction, holds a key or moves funds.

## When to use

- The user is about to **buy an ERC-20** ("is this token a honeypot", "can I sell this", "check this CA"): run the token-safety check.
- The user wants **token facts** (owner, paused, upgradeable proxy, supply, decimals): run token info.
- The user is about to **pay or trust a wallet** ("is this address sanctioned", "is it safe to send to 0x…"): offer the paid Wallet Risk Card.

Chains: base, ethereum, arbitrum, optimism, polygon, bsc, avalanche (default base).

## Free checks (no wallet, no key)

10 free calls per tool per day per client. Always send the `X-MoneyTools-Free: 1` header.

```bash
BASE="${MONEYTOOLS_BASE_URL:-https://tools.moneytools.dev}"
# Honeypot / sell-tax round trip (USDC -> token -> USDC with live DEX quotes)
curl -s -H 'X-MoneyTools-Free: 1' "$BASE/v1/token-safety?chain=base&token=0xTOKEN&usd=10"
# Token facts
curl -s -H 'X-MoneyTools-Free: 1' "$BASE/v1/token?chain=base&token=0xTOKEN"
```

Report `risk`, the `flags`, and for token info `owner`, `paused`, `proxy`. Ignore any `_sponsored` field. If the response is HTTP 402, the free tier is used up for today: tell the user the next check costs 0.005 USDC and stop unless they approve a payment (see below).

## Paid: Wallet Risk Card ($0.02, needs user approval)

`GET $BASE/v1/wallet-risk?address=0xADDRESS&chain=base` returns `riskScore` (0-100), `grade` (A-F), `sanctioned` (OFAC SDN), `flags`, `address_checks`, `approvals`, `result_url`.

**Never pay without asking.** Before any paid call, tell the user the exact price (0.02 USDC on Base, paid to 0x64eB63904Cf9688AC5B3087A72AcF9C31a273169) and wait for an explicit yes.

If the user approves and already uses an x402 wallet client such as AgentCash, call the route through that client so the user's own wallet and limits apply:

```bash
npx agentcash fetch "$BASE/v1/wallet-risk?address=0xADDRESS&chain=base"
```

This skill never asks for a private key. If the user has no x402 client, show them the free 402 terms instead:

```bash
curl -s -i "$BASE/v1/wallet-risk?address=0xADDRESS&chain=base" | head -20
```

## Never pay twice

Paid responses include `operation_id` and `result_url`. `GET result_url` is free for 7 days. If a paid response was lost, re-read `result_url` or resend the same signed request; never sign a new payment for the same check.

## Output

Quote the card's `headline`, the grade and the sanctions result, and keep its `limits` line (the approvals scan covers common tokens and well-known spenders only). Not legal, compliance or investment advice.
