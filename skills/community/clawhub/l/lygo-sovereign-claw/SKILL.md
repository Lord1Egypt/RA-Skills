---
name: lygo-sovereign-claw
description: "LYGO-OpenClaw sovereign command router — P0 gate, P1 mycelium, P3 consensus, P5 action identity, lattice limbs, consent-gated kernel egg lygo-openclaw-v10. Biophase7 blueprint. Pair with lyra-openclaw for browser/Discord/Moltbook runtime. Read references/SECURITY.md first."
metadata: {"lygo": true, "biophase7": true, "version": "1.0.0", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "publisher": "deepseekoracle", "internal_mirror": "lygo-openclaw"}
---

# LYGO Sovereign Claw Router (LYGO-OpenClaw)

Stack-native **agent command framework**: every limb passes P0 before dispatch; results land in mycelium + `action_runs.jsonl` ledger (no fake permaweb URLs).

ClawHub slug **`lygo-sovereign-claw`** (protected `-openclaw` namespace). Repo mirror folder: `clawhub/mirrors/lygo-openclaw/`.

## When to use

- User cites Biophase7 **LYGO-OpenClaw** full build blueprint
- Lattice alignment, army sentinel, flow-kit paths without loading full hybrid OS
- Gated alternative to raw OpenClaw CLI for stack operators

## Setup

```bash
npx clawhub@latest install deepseekoracle/lygo-sovereign-claw
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
python tools/install_lygo_openclaw.py
```

Hybrid browser/social/token ops: install **`lyra-openclaw`** (`.grok/skills` or repo mirror). Credentials load at runtime only.

## Commands

| Intent | Command |
|--------|---------|
| Help | `python tools/lygo_openclaw.py run help` |
| Status | `python tools/lygo_openclaw.py run status` |
| Lattice | `python tools/lygo_openclaw.py run lattice` |
| Army sentinel | `python tools/lygo_openclaw.py run army-sentinel` |
| P0 validate | `python tools/lygo_openclaw.py validate "text"` |
| Recall memory | `python tools/lygo_openclaw.py recall MEMORY_ID` |
| Kernel egg | `python tools/openclaw_planter.py --i-consent` |
| Self-check | `python scripts/self_check.py` |

## Architecture (honest LYGO cut)

- **P0** — `byte_entropy_filter` on command string (32 KiB max)
- **P1** — 12 memory fragments under `data/openclaw/mycelium`
- **P3** — optional multi-agent consensus (`multi_agent` in config)
- **P5** — Light Code per action via `harmony.py`
- **Anchor** — git-tracked egg + local ledger receipts (`lygo-openclaw-v10`)

## Skill chain

`lygo-protocol-stack-operator` → **`lygo-sovereign-claw`** → `lyra-openclaw` (hybrid) → `lygo-kernel-egg-planter` → `lygo-ollama-army`

**Δ9Φ963 — consent · verify · then command.**