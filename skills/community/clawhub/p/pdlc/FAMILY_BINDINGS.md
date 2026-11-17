# FAMILY_BINDINGS.md — PDLC

> **⚠️ GENERATED — Do not edit manually.**
> Derived from: package gate contracts + cross-family flow definitions.
> Regenerate after any gate contract or cross-family flow change.

---

```yaml
generatedAt: 2026-06-27
generatorVersion: 1.0.0
family: PDLC
familyRepo: AIPDLC
protocolVersion: 1.2.0
interfaceVersion: 1.0
```

---

## Internal Bindings (auto-derived from gate contracts)

> These edges form automatically via capability-type match within the family. Every `emits-type` matched by a sibling's `consumes-types` creates an edge.

### Chain Topology (the canonical routing graph)

```
AI-ILC ──► AI-PILC ──► AI-PPM
                  │
                  └──► AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG ──► AI-GCE
                                                                │
                                                                └──► AI-TGE

AI-FLO ◄── (reads all markers — orchestration overlay)
AI-DFE ◄── (reads all markers + each package's SOURCE_MAP — data-fabric overlay)
```

> **Sequential Project layer:** POLC→UXD→ADLC→DWG. Each package feeds the next.
> The edge table below shows all capability-type matches (including feedback/enrichment edges).
> The *forward sequence* is determined by routing policy, not by edge existence alone.

### Internal Edge Table

| # | From | Emits Type | To | Consumes Type | Via Marker |
|---|------|-----------|-----|---------------|------------|
| I-01 | AI-ILC | `idea-decision@1` | AI-PILC | `idea-decision@^1` | `ilc-state.md` |
| I-02 | AI-ILC | `idea-decision@1` | AI-PPM | `idea-decision@^1` | `ilc-state.md` |
| I-03 | AI-PILC | `project-initiation@1` | AI-ADLC | `project-initiation@^1` | `pilc-state.md` |
| I-04 | AI-PILC | `project-initiation@1` | AI-UXD | `project-initiation@^1` | `pilc-state.md` |
| I-05 | AI-PILC | `project-initiation@1` | AI-POLC | `project-initiation@^1` | `pilc-state.md` |
| I-06 | AI-PILC | `project-initiation@1` | AI-PPM | `project-initiation@^1` | `pilc-state.md` |
| I-07 | AI-ADLC | `architecture-design@1` | AI-UXD | `architecture-design@^1` | `adlc-state.md` |
| I-08 | AI-ADLC | `architecture-design@1` | AI-POLC | `architecture-design@^1` | `adlc-state.md` |
| I-09 | AI-ADLC | `architecture-design@1` | AI-DWG | `architecture-design@^1` | `adlc-state.md` |
| I-10 | AI-UXD | `ux-design@1` | AI-POLC | `ux-design@^1` | `uxd-state.md` |
| I-11 | AI-UXD | `ux-design@1` | AI-DWG | `ux-design@^1` | `uxd-state.md` |
| I-12 | AI-POLC | `product-backlog@1` | AI-DWG | `product-backlog@^1` | `polc-state.md` |
| I-13 | AI-DWG | `development-workspace@1` | AI-GCE | `development-workspace@^1` | `dwg-state.md` |
| I-14 | AI-DWG | `development-workspace@1` | AI-TGE | `development-workspace@^1` | `dwg-state.md` |

> **AI-FLO is a wildcard observer, not a capability edge.** It consumes `"*"` (all types) as routing triggers — it reads every marker to track positions but forms no capability-typed edge. It is excluded from the edge table by design.

