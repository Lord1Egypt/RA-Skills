# Cross-system: Planter ↔ Sovereign Seeder

**Planter skill:** `lygo-kernel-egg-planter`  
**Seeder skill:** `lygo-sovereign-kernel-seeder`  
**Unified doc:** `docs/KERNEL_EGG_SYSTEM_UNIFIED.md` in lygo-protocol-stack  

## Roles

| | Planter (classic) | Seeder (sovereign) |
|--|-------------------|---------------------|
| Storage | `data/kernel_eggs/` | `data/sovereign_seeds/` |
| Verify | `tools/verify_kernel_eggs.py` / `scripts/verify_eggs.py` | `scripts/verify_seed.py` |
| Network | Optional Turbo / pages / clawhub pins | **None** (zero external surface) |
| Best for | P0, champions, stack protocol eggs | Policy pins, skill pins, offline modules |

## Agent order

```text
1) python tools/verify_all_kernel_layers.py --json
2) If classic QUARANTINE → stop (do not retrieve classic eggs)
3) If sovereign QUARANTINE → stop (do not load sovereign modules)
4) Plant (planter) or seed (seeder) only with consent
5) Re-run unified verify
```

## Do not merge storage formats

Classic transport blobs (zlib/json `.bin` style) and sovereign `.egg.json` are **different schemas**.  
Cross-reference registries; do not overwrite one with the other.

## Install both

```bash
clawdhub install lygo-kernel-egg-planter
clawdhub install lygo-sovereign-kernel-seeder
```

ClawHub paths use `/skills/`:

- https://clawhub.ai/deepseekoracle/skills/lygo-kernel-egg-planter  
- https://clawhub.ai/deepseekoracle/skills/lygo-sovereign-kernel-seeder  
