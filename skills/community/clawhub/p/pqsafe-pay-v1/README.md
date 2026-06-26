# @pqsafe/openclaw

**OpenClaw skill plugin for PQSafe AgentPay**

Algorithm: ML-DSA-65 (NIST FIPS 204)  
Security level: NIST Level 3 (quantum-resistant)  
AP2-PQ profile: https://pqsafe.xyz/ap2-pq-rfc  
npm: `@pqsafe/openclaw`

---

## Why post-quantum payment signing matters for AI agents

AI agents are increasingly authorized to spend real money — booking travel, paying invoices, settling supplier bills, consuming API credits. The cryptographic keys that authorize those payments are high-value targets.

**The threat:** Shor's algorithm running on a large-scale fault-tolerant quantum computer will break RSA and all elliptic-curve cryptography (ECDSA, Ed25519) in polynomial time. Current estimates for "cryptographically relevant" quantum computers: **2030–2035**. Nation-state adversaries are already executing "harvest now, decrypt later" attacks — intercepting classical-signed payment authorizations today to decrypt when quantum hardware matures.

**The solution:** ML-DSA-65 (Module Lattice Digital Signature Algorithm, NIST Level 3) has no known quantum speedup beyond Grover's algorithm, which provides only a square-root reduction — completely insufficient to break 65-bit post-quantum security parameters. NIST finalized ML-DSA in FIPS 204 (August 2024).

---

## What this plugin does

