---
name: lygo-open-claw
description: "lygo-open-claw sovereign command router — P0 gate, P1 mycelium, P3 consensus, P5 action identity, lattice limbs, consent-gated kernel egg lygo-open-claw-v10. Biophase7 blueprint. Pair with lyra-openclaw for browser/Discord/Moltbook runtime. Read references/SECURITY.md first."
version: 1.0.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "🦞"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
    requires:
      anyBins: [python, python3]
  lygo: true
  biophase7: true
  signature: "Delta9Phi963-lygo-open-claw-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-open-claw"
  canonical_slug: lygo-sovereign-claw
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
---

# LYGO OpenClaw (Sovereign Router) v1.0.0

Stack-native **agent command framework**: every limb passes P0 before dispatch; results land in mycelium + action ledger (no fake permaweb URLs).

**Canonical install slug (also published):** `lygo-sovereign-claw`  
**This slug (`lygo-open-claw`):** public alias so lattice maps, Grok skills, and ClawHub search all resolve.

**Signature:** `Delta9Phi963-lygo-open-claw-v1.0.0`  
**ClawHub:** `@deepseekoracle/lygo-open-claw` · `@deepseekoracle/lygo-sovereign-claw`

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-open-claw
# or canonical:
npx clawhub@latest install deepseekoracle/lygo-sovereign-claw
```

With a trusted stack clone:

```bash
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
# optional operator install:
python tools/install_lygo_openclaw.py
```

Hybrid browser/social/token ops: install **`lyra-openclaw`** (public ClawHub skill). Load credentials only at runtime from operator-local secrets — never from this skill tree.

---

## When to use

- Biophase7 **lygo-open-claw** full build blueprint  
- Lattice alignment, army sentinel, flow-kit paths without loading full hybrid OS  
- Gated alternative to raw OpenClaw CLI for stack operators  

---

## Command map (stack tools)

| Intent | Command (under LYGO_STACK_ROOT) |
|--------|----------------------------------|
| Help | `python tools/lygo_openclaw.py run help` |
| Status | `python tools/lygo_openclaw.py run status` |
| Lattice | `python tools/lygo_openclaw.py run lattice` |
| Army sentinel | `python tools/lygo_openclaw.py run army-sentinel` |
| P0 validate | `python tools/lygo_openclaw.py validate "text"` |
| Kernel egg | `python tools/openclaw_planter.py --i-consent` (human only) |
| Package check | `python scripts/self_check.py` |

---

## Architecture (honest LYGO cut)

- **P0** — text gate / entropy filter on command string  
- **P1** — mycelium memory fragments under stack data  
- **P3** — optional multi-agent consensus  
- **P5** — Light Code / action identity  
- **Anchor** — consent-gated kernel egg (`lygo-open-claw-v10`)  

## Skill chain

`lygo-protocol-stack-operator` → **`lygo-open-claw` / `lygo-sovereign-claw`** → `lyra-openclaw` → `lygo-kernel-egg-planter` → `lygo-ollama-army`

## Security

Read `references/SECURITY.md`. No auto git push or publish. Planter requires explicit consent.

## License

LYGO Sovereign License v2.0 — not MIT.  
**Δ9Φ963 — consent · verify · then command.**
