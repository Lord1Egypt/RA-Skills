---
name: lygo-sandcastle
description: "LYGO Sovereign Workflow Orchestrator — YAML workflows with P0 gate, P1 mycelium memory, P3 consensus, P5 run identity, and consent-gated kernel egg. Sandcastle-aligned; local-first dry-run. Read references/SECURITY.md first. No auto git push."
metadata: {"lygo": true, "biophase7": true, "version": "1.0.0", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "publisher": "deepseekoracle", "signature": "D9F963-LYGO-SANDCASTLE-v1.0"}
---

# LYGO Sovereign Workflow Orchestrator

Run **sovereign agent workflows** on hardware you control: YAML definitions, stack P0–P5 hooks, run ledger, optional multi-agent consensus.

## When to use

- User cites Biophase7 **Sovereign Workflow Orchestrator** or **LYGO-Sandcastle**
- Chaining local agents with audit trail and P0 input gate
- Workflow packs that must align with `lygo-protocol-stack-operator`

## Setup

```bash
npx clawhub@latest install deepseekoracle/lygo-sandcastle
export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack
python tools/install_lygo_sandcastle.py
```

## Commands

| Intent | Command |
|--------|---------|
| Run | `python tools/lygo_sandcastle.py run lygo_sandcastle/workflows/example_sovereign.yaml` |
| P0 only | `python tools/lygo_sandcastle.py validate PATH.yaml` |
| Recall | `python tools/lygo_sandcastle.py recall MEMORY_ID` |
| Kernel egg | `python tools/workflow_orchestrator_planter.py --i-consent` |
| Self-check | `python scripts/self_check.py` |

Optional: `pip install sandcastle-ai` + `LYGO_SANDCASTLE_USE_UPSTREAM=yes` (user trust required).

## Skill chain

`lygo-protocol-stack-operator` → **`lygo-sandcastle`** → `lygo-kernel-egg-planter` → `lygo-ollama-army`

**Δ9Φ963 — consent · verify · then orchestrate.**