`@pqsafe/openclaw` is an [OpenClaw](https://docs.openclaw.ai) skill plugin that wraps the **PQSafe AgentPay AP2-PQ profile**. It enables any OpenClaw-compatible AI agent to:

1. **`create_envelope`** — build and ML-DSA-65 sign a `SpendEnvelope` authorizing an agent to spend up to a configured limit on a specified payment rail
2. **`verify_envelope`** — verify signature validity and temporal bounds (fully local, no network)
3. **`revoke_envelope`** — submit a revocation to the PQSafe registry, preventing the envelope from being used

---

## Quick start

```bash
npm install @pqsafe/openclaw @pqsafe/agent-pay
```

```typescript
import { createPQSafeOpenClawSkill } from '@pqsafe/openclaw'

const pqsafe = createPQSafeOpenClawSkill()

// Register with your OpenClaw agent
agent.registerSkill(pqsafe)

// Create a SpendEnvelope (signing is done locally — secret key never leaves your env)
const envelope = await pqsafe.invoke('create_envelope', {
  issuer: 'pq1a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b',
  agent: 'my-travel-agent-v1',
  maxAmount: 10,
  currency: 'USDC',
  allowedRecipients: ['0xdeadbeef...'],
  ttlSeconds: 300,
  rail: 'x402',
  dsaSecretKey: process.env.PQSAFE_DSA_SECRET_KEY, // 4032 bytes, hex-encoded
  dsaPublicKey: process.env.PQSAFE_DSA_PUBLIC_KEY,  // 1952 bytes, hex-encoded
})

// Pass the SignedEnvelope to executeAgentPayment
import { executeAgentPayment } from '@pqsafe/agent-pay'
const result = await executeAgentPayment(envelope, {
  recipient: '0xdeadbeef...',
  amount: 9.50,
  memo: 'API access token',
})
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PQSAFE_DSA_SECRET_KEY` | Yes (prod) | Hex-encoded ML-DSA-65 secret key (4032 B = 8064 hex chars) |
| `PQSAFE_DSA_PUBLIC_KEY` | Yes (prod) | Hex-encoded ML-DSA-65 public key (1952 B = 3904 hex chars) |
| `PQSAFE_TEST_MODE` | No | Set to `true` to use mock mode — no real keys or network calls |

For local development without ML-DSA keys:

```bash
export PQSAFE_TEST_MODE=true
```

---

## SpendEnvelope structure

```typescript
// What gets signed (deterministic JCS JSON, RFC 8785):
interface SpendEnvelope {
  version: 1
  issuer: string           // pq1 + 20-byte keccak hex of ML-DSA-65 pubkey
  agent: string            // calling agent identifier
  maxAmount: number        // maximum spend (positive)
  currency: string         // ISO 4217 or crypto ticker
  allowedRecipients: string[] // rail-specific recipient allowlist
  validFrom: number        // Unix timestamp (seconds)
  validUntil: number       // Unix timestamp (seconds)
  nonce: string            // 32 hex chars (128-bit CSPRNG)
  rail?: Rail              // optional rail constraint
}

// The SignedEnvelope wraps the above:
interface SignedEnvelope {
  envelopeJson: string     // canonical JSON bytes that were signed
  signature: string        // ML-DSA-65 signature, hex-encoded
  dsaPublicKey: string     // issuer public key, hex-encoded
}
```

---

## Security model

### Local signing
ML-DSA-65 signing is done entirely in your process using `@noble/post-quantum`. Your secret key never leaves your environment and is never sent to any PQSafe server.

### Envelope lifecycle

```
create_envelope → [agent presents to processor] → consumed (single-use nonce)
      ↓
revoke_envelope (any time before consumption — immediate, irreversible)
```

### Recipient allowlist
The `allowedRecipients` field is included in the signed payload. An agent can only pay recipients explicitly listed in the envelope — even if the agent is compromised, it cannot redirect payments to unapproved destinations.

### Expiry enforcement
`validUntil` is included in the signed payload. AP2-PQ-compatible processors verify both the ML-DSA-65 signature and `validUntil > now` before executing any payment. Envelopes cannot be extended after creation.

### Nonce replay protection
Each envelope contains a 128-bit CSPRNG nonce. The PQSafe nonce registry (checked via `executeAgentPayment`) rejects any verification attempt for a previously-consumed nonce.

---

## Rail support

| Rail | Description | Sandbox Status |
|------|-------------|----------------|
| `airwallex` | Airwallex multi-currency transfers | **LIVE sandbox** |
| `wise` | Wise international transfers | **LIVE sandbox** |
| `stripe` | Stripe payment processing | Mock-ready |
| `usdc-base` | USDC on Base L2 | Mock-ready |
| `x402` | HTTP 402 micropayment standard | Mock-ready |

Live sandbox rails (Airwallex, Wise) support real test-mode transactions with sandbox credentials. Mock-ready rails execute against local stubs — full sandbox integration is in progress.

---

## API reference

### `createPQSafeOpenClawSkill(config?)`

Factory function. Returns an `OpenClawSkillHandler` with `skillId = "pqsafe.pay.v1"`.

```typescript
const skill = createPQSafeOpenClawSkill({
  apiUrl: 'https://api.pqsafe.xyz/v1', // default
  timeoutMs: 30000,                     // default (used for revoke_envelope only)
})
```

### `create_envelope` operation

| Input field | Type | Required | Description |
|------------|------|----------|-------------|
| `issuer` | string | yes | PQSafe address (`pq1` + 20-byte keccak hex) |
| `agent` | string | yes | Agent identifier (1–128 chars) |
| `maxAmount` | number | yes | Max spend, positive |
| `currency` | string | yes | ISO 4217 or crypto ticker |
| `allowedRecipients` | string[] | yes | At least one recipient |
| `ttlSeconds` | integer | no | 30–86400 (default: 3600) |
| `startsInSeconds` | integer | no | Delay before envelope activates (default: 0) |
| `rail` | Rail | no | Constrain to specific rail |
| `dsaSecretKey` | string | prod | Hex ML-DSA-65 secret key (8064 hex chars) |
| `dsaPublicKey` | string | prod | Hex ML-DSA-65 public key (3904 hex chars) |

Returns: `{ envelopeJson, signature, dsaPublicKey }`

### `verify_envelope` operation

| Input field | Type | Required | Description |
|------------|------|----------|-------------|
| `envelope` | SignedEnvelope | yes | Full signed envelope to verify |
| `dsaPublicKey` | string | no | Override public key for verification |

Returns: `{ valid, agent, issuer, validUntil, reason? }`

Failure reasons: `SIGNATURE_INVALID` · `ENVELOPE_EXPIRED` · `ENVELOPE_NOT_YET_ACTIVE` · `MALFORMED_ENVELOPE`

### `revoke_envelope` operation

| Input field | Type | Required | Description |
|------------|------|----------|-------------|
| `envelope` | SignedEnvelope | yes | Full signed envelope to revoke |
| `reason` | string | no | Reason for revocation (max 256 chars) |

Returns: `{ revoked, revokedAt, httpStatus }`

Note: This operation requires network access to the PQSafe API (`PQSAFE_TEST_MODE` bypasses the call).

---

## ML-DSA-65 key parameters

| Parameter | Value |
|-----------|-------|
| Algorithm | ML-DSA-65 (NIST FIPS 204, formerly Dilithium3) |
| Security level | NIST Level 3 |
| Hardness problem | Module-LWE + Module-SIS |
| Public key size | **1952 bytes** (3904 hex chars) |
| Secret key size | **4032 bytes** (8064 hex chars) |
| Signature size | **3309 bytes** (6618 hex chars) |
| Serialization | JCS canonical JSON (RFC 8785) → bytes |

---

## Links

- PQSafe website: https://pqsafe.xyz
- AP2-PQ RFC: https://pqsafe.xyz/ap2-pq-rfc
- npm package: https://www.npmjs.com/package/@pqsafe/openclaw
- API docs: https://docs.pqsafe.xyz/agent-pay/openclaw
- NIST FIPS 204: https://doi.org/10.6028/NIST.FIPS.204
- @noble/post-quantum (underlying ML-DSA implementation): https://github.com/paulmillr/noble-post-quantum

---

## License

Apache-2.0 — see [LICENSE](../../LICENSE)

Security disclosures: security@pqsafe.xyz
