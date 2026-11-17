# Schema README — AI-PPM (`ppm-data.json`)

**Package:** AI-PPM — AI-Driven Portfolio Management
**Schema:** `ppm-data.schema.json` · **Version:** 1.0.0
**Produced file:** `{family}-ws/data/ppm-data.json` · **Scope:** portfolio (cross-project)

## Purpose

Machine-readable projection of AI-PPM's portfolio state — project counts by status, the portfolio register, strategic objectives, prioritization model, governance cadence, and last roll-up. This is the natural source for a portfolio dashboard.

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `summary` | `ppm-state.md` | Total/active/paused/retired/pending counts |
| `projects[]` | `portfolio-register.md` | Per-project status + health RAG + alignment |
| `lastRollUp` | `ppm-state.md` | Freshness of cross-project roll-up + FLO status |
| `prioritization` | `ppm-state.md` | Ranking model |
| `cadence` | `ppm-state.md` | Next sync/health/strategic review dates |

## Consumers
Family-status demand · AIFLC-PDLC-Dashboard (portfolio overview) · `DFA__`.

## Notes
PPM is portfolio-scoped (one file, not per-project). Uses its own portfolio-level registers (PPM-D-*), not the per-project spine.

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |
