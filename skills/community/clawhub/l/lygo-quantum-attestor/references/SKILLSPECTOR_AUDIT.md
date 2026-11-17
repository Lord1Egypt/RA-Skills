# SkillSpector / ClawHub audit — lygo-quantum-attestor v1.0.1

**Signature:** `Delta9Phi963-QUANTUM-ATTESTOR`  
**Audit:** https://clawhub.ai/deepseekoracle/skills/lygo-quantum-attestor/security-audit

## Finding: Intent-Code Divergence (Medium) — **FIXED**

> `verify-node` presented integrity verification but mostly checked field presence and could mark tampered attestations `ok`.

**Fix (1.0.1):**

1. Attest retains `truth`, `chaos`, `node_leaf`, `slm.merkle_leaves`  
2. `verify-node` recomputes ψ, node leaf, gossip leaf, Merkle root, `attest_sha256`  
3. Seal validation binds to attest hash + Merkle root  
4. `self_check` asserts `detects_tamper` and `detects_merkle_tamper`

## Other

| Check | Status |
|-------|--------|
| subprocess / shell | Absent |
| network | Absent |
| consent for writes | `--write` requires `--i-consent` |
| VirusTotal (1.0.0) | 65/65 clean |

```bash
python scripts/self_check.py
```