> **AI-DFE is also a wildcard observer, not a capability edge.** Like AI-FLO, it consumes `"*"` (all markers, plus each package's `SOURCE_MAP.md`) as gather triggers and forms no capability-typed edge. It **emits** `data-surface@1` (internal visibility) — consumed by tools/dashboards via `{family}-ws/data/REGISTRY.json`, not by sibling packages — so it appears in the chain summary as a data overlay but is excluded from the internal edge table by design.

### Fan-In Gates (from intra routing-policy)

| Consumer | Waits For | Gate Behavior |
|----------|-----------|---------------|
| AI-DWG | AI-ADLC (terminal predecessor) | Validates AP + PBP + UXP all present (guaranteed by sequence: POLC→UXD→ADLC) |
| AI-UXD | AI-POLC | Sequential: waits for PBP complete before starting |
| AI-ADLC | AI-UXD | Sequential: waits for UXP complete before starting |
| AI-PPM | AI-ILC + AI-PILC | Accept any (registers both ideas and projects) |

> **Note on edge table vs. routing policy:** The internal edge table (above) shows all capability-type matches — these represent *potential* data flows. Some edges are **forward** (chain sequence: I-05→I-10→I-07→I-09), some are **feedback/enrichment** (I-03, I-04, I-07→AI-UXD, I-08→AI-POLC). The routing policy (sequential POLC→UXD→ADLC→DWG) determines the *order*; the edges determine what data flows where.

---

## External Bindings (from CROSS_FAMILY_FLOWS.md)

> These edges are explicitly declared. Each represents a cross-family seam. Optional = family always works without it (P4).

### Inbound — Neighbors That Feed PDLC

| Flow | From | Into | Type | Via Marker | Gate Controller | Optional |
|------|------|------|------|------------|-----------------|:--------:|
| FLOW-001 | BVLC · AI-BPLC | PDLC · AI-PILC | `validated-business-case@1` | `bplc-state.md` | `(BVLC) ai-bplc § Gate Contract` | ✅ |
| FLOW-002 | EAFLC · AI-TRM | PDLC · AI-ILC | `capability-input@1` | `trm-state.md` | `(EAFLC) ai-trm § Gate Contract` | ✅ |

### Outbound — Neighbors PDLC Feeds

| Flow | From | To | Type | Via Marker | Gate Controller | Optional |
|------|------|----|------|------------|-----------------|:--------:|
| FLOW-003 | PDLC · AI-DWG | RUNFLC · AI-SLO | `development-workspace@1` | `dwg-state.md` | `ai-dwg § Gate Contract` | ✅ |

---

## Canonical Chain Summary

> This section replaces the hand-maintained family table for topology purposes. The diagram and edge table above are the authoritative routing graph. Package order reflects the sequential execution sequence.

| Layer | Package | Type | Emits | Consumes From |
|-------|---------|------|-------|---------------|
| Portfolio | AI-ILC | lifecycle | `idea-decision@1` | (user raw idea) or `capability-input` (external) |
| Portfolio | AI-PILC | lifecycle | `project-initiation@1` | `idea-decision` or `validated-business-case` (external) or (user raw requirement) |
| Portfolio | AI-PPM | adaptive engine | `portfolio-state@1` | `project-initiation`, `idea-decision` |
| Edge | AI-FLO | active engine | `orchestration-state@1` | (all types — routing overlay) |
| Project | AI-POLC | lifecycle | `product-backlog@1` | `project-initiation` |
| Project | AI-UXD | lifecycle | `ux-design@1` | `project-initiation`, `product-backlog` |
| Project | AI-ADLC | lifecycle | `architecture-design@1` | `project-initiation`, `product-backlog`, `ux-design` |
| Project | AI-DWG | generator | `development-workspace@1` | `architecture-design`, `product-backlog`, `ux-design` |
| Project | AI-GCE | companion engine | `governance-engine@1` | `development-workspace` |
| Project | AI-TGE | companion engine | `test-strategy@1` | `development-workspace` |
| Overlay | AI-DFE | adaptive engine (data fabric) | `data-surface@1` | (all package markers + SOURCE_MAPs — data overlay; consumed by tools via `REGISTRY.json`) |

---

## Generation Metadata

| Check | Result |
|-------|--------|
| Internal edges derived | 14 (FLO + DFE excluded — wildcard observers) |
| External inbound flows | 2 (FLOW-001, FLOW-002) |
| External outbound flows | 1 (FLOW-003) |
| Cycles detected | 0 |
| Compatibility issues | 0 (per-type scoping — GATE_PROTOCOL §4.2) |
| Fan-in gates | 3 (DWG, POLC, PPM) |

---

*Generated 2026-06-18 (regenerated 2026-06-27 to register AI-DFE) · Source: gate contracts (11 packages) + CROSS_FAMILY_FLOWS.md (3 flows) · Generator v1.0.0 · Part of the AIFLC Communication Fabric*
