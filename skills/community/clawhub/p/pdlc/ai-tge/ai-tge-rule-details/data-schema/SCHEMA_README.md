# Schema README — AI-TGE (`tge-data.json`)

**Package:** AI-TGE — AI-Driven Test Governance Engine
**Schema:** `tge-data.schema.json` · **Version:** 1.0.0
**Produced file:** `{family}-ws/data/tge-data.json` · **Scope:** per-project

## Purpose

Machine-readable projection of AI-TGE's per-project test governance state — coverage, test counts, risk buckets, depth level, and observation history — for quality dashboards and portfolio roll-ups.

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `mode` / `currentPhase` | `tge-state.md` | Engine state |
| `registerStats.coverage` | `tge-state.md` | Coverage % |
| `registerStats.testsMissing` / `testsFailing` | `tge-state.md` | Quality gaps |
| `riskSummary` | `tge-state.md` | Critical/High/Medium/Low counts |
| `observationHistory[]` | `tge-state.md` | Coverage trend |

## Consumers
Family-status demand · AIFLC-PDLC-Dashboard (quality card) · `DFA__`.

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |
