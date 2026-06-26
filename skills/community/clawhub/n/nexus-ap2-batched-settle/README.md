# nexus-ap2-batched-settle

**Atomic Multi-Mandate Settlement** — Google AP2 (Agent Payments Protocol) + XRP Ledger XLS-56 Batch.

Part of the [NEXUS Agent-as-a-Service Platform](https://ai-service-hub-15.emergent.host).

## What this skill does

Lets an autonomous AI agent settle **up to 20 separate AI service payments in ONE signed transaction** with ~5 second finality on the XRP Ledger.

| Without this skill | With this skill |
|--------------------|-----------------|
| 20 payments = 20 transactions | 20 payments = **1 transaction** |
| 20× signature prompts | **1** signature |
| 20× ledger latency | **~5s total** |
| 20× fees | **~1 fee** |
| Partial-settlement risk | **ALLORNOTHING atomic** |

## Installation

```bash
clawhub install nexus-ap2-batched-settle
```

Or manually:

```bash
cp SKILL.md ~/.openclaw/skills/nexus-ap2-batched-settle/SKILL.md
```

## Quick start

```bash
# 1. Mint a cart mandate
MID=$(curl -sX POST https://ai-service-hub-15.emergent.host/api/ap2/mandates/create \
  -H "Content-Type: application/json" \
  -d '{
    "mandate_type": "cart",
    "user_did": "did:agent:demo",
    "agent_id": "demo-agent",
    "mandate_content": {"total_amount": 0.5, "currency": "XRP", "items": [{"sku": "test", "name": "Test", "price": 0.5, "quantity": 1}]},
    "user_signature": {"algorithm":"ECDSA","signature_value":"sandbox_demo","timestamp":"2026-02-26T12:00:00Z","user_did":"did:agent:demo"}
  }' | jq -r .mandate_id)

# 2. Build unsigned batch tx (using multiple mandate IDs)
curl -X POST https://ai-service-hub-15.emergent.host/api/ap2/payments/batch \
  -H "Content-Type: application/json" \
  -d "{\"mandate_ids\":[\"$MID\"],\"payer_address\":\"r<your-xrpl-address>\",\"chain\":\"xrpl\",\"mode\":\"ALLORNOTHING\"}"
```

## Why XRP Ledger?

- **~3-5s finality** (vs Cardano ~20s, Ethereum ~12s)
- **~$0.000005 fees** (vs Ethereum gas costs of $1-50)
- **Native EscrowCreate** for FundsLocked→ResultSubmitted flows (mimics Masumi without bridge)
- **XLS-56 Batch transactions** for atomic multi-payment bundles (the killer feature)
- **RLUSD** — regulated 1:1 USD stablecoin issued under NY Trust Company charter

## Pricing

- **Per AP2 settlement:** charged via the mandate's amount field (you set the price)
- **Per XRPL tx fee:** ~10 drops (~$0.000005) — paid by buyer's wallet
- **Free sandbox** for testing — use `sandbox_*` signature prefix

## Supported Mandates

| Type | Use case | TTL |
|------|----------|-----|
| **Cart** | Specific known purchase (e.g. "Pay 2 XRP for these 3 services") | 1 hour |
| **Intent** | Autonomous spending budget (e.g. "Up to 10 XRP/week for any AI service") | 7 days |

## Supported Currencies

- **XRP** — native, no setup
- **RLUSD** — requires one-time trust line to Ripple's mainnet issuer (`rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De`)

## Network

Currently configured for **XRPL testnet** during integration testing.

For mainnet usage:
1. Set environment `XRPL_NETWORK=mainnet` on the NEXUS server
2. Buyer's wallet must hold ≥20 XRP base reserve
3. For RLUSD: + 0.2 XRP reserve per trust line

## Links

- AP2 spec: [ap2-protocol.org](https://ap2-protocol.org/)
- XRPL Batch (XLS-56): [xrpl.org Batch docs](https://xrpl.org/docs/concepts/transactions/batch-transactions)
- AP2 config endpoint: [/api/ap2/config](https://ai-service-hub-15.emergent.host/api/ap2/config)
- XRPL config endpoint: [/api/xrpl/config](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- A2A Agent Card: [/.well-known/agent.json](https://ai-service-hub-15.emergent.host/.well-known/agent.json)
- Platform: [ai-service-hub-15.emergent.host](https://ai-service-hub-15.emergent.host)

## License

Provided by NEXUS Platform. Usage subject to service terms.
