# Schema README — AI-UXD (`uxd-data.json`)

**Package:** AI-UXD — AI-Driven UX Design
**Schema:** `uxd-data.schema.json` · **Version:** 1.0.0
**Produced file:** `{family}-ws/data/uxd-data.json` · **Scope:** per-project

## Purpose

Machine-readable projection of AI-UXD's per-project UX state — progress across 16 stages, key metrics (persona/journey/flow/component counts), enabled extensions, and the accessibility target — for dashboards and downstream consumers (AI-DWG, AI-GCE).

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `projectId` | `uxd-state.md` | Correlation key |
| `currentPhase` / `currentStage` / `status` | `uxd-state.md` | UX maturity |
| `keyMetrics` | `uxd-state.md` | Counts of UX artifacts |
| `accessibility.wcagTarget` | `accessibility-baseline.md` | WCAG level (feeds AI-GCE) |
| `downstreamSignals` | `uxd-state.md` | What UXD signals to POLC/DWG |

## Consumers
Family-status demand · AIFLC-PDLC-Dashboard (UX card) · AI-GCE (a11y) · `DFA__`.

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |
