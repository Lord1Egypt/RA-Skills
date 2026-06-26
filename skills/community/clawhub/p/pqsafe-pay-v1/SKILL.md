---
name: pqsafe-pay-v1
description: Post-quantum signed SpendEnvelopes for AI agent payments. ML-DSA-65 (NIST FIPS 204) signatures over Airwallex, Wise, Stripe, USDC-Base, and x402 rails.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - PQSAFE_API_KEY
      bins:
        - node
    primaryEnv: PQSAFE_API_KEY
    envVars:
      - name: PQSAFE_API_KEY
        required: true
        description: PQSafe AgentPay API key from dashboard.pqsafe.xyz
      - name: PQSAFE_KEY_ID
        required: false
        description: ML-DSA-65 signing key ID (defaults to account default key)
      - name: PQSAFE_TEST_MODE
        required: false
        description: Set to "true" to use in-memory mocks for local development
    emoji: "🔐"
    homepage: https://pqsafe.xyz/openclaw-skill
    os: ["macos", "linux", "windows"]
    install:
      - kind: npm
        package: "@pqsafe/openclaw"
---

# PQSafe Post-Quantum Payment Skill (`pqsafe.pay.v1`)

Post-quantum signed SpendEnvelopes for AI agent payments. ML-DSA-65 (NIST FIPS 204) signatures
over Airwallex, Wise, Stripe, USDC-Base, and x402 rails.

## Quick Start

```bash
npm install @pqsafe/openclaw
```

```typescript
import { OpenClawClient } from "@openclaw/sdk";
import "@pqsafe/openclaw"; // registers pqsafe.pay.v1

const claw = new OpenClawClient();

const envelope = await claw.invoke("pqsafe.pay.v1/create_envelope", {
  agentId:   "agent_my_bot_v1",
  payerId:   "payer_usr_abc123",
  maxAmount: "100.00",
  currency:  "USD",
  rail:      "wise",
  expiresAt: "2026-12-31T23:59:59Z",
});
```

Set `PQSAFE_TEST_MODE=true` for local development — no real keys or network calls required.

## Operations

| Operation | Description |
|-----------|-------------|
| `create_envelope` | Issue a new ML-DSA-65 signed SpendEnvelope with spend cap, rail, and expiry |
| `verify_envelope` | Verify signature integrity, expiry, nonce uniqueness, and key ID validity |
| `revoke_envelope` | Append envelope ID to the real-time revocation list (append-only, timestamped) |

## Security Model

- **HSM-backed signing keys** — ML-DSA-65 private keys are generated and stored in hardware
  security modules; they never leave the PQSafe key service
- **Single-use nonce** — each envelope carries a 256-bit random nonce; replay attacks are
  rejected at the verify layer
- **Expiry enforced in signed payload** — `expiresAt` is part of the signed content; an attacker
  cannot extend expiry without invalidating the signature
- **Real-time revocation list** — `revoke_envelope` appends to a low-latency revocation list
  checked on every `verify_envelope` call
- **Append-only audit log** — all create, verify, and revoke events are timestamped and written
  to an immutable audit log
- **JCS-canonical signing** — payload serialized in JSON Canonicalization Scheme form (RFC 8785)
  before signing, eliminating signature ambiguity from key ordering or whitespace variation

## Supported Rails

| Rail | Status | Currency |
|------|--------|----------|
| `airwallex` | **LIVE sandbox** | Multi-currency (real test transfers) |
| `wise` | **LIVE sandbox** | 40+ fiat currencies (real test transfers) |
| `stripe` | mock-ready | USD + 135 others |
| `usdc-base` | mock-ready | USDC |
| `x402` | mock-ready | USDC + ETH |

LIVE sandbox = validated end-to-end with sandbox rails. Mock-ready = SpendEnvelope creation and
verification are fully functional; live rail integration is in progress.

## ML-DSA-65 Parameters

| Parameter | Value |
|-----------|-------|
| Standard | NIST FIPS 204 |
| Security level | NIST Level 3 |
| Public key size | 1,952 bytes |
| Secret key size | 4,032 bytes |
| Signature size | 3,309 bytes |
| Hardness assumption | Module-LWE + Module-SIS |

## Links

- Homepage: https://pqsafe.xyz/openclaw-skill
- npm package: https://www.npmjs.com/package/@pqsafe/openclaw
- API docs: https://docs.pqsafe.xyz/agent-pay/openclaw
- AP2-PQ Profile RFC: https://pqsafe.xyz/ap2-pq-rfc
- NIST FIPS 204: https://csrc.nist.gov/pubs/fips/204/final
- Source (Apache-2.0): https://github.com/PQSafe/pqsafe/tree/main/plugins/openclaw-pqsafe

## License

Apache-2.0 — Security disclosures: security@pqsafe.xyz
