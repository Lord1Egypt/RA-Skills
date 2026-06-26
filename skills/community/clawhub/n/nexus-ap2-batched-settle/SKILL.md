---
name: nexus-ap2-batched-settle
description: "Atomically settle up to 20 AI agent payments in a single XRPL Batch transaction. Implements Google's AP2 (Agent Payments Protocol) with XLS-56 Batch on XRP Ledger — ~5 second finality, ultra-low fees, non-custodial."
version: 1.0.0
capabilities:
  - id: create-ap2-mandate
    description: "Mint an AP2 Cart or Intent payment mandate authorizing future settlement"
  - id: settle-single-mandate
    description: "Build an unsigned XRPL Payment tx to settle one verified AP2 mandate"
  - id: batch-settle-mandates
    description: "Build a single XLS-56 Batch tx that atomically settles up to 20 AP2 mandates"
  - id: verify-xrpl-payment
    description: "Verify a broadcast XRPL Payment tx by hash (validates amount, destination, memo)"
permissions:
  network: true
  filesystem: false
  shell: false
inputs:
  - name: mandate_type
    type: string
    required: true
    description: "Either 'cart' (specific items, requires total_amount+items) or 'intent' (autonomous, requires max_price+time_window)"
  - name: user_did
    type: string
    required: true
    description: "Buyer's decentralized identifier (DID or wallet identifier)"
  - name: agent_id
    type: string
    required: true
    description: "Agent identifier initiating the payment authorization"
  - name: mandate_content
    type: object
    required: true
    description: "Mandate payload — for cart: {items[], total_amount, currency}. For intent: {natural_language_intent, max_price, time_window_start, time_window_end, allowed_merchant_list}"
  - name: user_signature
    type: object
    required: true
    description: "Cryptographic signature object {algorithm, signature_value, timestamp, user_did}. Use 'sandbox_test_*' prefix for free sandbox."
outputs:
  type: object
  properties:
    mandate_id:
      type: string
      description: "Returned mandate identifier — use this in subsequent settle/batch calls"
    unsigned_tx:
      type: object
      description: "XRPL transaction JSON ready for buyer's wallet to sign + broadcast"
    instructions:
      type: string
      description: "Step-by-step settlement instructions"
requires:
  env: [NEXUS_PAYMENT_PROOF]
protocols:
  - ap2
  - xrpl
  - mpp
  - x402
  - a2a
payment:
  protocol: "ap2"
  spec: "https://ap2-protocol.org/"
  settlement_chain: "xrpl"
  settlement_time_seconds: 5
  max_batch_size: 20
  batch_mode: "ALLORNOTHING (atomic - all settle or none)"
  accepted_currencies: [XRP, RLUSD]
  supported_chains: [xrpl]
  config_endpoint: "https://ai-service-hub-15.emergent.host/api/ap2/config"
  xrpl_config: "https://ai-service-hub-15.emergent.host/api/xrpl/config"
metadata: '{"openclaw":{"emoji":"\u26a1","requires":{"env":["NEXUS_PAYMENT_PROOF"]},"primaryEnv":"NEXUS_PAYMENT_PROOF"}}'
---

# NEXUS AP2 Batched Settlement on XRPL

> Google's Agent Payments Protocol (AP2) + XRP Ledger XLS-56 Batch | ~5s finality | Up to 20 mandates per tx | Non-custodial

## When to use

Use this skill when an autonomous agent needs to:

1. **Pre-authorize payments** for AI services using AP2 mandates (Cart for specific purchases, Intent for ongoing autonomous spending within a budget)
2. **Settle many payments at once** — pay 5, 10, or 20 different AI services with one signed transaction instead of one tx per service
3. **Operate at low latency** — XRPL settles in ~5 seconds with ~$0.000005 fees, dramatically reducing M2M friction vs other chains
4. **Maintain non-custodial control** — buyer's wallet signs every tx; NEXUS never holds keys or funds

## Why batched settlement matters

Without batching: agent makes 20 API calls → 20 separate XRPL transactions → 20 separate signatures, 20× the latency, 20× the fees.

**With NEXUS AP2 + XLS-56 Batch:** agent calls 20 APIs → pre-authorizes via AP2 mandates → executes ONE signed Batch tx that atomically settles all 20. ALLORNOTHING mode guarantees no partial settlement.

## Steps

### Step 1: Create an AP2 Mandate

For an **Intent Mandate** (agent autonomy, e.g. "spend up to 10 XRP this week"):

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/ap2/mandates/create \
  -H "Content-Type: application/json" \
  -d '{
    "mandate_type": "intent",
    "user_did": "did:agent:my-agent-id",
    "agent_id": "my-agent-id",
    "merchant_id": "nexus",
    "mandate_content": {
      "natural_language_intent": "Buy AI services up to 10 XRP this week",
      "max_price": 10.0,
      "currency": "XRP",
      "time_window_start": "2026-02-26T00:00:00Z",
      "time_window_end": "2026-03-05T23:59:59Z"
    },
    "user_signature": {
      "algorithm": "ECDSA",
      "signature_value": "sandbox_test_sig_001",
      "timestamp": "2026-02-26T12:00:00Z",
      "user_did": "did:agent:my-agent-id"
    }
  }'
