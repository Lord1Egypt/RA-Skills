---
name: merchant-safety
description: |
  Decide whether a shop, seller or destination domain is safe to transact with. Combines a merchant
  trust verdict with a link-level phishing and redirect check, so an agent can vet a checkout or a
  seller before paying.

  USE FOR:
  - Checking a merchant or seller domain before an agent buys from it
  - Vetting a checkout or payment link for phishing and look-alike tricks
  - Getting a trust verdict with the evidence behind it

  TRIGGERS:
  - "merchant trust", "is this shop safe", "seller reputation"
  - "checkout safety", "is this payment link safe", "merchant safety"
  Sold as x402/MPP pay-per-call tools on Base and Solana; agents pay per successful call.
metadata:
  version: 1
---

# Merchant safety

Live prices verified 20 Nov 2026 against `https://api.glyphcall.com`.

| Task | Endpoint | Price |
|---|---|---|
| Merchant trust verdict | `https://api.glyphcall.com/merchant/trust?name=<domain>` | $0.02 |
| Full link verdict | `https://api.glyphcall.com/pack/url-safety?url=<url>` | $0.01 |

```sh
npx agentcash@latest check "https://api.glyphcall.com/merchant/trust?name=example.com"
npx agentcash@latest fetch "https://api.glyphcall.com/merchant/trust?name=example.com"
```

A missing signal is not a clean verdict. Report the fields you actually received, and treat the
answer as guidance rather than a guarantee against fraud or loss. Failed calls are not charged.

