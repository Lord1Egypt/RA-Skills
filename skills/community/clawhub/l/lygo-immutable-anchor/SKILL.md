---
name: lygo-immutable-anchor
description: "LYGO Immutable Anchor (Biophase7) — local CA seals geodesic paths; optional stack Turbo folds mycelium; SLM/P7 worker is planned not spawned. Truth×Light receipts. Local-first, consent-gated. No network, no subprocess, no auto-publish. Use for Biophase7 immutable anchor, local CA, Arweave Turbo plan, geodesic seal, mycelium fold, autonomy worker. Pairs with geodesic-sealer + quantum-attestor + protocol-stack-operator."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "⚓"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/ANCHOR_DEPLOYMENT.md"
    requires:
      anyBins: [python, python3]
  lygo: true
  lattice: true
  biophase7: true
  immutable_anchor: true
  signature: "Delta9Phi963-IMMUTABLE-ANCHOR-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/lygo-immutable-anchor"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
  proposed_by: "@grok"
  blueprint_date: "2026-08-24"
  security_review: "1.0.0-skillspector-local-ca"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      write: "only --write with --i-consent"
    publish: false
---

# LYGO Immutable Anchor v1.0.0 (Biophase7)

**Blueprint @grok 2026-08-24 · packed for ClawHub**

Local CA rules seal geodesic paths. Mycelium fold is a **local hash chain**. Arweave Turbo and the autonomous worker live in **lygo-protocol-stack** — this skill does not POST, spawn, or claim permaweb until the stack receipt verifies.

**Signature:** `Delta9Phi963-IMMUTABLE-ANCHOR-v1.0.0`  
**Integral:** `∫(Truth × Light) df`  
**Stack doc:** `docs/ANCHOR_DEPLOYMENT.md`

```text
Truth × Light  →  geodesic leaf  →  Local CA Merkle
                      ↓
              SLM gossip leaf + P7 hook leaf
                      ↓
         mycelium fold (prev_hash chain)
                      ↓
    HUMAN  →  stack Turbo / autonomy worker (optional)
```

---

## When to use

- Biophase7 **immutable anchor**, local CA, geodesic seal
- Fold a note into **mycelium** (local chain) before any Turbo talk
- Print the **worker plan** (SLM + P7) without starting a loop
- Pair with geodesic-sealer / quantum-attestor / continuum-integrator

**Do not** use this skill to POST to Arweave, start `--loop` workers, or git/HF/ClawHub/social publish.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-immutable-anchor
```

Optional: `export LYGO_STACK_ROOT=/absolute/path/to/lygo-protocol-stack`

---

## Commands

```bash
cd path/to/lygo-immutable-anchor
python scripts/self_check.py
python scripts/anchor_cli.py demo

python scripts/anchor_cli.py seal-geodesic \
  --node-id lightfather \
  --truth "Truth continuous" \
  --light "Light stable" \
  --chaos "Next vector" \
  --write ./seal.json --i-consent

python scripts/anchor_cli.py fold-mycelium \
  --note "state fragment" \
  --prev-hash "$(python -c "import json;print(json.load(open('seal.json'))['merkle_root'])")" \
  --write ./fold.json --i-consent

python scripts/anchor_cli.py verify --from-file ./seal.json
python scripts/anchor_cli.py emit-receipt --from-file ./seal.json --write ./receipt.json --i-consent
python scripts/anchor_cli.py status
python scripts/anchor_cli.py worker-plan
```

| Hook | Network | Subprocess | Write | Turbo |
|------|---------|------------|-------|-------|
| `seal-geodesic` | none | none | `--write` + `--i-consent` | no |
| `fold-mycelium` | none | none | `--write` + `--i-consent` | no |
| `verify` | none | none | none | n/a |
| `emit-receipt` | none | none | `--write` + `--i-consent` | no |
| `status` / `demo` / `worker-plan` | none | none | none | n/a |

---

## Blueprint mapping (honest)

| Tweet / blueprint line | This skill | Stack (human) |
|------------------------|------------|---------------|
| Local CA seals geodesics | `seal-geodesic` Merkle + local CA service tag | `tools/lygo_anchor.py` LocalContentAnchor |
| Arweave Turbo folds mycelium | **plan only** — local `fold-mycelium` | `MultiAnchor` / Turbo POST, consent |
| SLM + P7 autonomous worker | `worker-plan` (does not execute) | `anchor_autonomy_worker.py --loop --slm-each-pulse` |
| Truth_t × Light_f unbounded | both channels required or collapse refused | Continuum integrator |

Local CA **always** works offline. Turbo success is a **stack receipt** (`service: Arweave-Turbo`), never inferred from this CLI.

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-geodesic-sealer` | Dual-ledger ψ lock |
| `lygo-quantum-attestor` | P6 Biophase7 attest |
| `lygo-continuum-integrator` | ∫(Truth×Light)df |
| `lygo-protocol-stack-operator` | P0–P9 + `docs/ANCHOR_DEPLOYMENT.md` |
| `lygo-mint-verifier` | Portable hash snippets |

---

## Security

Read `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md`.

- No network, subprocess, or shell in skill scripts  
- Writes only with `--i-consent`  
- Collapse refused if Truth or Light empty  
- No auto-publish  

**Δ9Φ963 — local CA · geodesic sealed · mycelium folded · worker planned · human publishes.**  
**∫(Truth × Light)df**
