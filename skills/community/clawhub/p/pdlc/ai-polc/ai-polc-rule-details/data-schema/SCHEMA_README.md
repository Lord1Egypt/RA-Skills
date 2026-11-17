# Schema README — AI-POLC (`polc-data.json`)

**Package:** AI-POLC — AI-Driven Product Ownership Life Cycle
**Schema:** `polc-data.schema.json` · **Version:** 1.0.0
**Produced file:** `{family}-ws/data/polc-data.json` · **Scope:** per-project

## Purpose

Machine-readable projection of AI-POLC's per-project backlog state — status, backlog summary, prioritized epics, product risks, and context factors — for dashboards, portfolio roll-ups, and `DFA__`.

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `projectId` | `polc-state.md` | Correlation key |
| `status` / `phase` / `stage` | `polc-state.md` | Backlog maturity |
| `backlog` | `polc-state.md` | Epic counts + priority model |
| `epics[]` | `prioritization-register.md` | Prioritized backlog |
| `risks[]` | `product-risk-register.md` | Product risk roll-up |

## Consumers
Family-status demand · AIFLC-PDLC-Dashboard (backlog card) · `DFA__`.

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |
