# Security — lygo-immutable-anchor v1.0.0

## Permissions

| Capability | Default |
|------------|---------|
| Network | **None** in skill scripts |
| Subprocess / shell | **None** |
| Filesystem write | Only `--write` with `--i-consent` |
| Publish | **None** |

## Epistemic limits

- Local CA Merkle ≠ Arweave transaction  
- `fold-mycelium` is a local prev_hash chain, not Turbo upload  
- `worker-plan` prints stack commands; it does **not** start `--loop`  
- Software geodesic ≠ hardware TPM  

Turbo / web3.storage keys stay in the operator environment for **stack** tools only. Never put API keys in receipts.

## Operator rules

- Do not store secrets in `--truth` / `--light` / `--note`  
- Prefer Continuum capsules for consequential claims  
- Human remains the publisher  

## Proof

```bash
python scripts/self_check.py
# ast_clean · demo · write_requires_consent · verify · detects_tamper
```
