# Security — lygo-quantum-attestor v1.0.1

**Audit page:** https://clawhub.ai/deepseekoracle/skills/lygo-quantum-attestor/security-audit

## Permissions

| Capability | Default |
|------------|---------|
| Network | **None** |
| Subprocess / shell | **None** |
| Filesystem write | Only `--write` with `--i-consent` |
| Publish | **None** |

## ClawHub finding — FIXED (1.0.1)

| Finding | Severity | Fix |
|---------|----------|-----|
| Intent-Code Divergence: `verify-node` only structural | Medium | Cryptographic recompute of `attest_sha256`, `node_leaf`, gossip leaf, Merkle root; seal binding checks; retain verification inputs on attest |

## Epistemic limits

- Software P6 attestation ≠ TPM / hardware root of trust  
- Local Merkle gossip leaf ≠ live SLM network consensus  
- Non-collapsing receipt is a **policy invariant**, not a physics claim  

## Operator rules

- Do not store secrets in `--truth` / `--chaos` / `--anchor-file`  
- Prefer Continuum capsules for consequential claims  
- Human remains the publisher  

## Proof

```bash
python scripts/self_check.py
# ok · verify_node · detects_tamper · detects_merkle_tamper
```
