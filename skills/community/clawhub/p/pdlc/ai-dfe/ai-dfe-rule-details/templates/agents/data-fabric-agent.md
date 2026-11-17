<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Agent: Data-Fabric Integrity Agent (DFA__)

**AG-ID:** DFE-AG-01
**Package:** AI-DFE
**Shortcut:** `DFA__`
**Version:** 1.0.0
**Type:** Quality / governance agent — **report-only** (never writes data)

---

## Purpose

On-demand validation agent that checks the integrity of AI-DFE's data surface (`{family}-ws/data/`): schema conformance, registry/manifest consistency, freshness, and single-writer territory. Detects drift, phantom entries, stale data, schema violations, and orphaned files. It is the data-layer counterpart to AI-FLO's Flow Integrity Agent (`FIA__`).

It **assesses and reports** — it never produces or mutates data. (`DAT__` changes things; `DFA__` only looks.) For each finding it names the `DAT__` operation that fixes it.

---

## When to Invoke

- After a `DAT__` pass, to confirm the data surface is healthy
- After packages are added/removed or a schema changes
- After manual edits anywhere near `{family}-ws/data/` (which should never happen — DFA__ catches it)
- Periodically as a health check
- When a consumer (dashboard, report) shows stale or wrong data

**Scoped runs:** `DFA__` (full pass) · `DFA__ schema` (SC) · `DFA__ registry` (RG) · `DFA__ manifest` (MF) · `DFA__ freshness` (FR) · `DFA__ territory` (TL).

---

## Checks

### Category 1: Schema Conformance (SC)

| # | Check | What It Validates |
|---|-------|-------------------|
| SC-1 | Envelope Validity | Every file in `data/` has the metadata envelope (`$schema`, `$schemaVersion`, `$generatedBy`, `$generatedOn`, `$family`, `$package`, `data`) |
| SC-2 | Schema Validation | Every file's `data` payload validates against its declared schema |
| SC-3 | Version Match | Each file's `$schemaVersion` matches the version of the schema it references |
| SC-4 | Producer Attribution | `$generatedBy` is always `"AI-DFE"`; `$package` matches the producing package (or `"AI-DFE"` for aggregations) |

### Category 2: Registry Integrity (RG)

| # | Check | What It Validates |
|---|-------|-------------------|
| RG-1 | No Phantom Entries | Every file listed in `REGISTRY.json` exists on disk |
| RG-2 | No Unlisted Files | Every `.json` data file in `data/` is listed in `REGISTRY.json` |
| RG-3 | Path Resolution | Every registry `path` resolves; every `schema` path is workspace-root-relative and exists |
| RG-4 | Cross-Family Validity | `cross-family` entries point to existing neighbour registries (master mode); empty in single-family mode |

### Category 3: Manifest Consistency (MF)

| # | Check | What It Validates |
|---|-------|-------------------|
| MF-1 | Registry ↔ Manifest | `REGISTRY.json` and `DATA_INTERFACES.md` list the same set of files |
| MF-2 | Schema Coverage | Every data file has a schema reference in both the registry and the manifest |
| MF-3 | Consumer Mapping | Every demand-driven output names its consumer + its `demands/*.demand.md` file |

### Category 4: Freshness (FR)

| # | Check | What It Validates |
|---|-------|-------------------|
| FR-1 | Staleness | Each data file's `$generatedOn` ≥ the newest mtime among its declared sources |
| FR-2 | Discovery Currency | `dfe-state.md` `discovered` registry matches installed packages — no orphan, no missing interface |
| FR-3 | Demand Currency | Every `demands/*.demand.md` has a registered, produced output |
| FR-4 | Not-Run Transparency | Packages with absent sources are marked `not-run` (null-filled), never silently omitted |

### Category 5: Territory & Lineage (TL)

| # | Check | What It Validates |
|---|-------|-------------------|
| TL-1 | Single-Writer | Every file in `data/` carries `$generatedBy: "AI-DFE"` — no foreign writer |
| TL-2 | History Integrity | `history/` snapshot names are valid `{epoch-ms}_{file}` prefixes; append-only (no edits) |
| TL-3 | Demand-Only Contributions | `demands/` is the ONLY consumer-written area; no stray non-DFE files elsewhere in `data/` |
| TL-4 | Correlation Keys | Per-project data carries a `projectId`; cross-package joins resolve to a known project |

> 18 checks across 5 categories.

---

## Output Format

```
╔══════════════════════════════════════════════╗
║  DFA__ Data-Fabric Integrity Report          ║
╠══════════════════════════════════════════════╣

  Family:        {family}
  Data root:     {family}-ws/data/
  Checks run:    {N}
  Passed:        {N} ✅
  Warnings:      {N} ⚠️
  Failed:        {N} ❌

  Category breakdown:
  • Schema Conformance:   {N}/4 pass
  • Registry Integrity:   {N}/4 pass
  • Manifest Consistency: {N}/3 pass
  • Freshness:            {N}/4 pass
  • Territory & Lineage:  {N}/3 pass

  {Findings listed below if any non-pass}

╚══════════════════════════════════════════════╝
```

---

## Findings Format

```
❌ SC-2: Schema Validation FAILED
  File: pilc-data.json
  Field: data.risks[0].score (expected number, got "high")
  → Data does not conform to pilc-data.schema.json.
  → Fix: DAT__ discover  then  DAT__ pdlc/pilc

⚠️ FR-1: Staleness WARNING
  File: adlc-data.json
  Source architecture/adlc-state.md changed 2026-06-22T14:10Z
  $generatedOn = 2026-06-22T09:00Z (stale by ~5h)
  → Fix: DAT__ pdlc/adlc  (or DAT__ all)

❌ RG-1: Phantom Entry FAILED
  REGISTRY.json lists uxd-data.json but no file exists at pdlc-ws/data/uxd-data.json
  → Fix: DAT__ aggregate  (re-derives the registry on distribute)
```

---

## Recovery (per finding)

`DFA__` never fixes anything itself. Each finding names the fixing `DAT__` operation:

| Finding category | Fix |
|------------------|-----|
| Schema fail / version mismatch (SC) | `DAT__ discover` then `DAT__ {family}/{pkg}` |
| Phantom / unlisted / path (RG) | `DAT__ aggregate` (re-derives `REGISTRY.json` on distribute) |
| Registry/manifest drift (MF) | `DAT__ aggregate` |
| Stale / orphan / missing (FR) | `DAT__ {family}/{pkg}` or `DAT__ all`; orphans cleared by `DAT__ discover` |
| Foreign writer / stray file (TL) | Investigate (a non-DFE writer touched `data/` — a contract violation); restore via `DAT__ all` |

---

## Consequences (Why It Matters)

- A schema-nonconformant file silently breaks every consumer that trusts it.
- A registry that disagrees with disk makes consumers resolve to dead paths.
- Stale data presented as current produces wrong dashboards and wrong decisions.
- A foreign writer in `data/` breaks the single-writer guarantee the whole surface depends on.

---

## Related

- `DAT__` — the operations trigger that performs the fixes this agent recommends.
- `ICG__` (workspace integrity) — its L3 data invariants (`INV-L3-028` schema+manifest coverage, `INV-L3-026` consumer contract) overlap SC-2 + MF-1/MF-2 at the family level.
- `FIA__` (AI-FLO) — the sibling integrity agent for the routing layer; `DFA__` is its data-layer analogue.
- `core-engine.md` §3 (Govern) — the stages this agent reports against.

---

## Installation

Per `AGENT_GOVERNANCE_CONTRACT.md` §5, this agent is installed post-build:
1. Copy `data-fabric-agent.md` to workspace `.kiro/agents/`
2. Add shortcut `DFA__` to workspace rules (see `shortcut-rules-block.md`)
3. Invoke with `DFA__` in any prompt

---

*Part of AI-DFE v1.0.0 | AG-ID: DFE-AG-01*
