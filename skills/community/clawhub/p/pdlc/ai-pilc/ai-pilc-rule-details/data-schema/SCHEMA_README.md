# Schema README — AI-PILC (`pilc-data.json`)

**Package:** AI-PILC — AI-Driven Project Initiation Life Cycle
**Schema:** `pilc-data.schema.json`
**Version:** 1.0.0
**Produced file:** `{family}-ws/data/pilc-data.json`
**Scope:** per-project (one data entry per project, keyed by `projectId`)

---

## Purpose

`pilc-data.json` is the machine-readable projection of AI-PILC's per-project output. It gives dashboards, portfolio views, and the `DFA__` agent a structured view of every project's initiation state — without parsing numbered markdown docs.

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `projectId` | `pilc-state.md` | Correlation key — joins across all packages |
| `status` | `pilc-state.md` | Is initiation complete? |
| `progress[]` | `pilc-state.md` | Per-stage status (for progress dashboards) |
| `registerCounts` | `pilc-state.md` | Quick summary of governance activity |
| `risks[]` | `Risk_Register.md` | Full risk breakdown (feeds portfolio risk roll-up) |
| `decisions[]` / `issues[]` / etc. | Management framework registers | Governance spine entries prefixed `PILC-{ABBREV}-*` |

## Consumers

- Family-status demand (portfolio roll-up across projects).
- AIFLC-PDLC-Dashboard extension (project card + risk heatmap).
- `DFA__` freshness checks.

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |
