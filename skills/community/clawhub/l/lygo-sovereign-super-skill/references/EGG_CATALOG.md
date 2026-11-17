# Egg catalog (static reference)

## Catalog (`EGG_SPECS` in `tools/kernel_egg_catalog.py`)

- `p0-nano-kernel`
- `stack-anchor-hook`
- `stack-orchestrator-slim`
- `lattice-soa-index`
- `firmware-p04-drivers`
- `protocol-drivers-p2-p5`
- `joy-loop-protocol-v21`
- `lygo-second-brain-v10`
- `lygo-sandcastle-v10`
- `lygo-openclaw-v10`
- `lygo-lpis-v10`
- `lygo-ops-detector-v1`
- `lygo-context-guard-v1` — token budget / redact / compact utility
- `lygo-skill-gate-v1` — local pre-install skill risk scanner
- music lattice eggs (`excavationpro-music-*`) when catalog includes them

## Planters (refresh product manifests + rebuild catalog eggs)

| Tool | Product egg |
|------|-------------|
| `tools/joy_loop_planter.py` | `joy-loop-protocol-v21` |
| `tools/second_brain_planter.py` | `lygo-second-brain-v10` |
| `tools/workflow_orchestrator_planter.py` | `lygo-sandcastle-v10` |
| `tools/openclaw_planter.py` | `lygo-openclaw-v10` |
| `tools/lpis_planter.py` | `lygo-lpis-v10` |

## Champions

`tools/champion_egg_planter.py --i-consent` — 15 council eggs; verify with `tools/verify_champion_eggs.py`.