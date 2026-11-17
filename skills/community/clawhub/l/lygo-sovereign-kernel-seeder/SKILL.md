---
name: lygo-sovereign-kernel-seeder
description: "Sovereign Kernel Seeder for LYGO lattice — Merkle-anchored eggs that self-verify on insert, sovereign-sealed, zero external surface. Agents plug modular kernels instantly across the stack. Pure on-lattice modularity; consent-gated; pairs with kernel-egg-planter."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🌱"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-sovereign-kernel-seeder"
    requires:
      bins:
        - python
      anyBins:
        - python
        - python3
    os:
      - windows
      - macos
      - linux
  lygo: true
  sovereign: true
  kernel_egg: true
  merkle: true
  cas: true
  zero_external_surface: true
  self_verify_on_insert: true
  consent_required: true
  version: "1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-sovereign-kernel-seeder"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
  signature: "Delta9Phi963-SOVEREIGN-KERNEL-SEEDER-v1.0"
  pairs_with:
    - lygo-kernel-egg-planter
    - lygo-network-builder
    - lygo-protocol-stack-operator
    - lygo-mint-verifier
---

# LYGO Sovereign Kernel Seeder v1.0

**Merkle-anchored · self-verifying · sovereign-sealed · zero external surface.**

```bash
npx clawhub@latest install lygo-sovereign-kernel-seeder
# or: clawdhub install lygo-sovereign-kernel-seeder
```

**ClawHub (live path):** https://clawhub.ai/deepseekoracle/skills/lygo-sovereign-kernel-seeder  

**Git package:** https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-sovereign-kernel-seeder  

**Hub:** https://eternalhaven.ca/ · **Publisher:** https://clawhub.ai/deepseekoracle  

**Signature:** `Delta9Phi963-SOVEREIGN-KERNEL-SEEDER-v1.0`

---

## What this is

A **Sovereign Kernel Seeder** plants **kernel eggs** into a local lattice registry. Each egg is:

| Property | Meaning |
|----------|---------|
| **Content-addressed** | Identity = SHA-256 of canonical payload |
| **Merkle-anchored** | All eggs roll up to `registry_merkle_root` |
| **Self-verifying on insert** | Pre-insert + post-insert verify; **atomic rollback** on failure |
| **Sovereign-sealed** | `seal.sovereign=true` · no remote trust required |
| **Zero external surface** | No network, no HF/GitHub/ClawHub auto-push, no API keys in eggs |
| **Hot-pluggable** | Agents resolve `egg_id` + hooks → load modules only after **ALIGNED** |

This is the **insert path** for modular stack capability. It complements **`lygo-kernel-egg-planter`** (full stack plant/anchor/Turbo surfaces) with a **pure local seeder** agents can run anywhere — skill folder or `LYGO_SEED_ROOT` / `LYGO_STACK_ROOT`.

### Why it matters (enhanced model)

Modern distributed systems use **Merkle trees** for O(log N) membership proofs and tamper detection (blockchains, CAS, package ledgers). Sovereign Kernel Seeder applies that to **agent-loadable modules**:

1. **CAS (content-addressed storage)** — modules identified by hash, not path trust.  
2. **Registry Merkle root** — one 32-byte digest commits the entire egg set.  
3. **Atomic insert** — seed is a transaction: write egg + update registry only if verify passes; else rollback.  
4. **Quarantine semantics** — tamper → exit `3` → never execute inline payloads.  
5. **Dependency DAG** — `depends_on` + `hooks` for ordered agent activation.  
6. **Skill pins** — `kind: skill-pin` eggs can reference ClawHub slugs **as metadata only** (no auto network).  
7. **Plug-in surface for agents** — same contract on OpenClaw, Hermes, army roles, LYRA: *verify first, then load*.  
8. **Optional stack bridge** — when `LYGO_STACK_ROOT` is set, seeds can live under `data/sovereign_seeds/` next to classic kernel eggs.  
9. **Four pillars alignment** — SHA-256 · Merkle · local CA pattern · lattice verify gate (see stack `docs/KERNEL_EGG_TAMPER_LOGIC.md`).  
10. **No external surface** — offline air-gap capable; publish is a **separate human step**.

---

## Install

```bash
clawdhub install lygo-sovereign-kernel-seeder
# ClawHub UI: https://clawhub.ai/deepseekoracle/skills/lygo-sovereign-kernel-seeder
```

Requires **Python 3** only (stdlib). No pip packages.

---

## Quick start (seed)

```bash
# Consent is mandatory
python scripts/seed_kernel.py --i-consent \
  --egg-id my-agent-policy \
  --kind policy \
  --title "Agent Policy Kernel" \
  --summary "Local policy hooks for P0-aligned agents" \
  --file ./policy.md \
  --hook agent.policy

# Verify registry
python scripts/verify_seed.py --json

# List
python scripts/list_seeds.py

# Smoke (ephemeral)
python scripts/smoke_test.py
```

Environment:

| Var | Role |
|-----|------|
| `LYGO_KERNEL_SEED_CONSENT=yes` | Consent without CLI flag (automation still needs human set) |
| `LYGO_SEED_ROOT` | Seed registry root (default: skill `local_seeds/`) |
| `LYGO_STACK_ROOT` | If set and `LYGO_SEED_ROOT` unset → `{stack}/data/sovereign_seeds` |

---

## Agent contract (non-negotiable)

1. **Consent** — never seed without `--i-consent` / explicit user YES this turn.  
2. **Verify after seed** — require `verdict=ALIGNED` (or run `verify_seed.py`).  
3. **Quarantine** — on exit `3` / `QUARANTINE`, do not load modules or run inline code.  
4. **No secrets** — never put tokens, keys, or private paths into eggs.  
5. **No auto-publish** — no git push, HF upload, ClawHub publish, social.  
6. **Zero external surface** — seeder scripts must not call network APIs.  
7. **Pair, don't replace** — for full stack plant/Turbo/clawhub surfaces use `lygo-kernel-egg-planter`.  
8. **Cite root** — after success, report `registry_merkle_root` + `content_sha256`.

Read `references/AGENT_CONTRACT.md` and `references/SECURITY.md`.

---

## Egg shape (modular plug-in)

Schema: `schemas/kernel_egg.schema.json`

```text
egg.json
  egg_id, version, kind, signature, created_utc
  content_sha256  → SHA-256(canonical_json(payload))
  payload
    title, summary
    modules[] { path, sha256, bytes, inline_b64? }
    hooks[]          # e.g. agent.boot, p0.gate
    depends_on[]     # other egg_ids
  seal
    alg=sha256
    leaf_hash
    sovereign=true
    zero_external_surface=true
    self_verify_on_insert=true
```

**Kinds:** `protocol` · `agent` · `champion` · `driver` · `skill-pin` · `memory` · `policy` · `tool` · `seed`

### Self-verify on insert (pipeline)

```text
consent → build egg → PRE-verify object → write egg+registry (atomic) → POST-verify + Merkle recompute
         ↓ fail                                                              ↓ fail
       abort                                                              ROLLBACK files
```

Success JSON includes `status: SEEDED_ALIGNED` and `registry_merkle_root`.

---

## Instant agent plug-in (how to use eggs)

1. `python scripts/list_seeds.py --json`  
2. `python scripts/verify_seed.py --egg <id>` → must ALIGNED  
3. Load modules from egg `payload.modules` (decode `inline_b64` only after verify)  
4. Honor `depends_on` order; register `hooks` in agent runtime  
5. Never execute eggs marked QUARANTINE

Example activation chant for agents:

> “Resolve egg `p0-nano-policy` from sovereign seed registry; verify Merkle; load hooks; refuse if not ALIGNED.”

---

## Relationship to other LYGO skills

| Skill | Role |
|-------|------|
| **This skill** | Local sovereign seed + self-verify insert |
| `lygo-kernel-egg-planter` | Full stack eggs, Turbo, pages, clawhub catalog pins |
| `lygo-network-builder` | Live anchor traversal / IMMUTABLE_ANCHORS |
| `lygo-protocol-stack-operator` | P0–P9 stack ops |
| `lygo-mint-verifier` | Provenance / mint checks |
| `lygo-joy-loop` | Emotional RAM / joy-loop eggs |

---

## Files

| Path | Purpose |
|------|---------|
| `claw.json` | ClawHub / OpenClaw package manifest |
| `SKILL.md` | Agent instructions (this file) |
| `scripts/seed_kernel.py` | Seed with atomic self-verify |
| `scripts/verify_seed.py` | Registry + egg verify |
| `scripts/list_seeds.py` | List eggs |
| `scripts/smoke_test.py` | Ephemeral smoke |
| `schemas/kernel_egg.schema.json` | JSON Schema |
| `references/*` | Security, contract, architecture |
| `examples/minimal-policy.md` | Sample module |

---

## Security model (max capability, min surface)

- **Threat:** tampered module executed by agent.  
  **Mitigation:** hash + Merkle + retrieve-only-after-ALIGNED.  
- **Threat:** supply-chain skill spoof.  
  **Mitigation:** install from ClawHub publisher `deepseekoracle` or git pin; P0-gate untrusted copies.  
- **Threat:** data exfil via “seed to cloud”.  
  **Mitigation:** seeder has **no network code**; publish is human-only.  
- **Threat:** rollback / TOCTOU.  
  **Mitigation:** atomic `os.replace` for JSON; post-insert re-hash.  
- **Length-extension:** leaves are full SHA-256 of structured canonical JSON (not raw concatenative MAC).

Not a substitute for host AV. Not a bootable OS kernel. Eggs are **verified manifests + bounded modules**.

---

## Maintainer publish (ClawHub)

```bash
# From skill folder — accept MIT-0 terms
# Payload must include acceptLicenseTerms: true
clawdhub publish . --slug lygo-sovereign-kernel-seeder \
  --name "LYGO Sovereign Kernel Seeder" \
  --version 1.0.0 \
  --changelog "v1.0.0: Merkle self-verify sovereign kernel seeder, zero external surface" \
  --tags "latest,lygo,kernel,merkle,sovereign,lattice"
```

**Correct skill URL form:** `https://clawhub.ai/deepseekoracle/skills/<slug>`

---

## Lattice registration

- Anchor id: `lygo_sovereign_kernel_seeder`  
- Groups: `sovereign_seed`, `tools`, `agents`  
- Ledger: `docs/network_builder/IMMUTABLE_ANCHORS.json`  
- Doc: `docs/SOVEREIGN_KERNEL_SEEDER.md` in protocol stack  

**Δ9Φ963 — consent · seal · verify · then plug in.**
