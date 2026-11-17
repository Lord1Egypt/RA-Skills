# DEMAND — AIFLC-PDLC-Dashboard

> **Shipped with the consumer (Obligation 1).** This file travels with the dashboard extension at `tools/extensions/AIFLC-PDLC-Dashboard/data-demand/dashboard-data.demand.md` — the consumer-side twin of a producer's `data-schema/SOURCE_MAP.md`. On install, the dashboard also adds its row to `{family}-ws/data/CONSUMER_REGISTRY.md`. AI-DFE's demander discovery (Stage 1.3) resolves this declaration, materializes it into `{family}-ws/data/demands/dashboard-data.demand.md`, and shapes `dashboard-data.json` from per-package data (Layer 2). The dashboard UI reads the `data` payload of the produced file.

**Consumer:** AIFLC-PDLC-Dashboard (VS Code extension + HTML dashboard)
**Output file:** `dashboard-data.json`
**Refresh:** on-demand (after any `DAT__` pass)
**Scope:** portfolio + per-project

---

## Output Shape

The dashboard consumes the rich shape below (inside the envelope's `data`). One `projects[]` row per project; each carries the per-package progress, chain edges, management roll-up, and (optional) PO/Architecture/UX detail panes.

| Field path (in output `data`) | Type | Source domain | Description |
|--------------------------------|------|---------------|-------------|
| `generated` | string | (generated) | ISO timestamp of this shaping |
| `projects[].id` | string | `projectId` across packages | Project correlation key |
| `projects[].name` | string | `pilc-data.projectName` / `dwg-data.systemName` | Display name |
| `projects[].status` | enum | derived | active / complete / pending / blocked |
| `projects[].progress` | number | mean of package `progress.pct` | Overall % |
| `projects[].lastActivity` | string | max `lastUpdated` across packages | Last activity date |
| `projects[].packages[]` | array | each `{pkg}-data` | Per-package `{ code, status, phase{c,t,name}, progress{pct,done,total}, stage{name}, blockers[], artifacts[] }` |
| `projects[].edges[]` | array | `flo-data.routes` (or canonical chain) | Chain edges `{ from, to, type, label }` |
| `projects[].mgmt` | object | `pilc-data`/`adlc-data`/`polc-data` register counts | `{ decisions, risks, changes, actions, issues, lessons }` |
| `projects[].mgmtDetail` | object | management_framework registers | Detail arrays per register type |
| `projects[].po` | object\|null | `polc-data.po` | **Full Product-Ownership pane** (§2.1.3): vision, roadmap{now,next,later}, releases[], backlog{…,dorReady,dodReady}, acceptance, velocity, stakeholders[]. `null` only if AI-POLC absent/unrun |
| `projects[].arch` | object\|null | `adlc-data.arch` | **Full Architecture pane** (§2.1.4): c4Progress, vision, principles[], constraints[], nfrs{}, integrations[], adrs[], risks[], techStack{}, containers[], c4Diagrams{l1,l2,l3}, diagrams{}. `null` only if AI-ADLC absent/unrun |
| `projects[].ux` | object\|null | `uxd-data.ux` | **Full UX pane** (§2.1.5): personas[], journeys[], flows[], userFlows, wireframes{}, designSystem{}, designSystemFiles[], componentLibrary{}, informationArchitecture, accessibility. `null` only if AI-UXD absent/unrun |
| `ideas[]` | array | `ilc-data.ideas` | Idea funnel items |
| `ppm` | object | `ppm-data` | Portfolio metrics `{ totalProjects, dispatched, pending, strategicFit, topPriority }` |
| `health` | object | aggregate | `{ totalBlockers, stalledProjects, overallProgress }` |

## Shape Notes

- `packages[]` maps each per-package data file into the dashboard's package shape. `phase`/`progress`/`stage` are derived from each package's state-derived fields (e.g. `currentPhase`, `currentStage`, `progress[]`).
- `po`/`arch`/`ux` panes are populated from `polc-data`/`adlc-data`/`uxd-data` when present, else `null`.
- `edges` come from `flo-data` routes when FLO is present; otherwise the canonical chain order.

## Full-Mode Coverage

When the **complete PDLC package set** is installed and run, every pane fills from your own data: AI-POLC→`po`, AI-UXD→`ux`, AI-ADLC→`arch`, AI-ILC→`ideas`, plus PM/Chain/MF from the per-package data. Run **`DAT__ full`** to assemble the complete contract and get a readiness report naming any package/pane still missing or `not-run` (vs `DAT__ all`, which silently degrades absent producers to `null`). Each rich pane is a 1:1 copy of the producing package's data — the renderer safely guards any pane that is still `null`.

## How This Consumer Reads Its Data (HARD RULE — Obligation 2)

1. Know ONE path: `{family}-ws/data/REGISTRY.json`.
2. Read the registry, find the entry for `dashboard-data.json`, get its `path`.
3. Open that path, parse it, and read the `data` payload.
4. NEVER hardcode `{family}-ws/data/dashboard-data.json`, and NEVER parse `*-state.md` files directly — the data fabric is the sole source.

## Schema

AI-DFE owns the validating schema: `{family}-ws/data/dashboard-data.schema.json`. The extension no longer ships its own schema copy.
