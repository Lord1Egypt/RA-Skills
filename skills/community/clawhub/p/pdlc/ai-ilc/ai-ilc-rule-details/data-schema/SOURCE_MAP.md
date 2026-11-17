# SOURCE_MAP — AI-ILC

> Declares where AI-ILC's raw data lives and how AI-DFE extracts it. Paths relative to `pdlc-ws/`. ILC is the pre-project ideas funnel.

**Package:** AI-ILC — AI-Driven Idea Life Cycle
**Schema:** `ilc-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** family (ideas funnel — pre-project)

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `ideas/ilc-state.md` | `status: not-run` → all payload fields `null` |

## Source Files

| # | Source path (relative to `pdlc-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `ideas/ilc-state.md` | current idea workflow state, status, stage, score, route |
| 2 | `ideas/idea-register.md` | all ideas (the funnel view — one row per idea) |
| 3 | `ideas/{NNN}-{slug}/` | per-idea deliverable folder — Approved/Feature Idea Brief + supporting files (→ `ideas[].files`, `ideas[].brief`) |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `currentIdea.name` | 1 | Workflow State → `Idea Name` |
| `currentIdea.id` | 1 | Workflow State → `Idea ID` (NNN) |
| `currentIdea.status` | 1 | Workflow State → `Status` (Captured/Shaped/Evaluated/Scoped/Approved/Routed/Parked/Rejected) |
| `currentIdea.stage` | 1 | Workflow State → `Current Stage` (1-6) |
| `currentIdea.domain` | 1 | Workflow State → `Domain Detected` |
| `currentIdea.route` | 1 | Workflow State → `Route` (pending/new-project/change-request/feature-backlog) |
| `currentIdea.briefFile` | 1 | Workflow State → `Brief File` |
| `currentIdea.created` | 1 | Workflow State → `Created` |
| `currentIdea.lastUpdated` | 1 | Workflow State → `Last Updated` |
| `currentIdea.score` | 1 | Score section → `{ problemClarity, userNeed, strategicFit, differentiation, feasibility, reusability, chainValue, total }` (n/35) |
| `ideas[]` | 2, 3 | One object per register row → `{ id, name, stage, status, score, scoreMax, decision, domain, depth, route, routeTarget, brief, created, lastUpdated, files[] }`. **`stage` is LOWERCASE** (renderer filters on it) — derive from the register `Status` (e.g. `Routed`→`routed`); keep `status` (PascalCase) for back-compat. `score`/`scoreMax` split the `n/35` value into numbers. `routeTarget` = the routed Project ID / backlog target. `brief` = one-line description from the register row (or the idea brief's summary). `files[]` = per-idea deliverables in `ideas/{NNN}-{slug}/` as `{ name, path, status }` objects (exclude `ilc-state.md`, shared `idea-register.md`). |
| `counts.total` | 2 | Count of register rows |
| `counts.approved` | 2 | Count where status = Approved/Routed |
| `counts.rejected` | 2 | Count where status = Rejected/Parked |

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- ILC is family-scoped at the funnel level: one `ilc-data.json` listing all ideas + the current idea's detail.
- `ilc-state.md` tracks the *current* idea workflow; `idea-register.md` is the full funnel. DFE reads both — the register for the portfolio-of-ideas view, the state for the active idea.
- Idea IDs (NNN) are not Project IDs — ILC mints ideas, not projects. Approved ideas route to AI-PILC/AI-POLC where a Project ID is later minted.
- **Dashboard Ideas funnel (ISS-003):** the dashboard filters the funnel by **lowercase `stage`** (`captured|shaped|evaluated|scoped|approved|routed|parked|rejected`) and reads `idea.brief`, `idea.routeTarget`, and `idea.files[]`. DFE emits `stage` as the lowercase form of the register `Status`, splits `score`/`scoreMax` from `n/35`, and lists per-idea deliverables as `files[]` objects. (Supersedes the earlier counts-only/PascalCase-status projection — the funnel was empty when the renderer received `status` instead of lowercase `stage`.)
