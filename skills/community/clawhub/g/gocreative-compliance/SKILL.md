---
name: gocreative-compliance
description: Sanctions screening, KYB, KYC, AML, OFAC & PEP watchlist checks for AI agents — plus a one-shot PASS/WARN/BLOCK compliance verdict and a 0-100 entity risk score. Screen any company or person against sanctions and watchlists before onboarding, paying, or transacting. Real OFAC SDN / GLEIF / CFPB data, pay-per-call in USDC via x402 — no API key, no signup.
tags: [compliance, kyb, kyc, aml, sanctions, ofac, pep, watchlist, due-diligence, risk-score, screening, onboarding, vendor]
author: gocreative
version: 1.0.0
license: MIT
---

# GoCreative Compliance

> Screen any company or person for sanctions, PEP, and risk — before your agent onboards, pays, or transacts. One install, no API key, pay-per-call in USDC.

## When to use this
- An agent is **onboarding a customer/business** and must run KYB/KYC.
- An agent is about to **pay or contract a vendor** and needs due diligence.
- An agent is **screening a counterparty/wallet/name** against sanctions before a transaction.
- Any "is this entity legit / safe / sanctioned?" decision.

## How it's paid (x402 — no key, no signup)
Every tool is a plain HTTPS GET. The first call returns **HTTP 402** with a price; your OpenClaw wallet auto-pays the small USDC fee (on Base) and the request retries, returning JSON. Nothing to configure.

## Tools (live endpoints)

| Call | What you get | Price |
|---|---|---|
| `GET https://api.gocreativeai.com/v1/compliance/verdict/{target}` | **One PASS / WARN / BLOCK** decision, fusing sanctions + PEP + risk. Best first call. | ~$0.15 |
| `GET https://api.gocreativeai.com/v1/data/sanctions-screen/{name}` | Matches across **OFAC, EU, UK, UN** sanctions + **PEP** + watchlists | ~$0.15 |
| `GET https://api.gocreativeai.com/v1/bundle/kyb-360/{company}` | **Full KYB**: sanctions/PEP/watchlist + 0-100 risk + business registry | ~$0.45 |
| `GET https://api.gocreativeai.com/v1/risk/entity-score/{company}` | Fused **0-100 risk score** (OFAC + CFPB + legal-entity) | ~$0.05 |
| `GET https://api.gocreativeai.com/v1/risk/vendor/{company}` | Vendor dossier: **GLEIF** legal entity + OFAC + CFPB complaints | ~$0.05 |

`{target}`/`{company}` = a domain (e.g. `stripe.com`) or legal name; `{name}` = a person or entity name (URL-encode spaces).

## Examples
- Gate onboarding: `GET /v1/compliance/verdict/acme-corp.com` → `{"verdict":"PASS", ...}` → proceed only on PASS.
- Screen a person before payout: `GET /v1/data/sanctions-screen/vladimir%20putin` → returns sanction matches → BLOCK.
- Vet a new supplier: `GET /v1/bundle/kyb-360/supplier-domain.com` → full KYB report.

## Recommended flow
1. Start with **`compliance_verdict`** for a fast PASS/WARN/BLOCK.
2. On WARN/BLOCK (or when you need detail), pull **`sanctions-screen`** and **`kyb-360`**.
3. For ongoing monitoring, re-run periodically — entities change status.

## Why GoCreative
- **The only native KYB/sanctions toolkit on x402** — agents elsewhere have no clean compliance option.
- **Real regulatory sources**: OFAC SDN, GLEIF, CFPB — not scraped guesses.
- **Cheaper than legacy KYB APIs** (~$2/company) with **zero signup** and per-call billing.

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com · contact@gocreativeai.com*
