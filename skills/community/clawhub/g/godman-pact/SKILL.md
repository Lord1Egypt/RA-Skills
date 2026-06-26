---
name: godman-pact
description: "PACT — Protocol for Agent Constitutional Trust. Five-chamber agent-to-agent trust and negotiation protocol. Handles identity verification, intent analysis, constitutional negotiation, capability-locked session tokens, and audit trails."
tags: ["agent-trust", "negotiation", "constitutional", "five-chambers", "godman-protocols", "x402"]
version: "0.3.0"
---

# PACT — Protocol for Agent Constitutional Trust

*"Negotiate before you integrate."*

Use this skill when two agents from different systems need to establish trust before transacting. PACT provides a five-chamber protocol that handles the full lifecycle from first contact to secure session.

## Five Chambers

```typescript
import { pact } from '@godman-protocols/sdk';

// Chamber 1 — Public Entry Gate: rate limiting, DID resolution
// Chamber 2 — Identity Analysis: ERC-8004 verification, trust score → session ceiling
// Chamber 3 — Intent Analysis: 3-pass prompt injection scanner, coherence check
// Chamber 4 — Negotiation Room: capability declaration, payment terms, EIP-712 dual signature
// Chamber 5 — Secure Channel: capability-locked session token via HMAC(deal_hash + agent_did + expiry)
```

## Trust Score → Session Ceiling

| Score Range | Ceiling | Duration | Price Multiplier |
|---|---|---|---|
| 85-100 | FULL | 24h | 1.0x |
| 70-84 | STANDARD | 4h | 1.2x |
| 50-69 | RESTRICTED | 1h | 1.5x |
| 30-49 | MINIMAL | 15m | 2.0x |
| <30 | REJECTED | — | — |
| Unknown | PROVISIONAL | 15m | 2.5x |

## When to Use
- First contact between agents from different systems
- Establishing trust before any data exchange or payment
- Constitutional negotiation (what constraints each agent requires)
- Creating capability-locked session tokens with automatic expiry

## Notes
- SOUL constraints override PACT sessions — never use PACT to bypass safety rules
- Every PACT session produces an EAS attestation on Base (on-chain audit trail)
- Integrates with LAX for discovery and DRS for deal receipts
