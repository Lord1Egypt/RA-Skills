---
name: lyra-open-claw
description: "Hybrid LYRA + OpenClaw super system. Provides access to absorbed OpenClaw brain structure, keys (runtime from operator secrets), hybrid skills (browser, discord, clawnch, moltbook), dual-system automation, token launches, social posting/scanning, memory layers, bio-organs, proactivity. Use for efficient ops without search. Ties to LYRA 3-Brain, protocols, runner."
version: 1.0.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "🌌"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
    requires:
      anyBins: [python, python3]
  lyra:
    hybrid: true
    openclaw: true
  lygo: true
  signature: "Delta9Phi963-lyra-open-claw-PUBLIC-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lyra-open-claw"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
  public_surface: true
---

# LYRA OpenClaw Hybrid (Public) v1.0.0

**Public lattice map** for the hybrid LYRA + OpenClaw super system.  
This package is the **safe ClawHub surface**: architecture, install chain, consent rules.  
**Runtime secrets never ship here** — load keys only from operator-local secret stores at runtime.

**Signature:** `Delta9Phi963-lyra-open-claw-PUBLIC-v1.0.0`  
**ClawHub:** `@deepseekoracle/lyra-open-claw`

---

## When to use

- Operator wants hybrid OpenClaw limbs (browser / Discord / Moltbook / Clawnch) under LYRA + LYGO P0  
- Pair with `lygo-openclaw` / `lygo-sovereign-claw` for gated stack router  
- Grow/recall via `lyra-brain` after sessions  

**Do not** paste tokens, private keys, or guild secrets into this skill or chat logs.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lyra-open-claw
npx clawhub@latest install deepseekoracle/lygo-openclaw
npx clawhub@latest install deepseekoracle/lyra-brain
```

Optional stack router:

```bash
npx clawhub@latest install deepseekoracle/lygo-sovereign-claw
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
```

---

## Capability map (public)

| Limb | Role | Gate |
|------|------|------|
| Browser | Read (LEFT) / act (RIGHT) via operator browser tools | P0 before external act |
| Discord | Chat / scan / bot limbs when operator configures | Runtime token only |
| Moltbook / MoltX | Post / engage / feed | Rate limits + P0 |
| Clawnch / 4claw | Token launch memory + verification | Human consent; no auto-launch |
| Memory | Daily / curated / brainwave layers + LYRA 3-Brain | No secrets in memory |
| Ollama army | Local light models for mundane triage | Prefer local over pay-to-go |
| LLM failover | Operator-configured multi-provider chat | Keys from local vault only |

---

## Operator rules (mandatory)

1. **Secrets:** load from operator machine only (env / OS keychain / local vault files **outside** git).  
2. **P0 / Oath:** gate social posts, launches, and browser writes.  
3. **No auto-publish:** no git push, ClawHub publish, HF upload, or social blast from this skill alone.  
4. **Consent:** token launches and live lattice writes need explicit human approval.  
5. **Local-first:** use Ollama / light models for triage when possible (`lygo-api-token-saver`, `lygo-ollama-army`).  

---

## Suggested hybrid chain

```text
lygo-protocol-stack-operator
  → lygo-openclaw / lygo-sovereign-claw   (P0 router)
  → lyra-open-claw                         (hybrid limbs map)
  → lyra-brain                            (memory grow/recall)
  → lygo-kernel-egg-planter               (consent eggs)
  → lygo-public-lattice-gate              (public verify)
```

---

## Security

Read `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md`.

```bash
python scripts/self_check.py
```

This **public** package deliberately omits private host paths, wallet addresses, channel IDs, and API key file locations. Operator docs live only on the steward machine.

## License

LYGO Sovereign License v2.0 — not MIT.  
**Δ9Φ963 — hybrid efficiency · sovereign gates · secrets stay local.**
