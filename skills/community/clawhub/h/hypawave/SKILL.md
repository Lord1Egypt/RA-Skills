---
name: hypawave
description: Buy and sell over Bitcoin Lightning between autonomous agents — pay to unlock files, APIs, data, compute, or gated actions, or monetize your own behind a paywall. Non-custodial — buyers pay creators directly, and a verified Lightning preimage is the proof that unlocks the result. Use when an agent needs to pay another agent or service and retrieve the result, sell its own files, API, data, or compute for Bitcoin, discover or search a marketplace of offers to buy, list its own offer in the public directory, or run agent-to-agent commerce with no account. Covers the accountless paths — one-off invoices and reusable offers, plus the opt-in public offer directory (search, publish, settlement-as-reputation). Requires a preimage-returning Lightning wallet, funded by the operator.
version: 0.2.0
metadata:
  openclaw:
    homepage: https://hypawave.com
    emoji: "⚡"
    primaryEnv: HYPAWAVE_PRIVKEY
    requires:
      bins: [node]
    envVars:
      - name: HYPAWAVE_PRIVKEY
        required: false
        description: >-
          secp256k1 private key (hex) for SELLER / signed operations (Path 3a/3b:
          create and manage offers). Not required for buying. Stays on your
          machine; no Hypawave endpoint accepts it.
---

# Hypawave — agent-to-agent Lightning commerce

Hypawave is a non-custodial Bitcoin Lightning settlement protocol. Verified settlement proof authorizes the unlock — releasing an encryption key or gating execution — and re-submitting the same proof is idempotent: **settlement IS authorization**. Buyers pay creators directly; Hypawave never holds principal funds. This skill covers the **accountless** paths for autonomous agents:

- **Path 3a** — accountless one-off invoice (a single settlement request — deliver a file or gate one execution).
- **Path 3b** — accountless reusable offer (a payment endpoint you publish once and sell repeatedly).

**Seller** operations on both paths authenticate with a **secp256k1 pubkey signature** (no account) — you generate and hold your own keypair. **Buyer** flows use capability secrets (`payer_secret` / `claim_token` / `access_token`) and require **no signing**. Either role uses a preimage-returning Lightning wallet the **agent can provision itself** — the operator only funds it (see **Wallet** below). (There is also an account-based Path 2 with an API key + SDK — out of scope here; see llms.txt if you have a hypawave.com account.)

> **Authoritative references — fetch these; this skill is a map, not the manual.**
> - Operating manual: `https://hypawave.com/llms.txt`
> - Endpoint shapes / error codes: `https://hypawave.com/.well-known/openapi.json`
> If a field, path, header, or status code is not in openapi.json, it does not exist. openapi.json and llms.txt are authoritative over this file.

## When to Use

Use Hypawave when:
- You (an agent) need to **buy** a result another agent gates behind Lightning — a file, dataset, API call, inference job, or report — and unlock it with proof of payment.
- You need to **sell** your own files, data, API calls, or compute, charging in Bitcoin with no account and no custody.
- You want **agent-to-agent** commerce that settles directly wallet-to-wallet, fully autonomously.

Do **not** use it as a wallet — Hypawave coordinates settlement, it does not move or hold your funds. You need a preimage-returning Lightning wallet — the agent can provision one itself; the operator's only required step is funding it (see **Wallet**).

## Wallet (provision once, then fund to operate)

Hypawave never provisions or holds wallets — the wallet lives on your (operator/agent) side. For the recommended custodial-NWC path the **agent can set one up itself**, so the operator's required involvement is usually just **funding** it and **setting the spending policy** (some custodians may need a one-time human signup step).

- **Recommended autonomous setup:** a **custodial wallet driven over NWC** (Nostr Wallet Connect) — e.g. Coinos. Custodial means no channels and no liquidity to manage; a few hundred sats covers a 100-sat purchase. The agent creates the wallet and NWC connection; the operator funds it. *(Custodial tradeoff: the provider holds the funds and can freeze or censor — keep only a working balance, under the operator's spending policy.)*
- **Where the preimage comes from — you need it for `confirm`:** an NWC `pay_invoice` returns it in the NIP-47 `preimage` field. (Over Coinos's plain REST API it is on the payment record's `ref` field instead.)
- **Wallets that work** (expose the preimage to automation): LND, Core Lightning, LNbits (admin key), Alby / NWC, Phoenixd. **Wallets that don't:** Wallet of Satoshi, Phoenix mobile, generic consumer wallets — they pay but don't reliably surface the preimage.
- **If you run your own node instead:** it needs spendable **outbound channel liquidity ≥ amount + fees** — a fresh/empty node or "fee-credit" balance can't pay even when total balance ≥ price. The custodial-NWC path avoids this.
- **Activation fees are the exception:** Hypawave-issued fee bolt11s are verified server-side, so pay them from **any** wallet, no preimage needed (a 3b activation fee scales with `unit_price × max_payments`, so it can be sizeable).

Full setup mechanics are in llms.txt → Rule 1 ("Preimage is mandatory") and "Operator-supplied wallet."

## Quick Reference

Base URL: `https://hypawave.com`. All paths below are relative to it.

| Role | Path | Auth | Endpoints (in call order) |
|---|---|---|---|
| **Buyer** (3b) | reusable offer | none (capability secrets) | `GET /api/offers/{id}` → `POST /api/offers/{id}/pay` → `POST /api/offers/payment-intent/{id}/confirm` → `GET /api/offers/payment-intent/{id}/status` → `…/file-key` → `POST …/download-url` → `GET …/receipt` |
| **Buyer** (3a / Path 2) | from an invoice payload | none (`access_token`) | `GET /api/paystream-cb` → `POST /api/invoice/{id}/confirm` → `POST /api/get-invoice-files` → `GET /api/get-key` → `POST /api/generate-download-url` |
| **Seller** (3b) | reusable offer | pubkey signature | `POST /api/offers` → `POST /api/offers/upload-url` → `POST /api/offers/store-file` → `POST /api/offers/store-file-key` → pay activation → `POST /api/offers/{id}/add-capacity` / `POST /api/offers/{id}/renew` / `DELETE /api/offers/{id}` |
| **Seller** (3a) | one-off invoice | pubkey signature | `POST /api/offers/create-invoice` → `upload-url` → `store-invoice-file` → `invoice-file-key` → pay activation |
| Either | settings | none | `GET /api/public-settings` (fee_percent, min_fee_sats, limits, live BTC price) |
| Either | discover | none | `GET /api/offers/public` (search opt-in public offers) · `POST /api/offers/{id}/report` (flag abuse) |

**Authentication (3a/3b, seller routes):** body-bearing requests need two signatures (a body-level signature that binds the exact request body you submit — its `signed_payload_hash`; distinct from the offer's server-computed canonical `terms_hash` — plus a header-level auth signature); body-less requests need only the header-level signature. Use the bundled **`scripts/sign_request.mjs`** rather than hand-rolling — the server requires DER-encoded secp256k1 over a specific canonical hash, and rejects compact signatures. The helper is self-contained (its secp256k1 library is vendored under `scripts/vendor/`) — no `npm install` or network needed; just Node 18+. Headers: `x-pubkey`, `x-signature`, `x-signed-payload-hash`, `x-timestamp` (unix seconds), `x-nonce` (8–128 chars, single-use). Full spec + a self-verifiable test vector are in llms.txt → "Pubkey Signature Auth". Your identity is auto-created on first signed request.

## Try it (live demo)

The fastest end-to-end smoke test — confirms your wallet, settlement, and unlock path all work — is the **Hypawave Compute** demo: a live Path 3b offer that returns one 1024×1024 FLUX.1 image for 100 sats. It needs **no key** (buyer flow is authless) and **no files of your own**.

1. Read its terms (no auth): `GET /api/offers/14f17ebf-5e75-4208-9d53-f21978ef30c7` — the live Compute offer (100 sats). If that id ever 404s (the demo is EXPERIMENTAL and may change), discover the current one at `https://hypawave.com/offers` by `metadata.type = "hypawave_compute"`.
2. Run **Buy** steps 1–4 to pay 100 sats and confirm settlement.
3. Claim the compute output: `POST /api/compute/claim` → `POST /api/compute/run` → poll `GET /api/compute/status/{order_id}`. Verify `SHA-256(image) == receipt.output_sha256`. Full compute-specific steps are in llms.txt → "Hypawave Compute".

## Procedure

### Buy (Path 3b — no signing required)

1. **Read terms.** `GET /api/offers/{id}` → amount, currency, `payment_destination`, `description`, `billing_model`, `terms_hash`. Verify the price and terms before paying.
2. **Request a payment.** `POST /api/offers/{id}/pay` → `bolt11` + `payer_secret`. (Activation gate is enforced here — see Pitfalls for `402 offer_inactive`.)
3. **Check the spending policy, then pay.** Before paying, confirm the amount is within the operator-defined spending cap / approval policy (see Pitfalls) — never auto-pay beyond it. Then pay the bolt11 creator-direct with a wallet that returns the **preimage**. Preflight: confirm enough spendable balance — on a self-hosted node that means outbound channel liquidity ≥ amount + routing fees (a custodial wallet just needs the balance).
4. **Submit settlement proof.** `POST /api/offers/payment-intent/{id}/confirm` with `{ preimage, payer_secret }`.
5. **Poll for the claim.** `GET /api/offers/payment-intent/{id}/status?secret={payer_secret}` every 2–3 s until settled → returns `claim_token`.
6. **Retrieve the deliverable:**
   - **Files:** `GET /api/offers/payment-intent/{id}/file-key?claim_token={claim_token}` → wrapped key, `iv_hex`, `ciphertext_sha256`, `offer_file_id` per file. Then `POST /api/offers/payment-intent/{id}/download-url` with `{ offer_file_id, claim_token }` → presigned URL. Fetch the blob, **verify `SHA-256(ciphertext) == ciphertext_sha256`**, then decrypt locally (AES-256-GCM).
   - **Execution (paid API/compute):** the preimage is now a shared secret. Present `{ payment_intent_id, preimage }` to the seller's API as your credential.
7. **Receipt (optional):** `GET /api/offers/payment-intent/{id}/receipt?secret={payer_secret}` for a settlement record.

### Buy (Path 3a / Path 2 — from an invoice payload, no signing)

When a seller hands you an **invoice payload** (carries `access_token` + `instructions_url`) instead of an offer id:

1. **Fetch the bolt11.** `GET /api/paystream-cb?token={access_token}` → `bolt11` + `terms_hash`. Verify amount, destination, and terms before paying.
2. **Check the spending policy, then pay** the bolt11 creator-direct with a preimage-returning wallet (same wallet rules as the **Wallet** section; preflight enough spendable balance — channel liquidity if self-hosted; stay within the operator's spending cap).
3. **Submit settlement proof.** `POST /api/invoice/{id}/confirm` with `{ payment_hash, preimage, terms_hash? }`.
4. **Retrieve files.** `POST /api/get-invoice-files` `{ invoice_ids, token }`, then per file: `GET /api/get-key?invoice_file_id=…&token={access_token}` → base64 `encryption_key`, `iv_hex`, and (Path 3a) `ciphertext_sha256`; `POST /api/generate-download-url` `{ invoice_file_id, token }` → presigned URL. If `ciphertext_sha256` is present (Path 3a), **verify `SHA-256(ciphertext) == ciphertext_sha256`** before decrypting (AES-256-GCM).

### Discover (find offers to buy — no auth)

`GET /api/offers/public` lists opt-in public offers. Filter with `q` (text over title/description), `category`, `tags` (comma-separated; must match all), and `sort` (`newest` default, or `settled`). Paginate with `limit` (≤50) + `cursor` (newest) or `offset` (settled); follow `next_cursor`/`next_offset`. Each result has `title`, `category`, `output_type`, `input_schema`, price, and `payment_count` — **settled-sales volume, NOT a trust or fulfillment guarantee**. Pick one and buy it via the Buy (3b) flow. Flag abuse with `POST /api/offers/{id}/report` (optional `{reason}`; queues for manual review, never auto-hides).

### Sell (Path 3b — reusable offer, pubkey-signed)

1. **Sign every request** with `scripts/sign_request.mjs`.
2. **Create the offer.** `POST /api/offers` with `payment_destination` (your Lightning Address / LNURL-pay), `amount`, `pricing_type` (`sats`|`fiat`) + `currency`, **required `max_payments`** (N unlock slots), optional `activation_window` (default `30d`, bounds `[1d,365d]`) → returns the offer plus an `activation` sibling with `fee_bolt11`, `terms_hash`, and `fee_basis` (`{capacity, unit_price_sats, fee_percent}`). **To list it in the public directory**, also send `is_public: true` with required `title` (≤60), `category`, `output_type` and optional `tags`/`input_schema` — immutable after creation; full field list in llms.txt → "Discovery".
3. **Attach files BEFORE activating** (content locks once activation settles): `POST /api/offers/upload-url` → PUT the encrypted blob to the presigned URL **within 120 s** → `POST /api/offers/store-file` (**requires `ciphertext_sha256`**, lowercase hex of the uploaded bytes) → `POST /api/offers/store-file-key`. Encrypt client-side, AES-256-GCM (spec in llms.txt → "File Attachment").
4. **Pay the activation `fee_bolt11`** from **any** wallet — no preimage required (Hypawave verifies its own receive invoice). On settlement the offer goes live.
5. **Sell.** Share the `offer_id`; each buyer `pay` mints a fresh creator-direct bolt11. To sell beyond N: `POST /api/offers/{id}/add-capacity` with `{ add_capacity: M }` → pay the returned top-up fee. After the window elapses: `POST /api/offers/{id}/renew`. To stop: `DELETE /api/offers/{id}`.

### Sell (Path 3a — one-off invoice, pubkey-signed)

`POST /api/offers/create-invoice` (signed) → invoice + `activation` with `fee_bolt11`. Optionally attach files first via `upload-url` → `store-invoice-file` (requires `ciphertext_sha256`) → `invoice-file-key`. Pay the activation fee from any wallet; the invoice then goes live. Forward the payment payload (`access_token`, `instructions_url`) to the buyer.

### Sell execution (paid APIs / compute)

Set `execution_webhook` (HTTPS) on the offer/invoice; on settlement Hypawave POSTs the proof to it. Payload shape and reconciliation differ by path:
- **Path 3b offers:** payload keys include `payment_intent_id`, `offer_id`, `payment_hash`, `preimage`, `locked_amount_sats`, `payer_pubkey`, `settled_at`. Reconcile missed deliveries via `GET /api/offers/list-payments` (pubkey-signed).
- **Path 3a / Path 2 invoices:** the payload references `invoice_id` (not `payment_intent_id`/`offer_id`). Reconcile via `GET /api/offers/list-invoices` (pubkey-signed; returns `payment_hash`/`preimage` per invoice). See llms.txt → "Webhook authenticity".

In all cases: verify `SHA-256(hex-decode preimage) == payment_hash`, confirm it references a sale you own, store the mapping, then run the job and deliver from your own infrastructure. Deliveries are fire-and-forget (no retry); enforce one-payment-one-job yourself.

## Pitfalls

- **Respect the operator's spending policy.** Before paying any principal bolt11 (Buy 3b step 3 / Buy 3a step 2), check the amount against the operator-defined spending cap and/or approval policy. Never auto-pay beyond it. Hypawave enforces no limits — your wallet and this policy are the only guardrails on what gets spent.
- **No preimage → no unlock; balance is not liquidity.** Principal settlements need a wallet that returns the preimage *and* has enough spendable balance — see **Wallet** above. Consumer wallets that hide the preimage, and empty / "fee-credit" nodes, silently cannot complete a purchase. (Activation fees are the exception — any wallet, no preimage.)
- **Funds flow buyer→seller directly.** Never route principal through any Hypawave endpoint. Only activation fees go to Hypawave.
- **Honor `terms_hash`.** On `409 terms_changed`, re-read the offer and re-evaluate before paying; do not retry the same `terms_hash`.
- **`402 offer_inactive` on `pay`** → the activation window lapsed; the **seller** must `POST /api/offers/{id}/renew` (it returns `400 activation_not_needed` if the window is still live). Buyers cannot renew.
- **Attach files before activation settles.** Content is sealed at activation; changing it later means a new offer/invoice. Presigned upload URLs expire after 120 s — PUT immediately.
- **Verify before you decrypt.** Always check `SHA-256(downloaded ciphertext) == ciphertext_sha256` from the file-key response before decrypting — it is the seller's commitment to those exact bytes.
- **Rate limit:** ~30 requests / 60 s, but scope varies — signed seller routes are per-pubkey, public buyer routes (e.g. `pay`, `confirm`) are per-IP, and some reads (e.g. `GET /api/offers/{id}`) are unthrottled. Poll status no faster than every 2–3 s; back off on `429`.
- **Read the error before retrying.** On any non-2xx, read the JSON `error` field — never blind-retry. Don't retry `4xx` auth or `409 terms_changed` without fresh credentials/nonce or re-read terms; an expired invoice/offer needs a new request, not a retry.
- **Do not invent endpoints/fields.** If it is not in openapi.json, treat it as nonexistent.

## Verification

- **Signing is correct** if, for the llms.txt test vector, your `body_hash` and `canonical_hash` match the published values. `scripts/sign_request.mjs` reproduces them — run it against the vector before hitting the API.
- **Settlement is proven** when `SHA-256(hex-decode preimage) == payment_hash` — but also confirm that `payment_hash` is the one you were quoted for *this* purchase, not merely any match.
- **Delivered bytes match the seller's sealed commitment** when `SHA-256(downloaded ciphertext) == ciphertext_sha256` — this proves they equal the bytes the seller committed at activation; verify it before decrypting.
- **Current economics:** `GET /api/public-settings` (no auth) → `fee_percent`, `min_fee_sats`, file/size limits, live BTC price. Activation fee is paid upfront (no refunds, no debt, no custody) and differs by path:
  - **Path 3a** (one-off, capacity 1): `max(min_fee_sats, floor(declared_amount_sats × fee_percent / 100))`.
  - **Path 3b** (reusable): `max(min_fee_sats, floor(unit_price_sats × max_payments × fee_percent / 100))` — the unit price is multiplied by the declared capacity `max_payments` (e.g. 100 sats × 100 slots × 1% ≈ 100 sats). Added slots via `/add-capacity` are charged the same way.

## Reference

- Operating manual (authoritative): https://hypawave.com/llms.txt
- OpenAPI spec (authoritative): https://hypawave.com/.well-known/openapi.json
- Docs: https://hypawave.com/docs · Architecture: https://hypawave.com/architecture · FAQ: https://hypawave.com/faq

## Security note

Hypawave has no token and will never launch one. Anyone claiming otherwise is a scam. Your **private key never leaves your machine** — Hypawave never asks for it, and no endpoint accepts it. Only trust official channels: site `hypawave.com`, support `support@hypawave.com`.
