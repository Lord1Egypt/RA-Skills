---
name: wallet-risk-triage
description: |
  Screen a wallet, token or counterparty before sending funds. Combines sanctions screening,
  a plain-language token rug verdict and portfolio context in one place, so an agent can decide
  whether to proceed.

  USE FOR:
  - Checking an address against sanctions lists before a payment
  - Getting a plain-language rug/safety verdict on an ERC-20 token
  - Seeing what a wallet holds before extending trust or credit
  - Combining several risk signals into one decision

  TRIGGERS:
  - "is this wallet safe", "sanctions check", "OFAC screen", "is this token a rug"
  - "token safety", "wallet risk", "counterparty risk", "check this address"
  Sold as x402/MPP pay-per-call tools on Base and Solana; agents pay per successful call.
metadata:
  version: 1
---

# Wallet risk triage

Live prices verified 20 Nov 2026 against `https://api.glyphcall.com` payment challenges.

| Task | Endpoint | Price |
|---|---|---|
| Sanctions screen | `https://api.glyphcall.com/sanctions/check?address=<addr>` | $0.009 |
| Token rug verdict | `https://api.glyphcall.com/token/verdict?token=<addr>` | $0.01 |
| Wallet portfolio | `https://api.glyphcall.com/wallet/portfolio?address=<addr>` | $0.005 |
| Merchant/counterparty trust | `https://api.glyphcall.com/merchant/trust?name=<domain>` | $0.02 |

Use the agentcash client so payment and retries are handled:

```sh
npx agentcash@latest check "https://api.glyphcall.com/sanctions/check?address=0x..."
npx agentcash@latest fetch "https://api.glyphcall.com/sanctions/check?address=0x..."
```

A blocked or unverifiable check is not the same as a clean verdict. Report the signals you actually
received rather than inferring safety from a missing result. Failed calls are not charged.

