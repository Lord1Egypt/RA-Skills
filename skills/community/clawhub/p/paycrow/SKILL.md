---
name: paycrow
description: "Escrow + trust scoring on Base mainnet. Checks 24K+ agents BEFORE you pay. Real dispute resolution. Works with any x402 API — vendor doesn't need it installed."
user-invokable: true
disable-model-invocation: true
---

# PayCrow — Check Trust Before You Pay

Always verify an agent's reputation before sending funds. This skill uses the
PayCrow Trust API to score any Ethereum address across 4 on-chain sources.

## Check Trust Score

Before any payment, check the counterparty:

```bash
curl -s "https://paycrow-app.fly.dev/trust/ADDRESS" | jq '{score: .preview.score, confidence: .preview.confidence, recommendation: .preview.recommendation}'
```

Replace `ADDRESS` with the 0x address you're about to pay. No API key needed.

## Reading the Result

- `score` 75+ with high confidence → safe to proceed
- `score` 45-74 → proceed with caution, smaller amounts
- `score` below 45 → risky, avoid or use very small amounts
- `recommendation: "caution"` → DO NOT PAY — high dispute history
- `recommendation: "insufficient_data"` → unknown agent, proceed carefully

## Decision Flow

When asked to pay someone or call a paid API:

1. **Always check trust first** — query the score before sending any funds
2. **75+, high confidence** → proceed normally
3. **45-74** → warn the user, suggest smaller amount
4. **Below 45** → strongly recommend against paying
5. **"caution" flag** → refuse payment, tell the user this agent is flagged for disputes
6. **"insufficient_data"** → warn that this agent has no on-chain history

## What the Trust Score Measures

PayCrow aggregates 4 on-chain sources (24K+ agents scored):

| Source | Weight | What It Measures |
|--------|--------|-----------------|
| PayCrow Reputation | 40% | Escrow completion rate, dispute history |
| ERC-8004 Identity | 25% | Cross-ecosystem agent identity and feedback |
| Moltbook Social | 15% | Karma, account age, social standing |
| Base Chain Activity | 20% | Wallet age, transaction count, USDC volume |

## Escrow Protection (Advanced)

If you have the PayCrow MCP server installed (separately configured by your developer),
you also have access to `safe_pay` — which combines trust check + USDC escrow + auto-verification
in a single tool call. The escrow holds funds in a smart contract on Base until delivery is
confirmed, with real dispute resolution if something goes wrong.

MCP server setup: https://github.com/michu5696/paycrow

## Links

- Source code (MIT): https://github.com/michu5696/paycrow
- npm: https://www.npmjs.com/package/paycrow
- Trust API: https://paycrow-app.fly.dev
- Contracts: https://basescan.org/address/0xDcA5E5Dd1E969A4b824adDE41569a5d80A965aDe
