# Schema README — AI-ILC (`ilc-data.json`)

**Package:** AI-ILC — AI-Driven Idea Life Cycle
**Schema:** `ilc-data.schema.json` · **Version:** 1.0.0
**Produced file:** `{family}-ws/data/ilc-data.json` · **Scope:** family (ideas funnel)

## Purpose

Machine-readable projection of AI-ILC's idea funnel — all ideas with status/domain/route/score, plus the current idea's detail — for funnel dashboards and "what's in the pipeline?" views.

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `ideas[]` | `idea-register.md` | Full funnel (one row per idea) |
| `counts` | `idea-register.md` | total / approved / rejected |
| `currentIdea` | `ilc-state.md` | Active idea's stage + score + route |

## Consumers
Family-status demand · AIFLC-PDLC-Dashboard (funnel card) · `DFA__`.

## Notes
Idea IDs (NNN) are not Project IDs — ILC mints ideas, not projects. Approved ideas route downstream where a Project ID is later minted.

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |
