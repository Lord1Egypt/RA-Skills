---
name: merso-integration
description: >
  Integrate Merso PNPL (Play Now, Pay Later) payments into games or digital goods platforms.
  Use when a user wants to: (1) add Merso installment payments to a game or app,
  (2) understand how Merso works technically or commercially,
  (3) set up the Merso API, webhooks, or payment flow,
  (4) troubleshoot an existing Merso integration.
  Covers API endpoints, full integration flow, Node.js configuration, webhook handling, DB schema, and real-world case studies.
  Requires MERSO_GAME_ID and MERSO_API_KEY env vars (provided by Merso). MERSO_ENV sets the target environment (production or development).
metadata: {"clawdbot":{"requires":{"env":["MERSO_GAME_ID","MERSO_API_KEY","MERSO_ENV"]}}}
---

# Merso Integration Skill

Merso is a PNPL (Play Now, Pay Later) platform for digital goods for games like NFTs, web2 in-game assets and virtual currency packs. It is not a credit product. It issues software licenses that grant immediate access; the license expires automatically if installment payments stop. Zero KYC, zero underwriting, zero credit risk for the merchant.

## Key references

- **Full API + integration guide:** See `references/api.md`
- **Commercial context, case studies, and pitch info:** See `references/commercial.md`

## When to load references

- Load `references/api.md` for any technical integration task (endpoints, webhooks, DB schema, Node.js config, flow)
- Load `references/commercial.md` for pitch preparation, case studies, GMV metrics, or partner context

## Integration checklist

1. Set env vars: `MERSO_ENV`, `MERSO_GAME_ID`, `MERSO_API_KEY`
2. Authenticate → cache Bearer token (auto-renew 30 min before expiry)
3. Implement `POST /merso-buy-item` with a **unique `itemId` per purchase**
4. Register webhook URL via `POST /set-webhook-url`
5. Handle webhook events idempotently (check payment status before crediting)
6. Add fallback: `GET /verify-payment-intent/:id` if webhook doesn't arrive
7. Apply Node.js TLS config (SNI) when connecting through Cloudflare — see `references/api.md`

## Minimum item price: $5
