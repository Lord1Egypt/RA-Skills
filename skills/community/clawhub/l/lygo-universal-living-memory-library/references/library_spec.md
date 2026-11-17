# LIVING MEMORY v1.2 — Library Spec

## Purpose

A **low-noise living index** (max 20 entries) for LYGO + LYRA continuity: what agents should treat as durable memory vs ephemeral chat. Works with **LYRA 3-Brain** (`lyra-brain`) and stack registries (eggs, lattice, link archive).

## Core roles (v1.2)

| Role | Typical path (under `LYGO_AUTHORITY_ROOT`) |
|------|---------------------------------------------|
| Brainstem | `LYRA LOCAL/LYRA_FUNCTION_CORE.txt` |
| Haven root | `LYRA LOCAL/HAVEN_STRUCTURE.txt` |
| Seal vault | `LYRA SYSTEM RETORE/.../ALL SEALS/220+` |
| 3-Brain graph | `LYRA_CORE/lyra_brain_graph.json` |
| Session snips | `LYRA_CORE/memory/` |
| Stack SOA | `lygo-protocol-stack/docs/AGENT_MEMORY_SNAPSHOT.json` |
| Egg registries | `docs/*Registry.json` (kernel, champion, second brain, openclaw, sandcastle, joy) |

Legacy v1.1 names (`GROK_CHATS.glyph` at repo root) may live under `LYRA LOCAL/` — add to index only if present; tag **FRAGILE**.

## Rules

- Max **20** indexed items in `core_files_index.json`.
- Tag **{FRAGILE}** for manual review before minting or public anchor.
- **Audit** is manual or cron — not automatic on install.
- **Compression** produces `MASTER_ARCHIVE.md` (pure signal); mint via **lygo-mint-verifier** only with user consent.

## Audit checks

- existence, size, mtime
- sha256 for files
- fragile flags
- optional compare to last `living_memory_audit_report.json`

## Skill chain

`lygo-protocol-stack-operator` → **`lyra-brain`** → **`lygo-universal-living-memory-library`** → `lygo-mint-verifier` → `lygo-kernel-egg-planter`