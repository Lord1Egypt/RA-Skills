# Security — Sovereign Kernel Seeder

**Signature:** `Delta9Phi963-SOVEREIGN-KERNEL-SEEDER-SEC-v1`

## Guarantees

| Guarantee | How |
|-----------|-----|
| Zero external surface | Scripts use only Python stdlib; no `urllib`/`requests`/socket |
| Self-verify on insert | Pre + post hash/Merkle checks; rollback on fail |
| Consent | `--i-consent` or `LYGO_KERNEL_SEED_CONSENT` |
| No secrets | Agent contract forbids tokens/keys in eggs |
| Quarantine | Exit code 3 → do not execute modules |

## Non-goals

- Not OS malware scanning  
- Not remote attestation of other machines  
- Not a replacement for `lygo-kernel-egg-planter` Turbo/permaweb paths  

## Operator checklist

1. Install only from `deepseekoracle` ClawHub or pinned git  
2. Run `smoke_test.py` after install  
3. Keep seed roots off shared untrusted volumes when possible  
4. Treat divergent `registry_merkle_root` across machines as fork — reconcile deliberately  