```

Returns `{ "mandate_id": "ap2_intent_xxx", "expires_at": "...", ... }`.

For a **Cart Mandate** (specific items, single purchase):

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/ap2/mandates/create \
  -H "Content-Type: application/json" \
  -d '{
    "mandate_type": "cart",
    "user_did": "did:agent:my-agent-id",
    "agent_id": "my-agent-id",
    "mandate_content": {
      "total_amount": 1.0,
      "currency": "XRP",
      "items": [{"sku": "llm-gateway", "name": "LLM Gateway Call", "price": 1.0, "quantity": 1}]
    },
    "user_signature": {"algorithm":"ECDSA","signature_value":"sandbox_test_sig_002","timestamp":"2026-02-26T12:00:00Z","user_did":"did:agent:my-agent-id"}
  }'
```

### Step 2a (Single Settle): Settle One Mandate

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/ap2/payments/settle \
  -H "Content-Type: application/json" \
  -d '{
    "mandate_id": "ap2_intent_xxx",
    "mandate_type": "intent",
    "verification_record_id": "",
    "amount": 2.5,
    "currency": "XRP",
    "payer_address": "r<your-xrpl-address>",
    "recipient_address": "rM86ChiqozvfHwLckKRq2yTtzKLwfBe2XA",
    "chain": "xrpl"
  }'
```

Returns `unsigned_tx` — an XRPL Payment JSON with hex-encoded `ap2.mandate.id` memo. Sign with your wallet (Xumm, Crossmark, hardware), broadcast, then confirm:

```bash
curl -X POST "https://ai-service-hub-15.emergent.host/api/ap2/payments/<mandate_id>/confirm?tx_hash=<HASH>"
```

### Step 2b (Batched Settle): Settle Up to 20 Mandates in One Tx

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/ap2/payments/batch \
  -H "Content-Type: application/json" \
  -d '{
    "mandate_ids": ["ap2_cart_001", "ap2_cart_002", "ap2_cart_003", "ap2_intent_001"],
    "payer_address": "r<your-xrpl-address>",
    "chain": "xrpl",
    "mode": "ALLORNOTHING"
  }'
```

Returns an unsigned **XLS-56 Batch** transaction containing all inner Payments. Sign + broadcast once. After broadcast:

```bash
curl -X POST "https://ai-service-hub-15.emergent.host/api/ap2/payments/batch/<batch_id>/confirm?tx_hash=<HASH>"
```

### Step 3 (Optional): Verify the broadcast

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/xrpl/verify \
  -H "Content-Type: application/json" \
  -d '{"tx_hash":"<HASH>","currency":"XRP","expected_memo":"<mandate_id>"}'
```

Returns `{ valid: true, amount_drops, amount_xrp, currency, source, destination, memos: [...] }`.

## RLUSD Support

Want to settle in regulated USD stablecoin instead of XRP? RLUSD is supported natively.

**One-time setup** — establish a trust line to Ripple's RLUSD issuer:

```bash
curl -X POST https://ai-service-hub-15.emergent.host/api/xrpl/build/trust-line \
  -H "Content-Type: application/json" \
  -d '{"holder_address":"r<your-address>","currency":"RLUSD"}'
```

Then use `"currency": "RLUSD"` in your mandates. RLUSD issuer is `rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De`.

## External Endpoints

| URL | Method | Purpose |
|-----|--------|---------|
| `/api/ap2/mandates/create` | POST | Mint a new mandate |
| `/api/ap2/mandates` | GET | List mandates (filter by agent_id) |
| `/api/ap2/payments/settle` | POST | Settle one mandate |
| `/api/ap2/payments/batch` | POST | Atomic batched settlement |
| `/api/ap2/payments/{id}/confirm` | POST | Confirm broadcast tx |
| `/api/ap2/config` | GET | AP2 discovery (chains, tokens, batch spec) |
| `/api/xrpl/config` | GET | XRPL config (network, receiving address, assets) |
| `/api/xrpl/verify` | POST | Verify any XRPL Payment tx |
| `/api/xrpl/build/escrow` | POST | EscrowCreate template (FundsLocked → ResultSubmitted) |

## Security & Privacy

- **Non-custodial.** NEXUS NEVER sees or signs with your XRPL seed. Every unsigned_tx returned must be signed locally in your wallet.
- **All requests over HTTPS/TLS** to `ai-service-hub-15.emergent.host`.
- **Mandate signatures** validated cryptographically (sandbox bypass available for testing via `sandbox_` prefix).
- **Payment proofs** verified on XRPL via Ripple public JSON-RPC nodes.

## Model Invocation Note

This skill does NOT invoke any LLM. It is pure payment orchestration infrastructure — mandates, signatures, transaction templates, and on-chain verification.

## Trust Statement

NEXUS only constructs unsigned transaction JSON and verifies on-chain payment proofs. Buyers retain full control of their wallets and funds. Mandate creation is reversible (mandates can be deleted before settlement). For production use, replace `sandbox_` signatures with real ECDSA/EdDSA signatures.

## Tags

`ap2`, `xrpl`, `agent-payments-protocol`, `batched-settlement`, `xls-56`, `non-custodial`, `rlusd`, `xrp`, `m2m-payments`, `low-latency`
