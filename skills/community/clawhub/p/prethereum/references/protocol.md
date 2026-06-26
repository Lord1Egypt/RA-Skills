# Prethereum Wire Format - prethereum/1

## Proof Structure

A prethereum proof is self-contained JSON:

| Field | Type | Description |
|-------|------|-------------|
| `version` | `"prethereum/1"` | Wire format version |
| `artifact.hashAlg` | `"sha256"` | Hash algorithm |
| `artifact.digestB64` | string | Base64-encoded SHA-256 digest of committed bytes |
| `commit.nonceB64` | string | Base64-encoded 32-byte random nonce |
| `commit.counter` | string | Monotonic counter value |
| `commit.time` | number | Unix timestamp (ms) |
| `signer.publicKeyB64` | string | Base64-encoded Ed25519 public key (32 bytes) |
| `signer.signatureB64` | string | Base64-encoded Ed25519 signature (64 bytes) |
| `environment.enforcement` | string | `"nitro"` for TEE, `"stub"` for development |
| `environment.measurement` | string | Enclave measurement or stub identifier |

## Signed Body

The signature covers a canonical JSON serialization of:

```json
{
  "artifact": { "hashAlg": "sha256", "digestB64": "..." },
  "commit": { "nonceB64": "...", "counter": "...", "time": ... },
  "enforcement": "...",
  "measurement": "...",
  "publicKeyB64": "...",
  "version": "prethereum/1"
}
```

Keys are sorted alphabetically. No whitespace.

## Verification Steps

1. Compute SHA-256 digest of the original bytes
2. Compare against `artifact.digestB64` in the proof
3. Reconstruct the signed body from proof fields
4. Canonicalize (sorted keys, no whitespace)
5. Verify Ed25519 signature over the canonical bytes using `signer.publicKeyB64`
6. Optionally validate `environment` attestation (for TEE-backed proofs)

## Environment Types

- **Stub** (`enforcement: "stub"`) - development/testing, no hardware attestation
- **Nitro** (`enforcement: "nitro"`) - AWS Nitro Enclave with attestation document

## Fail-Closed Design

If any step in proof generation fails (hashing, signing, counter increment, environment measurement), no proof is returned. Partial proofs are never emitted.
