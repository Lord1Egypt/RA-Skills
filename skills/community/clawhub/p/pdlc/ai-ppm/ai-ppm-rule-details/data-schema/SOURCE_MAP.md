# SOURCE_MAP — AI-PPM

> Declares where AI-PPM's raw data lives and how AI-DFE extracts it. Paths relative to `pdlc-ws/`. PPM is portfolio-scoped (cross-project).

**Package:** AI-PPM — AI-Driven Portfolio Management
**Schema:** `ppm-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** portfolio (cross-project, family-level)

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `portfolio/ppm-state.md` | `status: not-run` → all payload fields `null` |

## Source Files

| # | Source path (relative to `pdlc-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `portfolio/ppm-state.md` | engine status, portfolio summary, roll-up ingestion, prioritization model, cadence |
| 2 | `portfolio/portfolio-register.md` | the project portfolio (one row per registered project) |
| 3 | `portfolio/management_framework/Decision_Log.md` | portfolio governance decisions (prefix `PPM-D-*`) |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `currentPhase` | 1 | Engine Status → `Current Phase` |
| `currentStage` | 1 | Engine Status → `Current Stage` |
| `lastActivity` | 1 | Engine Status → `Last Activity` |
| `depthLevel` | 1 | Engine Status → `Depth Level` |
| `activeExtensions[]` | 1 | Engine Status → `Active Extensions` |
| `summary.totalProjects` | 1 | Portfolio Summary → `Total Projects` |
| `summary.active` | 1 | Portfolio Summary → `Active` |
| `summary.paused` | 1 | Portfolio Summary → `Paused` |
| `summary.retired` | 1 | Portfolio Summary → `Retired (this period)` |
| `summary.pendingRegistration` | 1 | Portfolio Summary → `Pending Registration` |
| `lastRollUp.timestamp` | 1 | Last Roll-Up Ingestion → `Timestamp` |
| `lastRollUp.projectsRefreshed` | 1 | → `Projects Refreshed` |
| `lastRollUp.anomaliesFlagged` | 1 | → `Anomalies Flagged` |
| `lastRollUp.floStatus` | 1 | → `FLO Status` (connected/fallback-manual) |
| `strategicObjectives[]` | 1 | Strategic Objectives list |
| `prioritization.model` | 1 | Prioritization Model → `Model` |
| `prioritization.lastRanked` | 1 | → `Last Ranked` |
| `cadence` | 1 | Governance Cadence → `{ nextPortfolioSync, nextHealthReview, nextStrategicReview }` |
| `projects[]` | 2 | One object per portfolio-register row: `{ projectId, name, status, priority, healthRag, strategicAlignment }` |
| `decisions[]` | 3 | Rows prefixed `PPM-D-*`: `{ id, date, summary, status }` |

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- PPM is **portfolio-scoped** (not per-project): one `ppm-data.json` covering the whole portfolio. This is the natural source for a portfolio dashboard.
- PPM has its own portfolio-level `management_framework/` (PPM-D-* / PPM-L-*) — NOT the per-project spine (/ Contract §7).
- PPM reads `projects/PROJECTS.md` but does not own it; DFE reads PPM's own register for portfolio composition.
