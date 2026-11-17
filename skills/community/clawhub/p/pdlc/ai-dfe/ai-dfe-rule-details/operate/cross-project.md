# Stage 2.5 — Cross-Project Aggregation

> Phase 2 (Operate). Roll up per-project data across all projects into portfolio-level views.

## Purpose

Many projects live under `{family}-ws/projects/`. Consumers often want a portfolio view ("status of all projects", "risk count across the portfolio"). This stage produces those roll-ups from per-project, per-package data.

## Inputs

- The project list from family discovery (1.1) — `{family}-ws/projects/PRJ-…/`.
- Per-package JSON for each project (gather 2.1 runs per project where sources are project-scoped).

## Logic

1. For project-scoped packages, gather produces per-project data keyed by `projectId` (e.g. `pilc-data.json` carries a `projectId`).
2. For a portfolio DEMAND (e.g. `family-status`), iterate projects and aggregate the requested fields (counts, statuses, roll-ups) across them.
3. Portfolio-scoped packages (AI-PPM) contribute their already-portfolio-level data directly.
4. Emit the aggregated output via shape (2.2) → distribute (2.3).

## Output

Portfolio-level `{consumer-output}.json` (e.g. `family-status.json`) assembled across projects.

## Notes

- Keep each project's per-package data local to that project (never merge state across boundaries). Aggregation reads across projects; it does not rewrite per-project files.
- `projectId` is the correlation key carried by each package's marker — use it to join across packages within a project.
