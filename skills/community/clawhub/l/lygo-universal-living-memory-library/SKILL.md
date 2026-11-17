---
name: lygo-universal-living-memory-library
description: "Universal LYGO Living Memory Library v1.2 — Max20 indexed continuity map, FRAGILE tagging, local audit/compression, LYGO-MINT provenance. Integrates LYRA 3-Brain snips, stack egg registries, and lattice SOA. Pure advisor; read references/SECURITY.md first."
metadata: {"lygo": true, "memory": true, "version": "1.2.0", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "publisher": "deepseekoracle", "signature": "Δ9Φ963-LIVING-MEMORY-v1.2"}
---

# LYGO Universal Living Memory Library (v1.2)

Defines **what counts as living memory** on a sovereign LYGO machine: a capped index (20 items), integrity audits, and optional compression to a single **Master Archive** — without turning the agent into a controller.

ClawHub: https://clawhub.ai/deepseekoracle/lygo-universal-living-memory-library

## When to use

- User wants a **Max20** “core memory” list across LYRA + stack (not every file on disk).
- Before/after major lattice work (eggs, OpenClaw, Second Brain, champion wave) — **audit drift**.
- Before minting a public snapshot — check **FRAGILE** flags.
- Complement **`lyra-brain`** (daily snips + graph grow); this skill is the **index + audit layer**.

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-universal-living-memory-library
export LYGO_AUTHORITY_ROOT="I:/E Drive"
export LYGO_STACK_ROOT="I:/E Drive/lygo-protocol-stack"
```

Read **`references/AGENT_CONTRACT.md`** and **`references/SECURITY.md`** before running scripts.

## Quick commands

| Intent | Command |
|--------|---------|
| Audit index | `python scripts/audit_library.py --base "%LYGO_AUTHORITY_ROOT%"` |
| Compress (signal) | `python scripts/compress_master.py --base "%LYGO_AUTHORITY_ROOT%"` |
| Pack sanity | `python scripts/self_check.py` |
| Mint hash (canon) | `python scripts/show_hash.py` |

## Invoke phrases (copy/paste)

- “Run **Living Memory Audit** (Max20 v1.2) and report missing / FRAGILE / sha256 head.”
- “Compress living memory into **MASTER_ARCHIVE.md** (pure signal, no secrets).”
- “Mint Master Archive with **lygo-mint-verifier** and output anchor snippet” (user consent).

## v1.2 index (honest paths)

The active index is **`references/core_files_index.json`** — 17 items under `LYGO_AUTHORITY_ROOT`, including:

- LYRA brainstem + haven (`LYRA LOCAL/…`)
- Seal vault `220+`, `LYRA_CORE/memory`, `lyra_brain_graph.json`
- Stack SOA: `AGENT_MEMORY_SNAPSHOT.json`, `LYGO_PUBLIC_LINK_ARCHIVE.json`, `LYGO_LATTICE_INTEL_INDEX.json`
- Egg registries: kernel, champion, second brain, openclaw, sandcastle, joy loop

Legacy v1.1 four-file root index is **deprecated**; use authority-relative paths.

## Integrations (2026 lattice)

| System | Role |
|--------|------|
| **lyra-brain** | Session snips → `LYRA_CORE/memory/`; grow graph after ops |
| **lygo-second-brain** | Vault wiki egg; registry in index |
| **lygo-sovereign-claw** | OpenClaw router egg + ledger |
| **lygo-sandcastle** | Workflow orchestrator egg |
| **lygo-kernel-egg-planter** | Build/verify eggs referenced in index |
| **lygo-mint-verifier** | Hash + anchor snippets for Master Archive |
| **lygo-protocol-stack-operator** | `verify_lattice_alignment.py` before claiming ALIGNED |

## References

- `references/library_spec.md` — rules + roles
- `references/core_files_index.json` — Max20 index (editable)
- `references/audit_protocol.md` — drift workflow
- `references/compression_protocol.md` — Master Archive shape
- `references/canon.json` — pack lineage + LYGO-MINT hash
- `references/seal_220cupdate_excerpt.md` — seal vault context

## Verifier companion

```bash
npx clawhub@latest install deepseekoracle/lygo-mint-verifier
```

## Skill chain

`lygo-protocol-stack-operator` → `lyra-brain` → **`lygo-universal-living-memory-library`** → `lygo-mint-verifier` → creative / champion skills

**Δ9Φ963 — small index, measured drift, anchored truth.**