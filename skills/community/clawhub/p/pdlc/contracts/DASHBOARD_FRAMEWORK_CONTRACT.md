# Dashboard Framework — Shared Cross-Package Contract

**Version:** 1.1.0
**Date:** 2026-06-17
**Author:** Maheri
**Authored under:** `#persona-process-designer` (lead) + `#persona-compliance-governance` (support)
**Status:** ADOPTED — multi-project reconciliation added (v1.1.0, 2026-06-17); see the v1.1.0 note below
**Sibling:** `MANAGEMENT_FRAMEWORK_CONTRACT.md` v1.2.0 (governance spine — registers) · `OUTPUT_AND_STATE_CONTRACT.md` v1.0.0 (the `projects/` layout — source of truth)
**Plan:** See dashboard framework plan (internal development reference)

> **v1.1.0 amendment (2026-06-17 — multi-project reconciliation):** The original "one root, two mutually-exclusive modes" framing (§2) assumed a single `management_framework/` that switched between project and portfolio mode. The multi-project model retires that premise: **projects coexist** (not mutually exclusive), so each project carries its **own** spine + `dashboards/` at `projects/PRJ-{ABBREV}-{slug}/management_framework/dashboards/`, and **portfolio dashboards live at the workspace-level `portfolio/` area**. Consequence: the portfolio-mode **`{Project ID}/` sub-partition is retired** — per-project dashboards are now distributed to each project's own folder, so nesting copies of them under a shared portfolio root is redundant. AI-PPM rolls up by reading each project's dashboards keyed by `projectId` (§8), it does not partition copies. See `OUTPUT_AND_STATE_CONTRACT.md`.
>
> **Amendment (2026-06-22 — family-workspace prefix):** Per the install-lock design, dashboard locations now nest under `pdlc-ws/`: per-project dashboards at `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/management_framework/dashboards/`, portfolio dashboards at `pdlc-ws/portfolio/dashboards/`. Layout and roll-up wiring are unchanged — only paths gain the `pdlc-ws/` prefix (reflected throughout §2 and §8).

---

## 1. Purpose

Every AI-* family package produces governance, quality, or status information that benefits from a **visual roll-up** — a dashboard. Today one exists (AI-GCE's `compliance-dashboard.md`), placed ad hoc in `docs/`. This contract defines a single, consistent convention:

> **All dashboards live flat in `management_framework/dashboards/`**, attributed by `generatedBy` provenance front-matter (per `NAMING_AND_OWNERSHIP.md` §5). No per-package subfolders. No filename prefixes. One folder, one index, all packages contribute.

This is a **shared artifact contract** — the same stance as `MANAGEMENT_FRAMEWORK_CONTRACT.md`. No package "owns" or renders another's dashboard.

---

## 2. Two Dashboard Locations — Per-Project Spine vs Portfolio Area

In the multi-project model, **projects coexist** — the user is not in a single "project mode" or "portfolio mode." Dashboards therefore live in two distinct, simultaneously-valid locations:

| Location | Holds | Path |
|----------|-------|------|
| **Per-project spine** | That project's own dashboards (compliance, quality, status, architecture, ux, backlog, readiness) — **flat**, one set per project | `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/management_framework/dashboards/` |
| **Portfolio area** | Cross-project dashboards (portfolio health, flow/pipeline, idea funnel) — **flat** | `pdlc-ws/portfolio/dashboards/` |

Because each project owns its own `management_framework/dashboards/`, per-project records are never mixed across projects — the spine contract's per-project scope is preserved structurally (by separate folders), not by a mode switch.

> **Retired (v1.1.0):** the old portfolio-mode `{Project ID}/` sub-partition. Per-project dashboards now live in each project's own folder, so there is no shared portfolio root that needs to nest project copies. The portfolio area holds **only** portfolio-level dashboards; it correlates to per-project dashboards by `projectId` (§8), it does not copy or partition them.

### 2.1 Per-Project Layout (one per project)

```
pdlc-ws/projects/PRJ-{ABBREV}-{slug}/management_framework/
├── MANAGEMENT_FRAMEWORK.md                ← spine marker
├── dashboards/
│   ├── DASHBOARDS.md                      ← dashboard hub marker + index
│   ├── compliance-dashboard.md            ← generatedBy: AI-GCE
│   ├── quality-dashboard.md              ← generatedBy: AI-TGE
│   ├── project-status-dashboard.md       ← generatedBy: AI-PILC
│   ├── architecture-dashboard.md         ← generatedBy: AI-ADLC
│   ├── ux-dashboard.md                   ← generatedBy: AI-UXD
│   ├── backlog-dashboard.md             ← generatedBy: AI-POLC
│   └── readiness-dashboard.md            ← generatedBy: AI-DWG (optional snapshot)
└── (registers: Decision_Log.md, etc.)
```

> When AI-DWG carries the spine forward into the dev workspace (Option A), the carried-forward `management_framework/dashboards/` travels with it for the dev-workspace-side packages (GCE/TGE).

### 2.2 Portfolio Layout (one per workspace)

```
pdlc-ws/portfolio/
├── ppm-state.md  ·  Portfolio_Register.md   ← AI-PPM
└── dashboards/
    ├── DASHBOARDS.md                        ← hub marker + index
    ├── portfolio-dashboard.md              ← generatedBy: AI-PPM (cross-project)
    ├── flow-dashboard.md                  ← generatedBy: AI-FLO (cross-project)
    └── idea-pipeline-dashboard.md          ← generatedBy: AI-ILC (idea funnel)
```

The portfolio area holds **only** portfolio-level dashboards — all flat, attributed by `generatedBy`. It references each project's per-project dashboards by `projectId` for roll-up (§8); it never nests copies of them.


---

## 3. Detection by Marker

| Element | Value |
|---------|-------|
| **Hub folder** | `management_framework/dashboards/` |
| **Hub marker** | `dashboards/DASHBOARDS.md` |
| **Detection strategy** | Scan for `DASHBOARDS.md` inside the management_framework folder (which is itself detected by its own marker per the spine contract §3) |

The user chooses WHERE the management_framework lives. This contract defines WHAT must exist inside `dashboards/`.

---

## 4. Contribution Behavior

Every package that emits a dashboard follows the same rule:

```
1. DETECT the dashboard hub (by marker — dashboards/DASHBOARDS.md).
2. IF the hub exists:
      → CREATE (or refresh) only this package's own dashboard FILE in dashboards/.
      → Register/refresh this package's row in the hub index.
      → NEVER read-modify-delete another package's file.
3. IF no hub exists:
      → CREATE dashboards/ + DASHBOARDS.md marker + this package's dashboard file.
      → Self-contained standalone.
4. Refresh = overwrite own `ownership: generated` file only.
   Human-authored notes within `<!-- custom -->` markers are preserved (/ DWG Rule 6).
```

---

## 5. Hub Index Schema (`DASHBOARDS.md`)

```markdown
<!-- Dashboard hub | contract v1.0.0 -->

# Dashboards

Consolidated dashboard hub for **{project_name}** (Project ID: `{project_id}`).
Each AI-* package contributes its own dashboard here, identified by `generatedBy` front-matter.

## Contributing Dashboards

| Dashboard | File | Producer | Scope | Last Refreshed |
|-----------|------|----------|-------|:--------------:|
| Compliance | compliance-dashboard.md | AI-GCE | Per-project | {date} |
| Quality | quality-dashboard.md | AI-TGE | Per-project | {date} |

## Conventions
- One file per package, named by concern (`{concern}-dashboard.md`).
- Producer identified by `generatedBy` front-matter (not by filename or folder).
- Dashboards are regenerated (not hand-maintained) — `ownership: generated`.
- Filter by `generatedBy` to identify a package's contribution.
- Detection: this file's presence means "a dashboard hub exists here."
```

---

## 6. Provenance Front-Matter (per NAMING_AND_OWNERSHIP.md §5.2)

Every dashboard carries:

```yaml
---
generatedBy: AI-TGE
generatedVersion: 1.0.0
source:.tge/coverage-report.md,.tge/debt-scorecard.md
generatedOn: {date}
ownership: generated
projectId: {Project ID}
---
```

- `ownership: generated` — tool-regenerated on each refresh cycle.
- `projectId` — the immutable identifier minted at AI-PILC Stage 1; enables portfolio roll-up.
- `source` — upstream data file(s) that feed this dashboard.

---

## 7. Dashboard Inventory

### 7.1 Per-Project Dashboards

| Package | File | Class | What It Shows |
|---------|------|:-----:|---------------|
| AI-GCE | `compliance-dashboard.md` | Existing (relocate) | Tier progress, compliance score, rules/hooks inventory, active exceptions, MTTR, top violations |
| AI-TGE | `quality-dashboard.md` | Recommended | Coverage by commitment/component/risk, debt summary, open defects, trend |
| AI-PILC | `project-status-dashboard.md` | Extended | Open issues, top risks, recent decisions, action items, milestone RAG |
| AI-ADLC | `architecture-dashboard.md` | Extended | ADR status, requirement→component coverage, architecture risks, extension map |
| AI-UXD | `ux-dashboard.md` | Extended | Design-system coverage, accessibility baseline status, persona/journey/flow coverage |
| AI-POLC | `backlog-dashboard.md` | Extended | Priority distribution, DoR/DoD status, value-vs-effort, release readiness |
| AI-DWG | `readiness-dashboard.md` | Optional | One-time workspace readiness scorecard (point-in-time, not maintained) |

### 7.2 Portfolio Dashboards

| Package | File | Class | What It Shows |
|---------|------|:-----:|---------------|
| AI-PPM | `portfolio-dashboard.md` | Recommended | Cross-project health: phase/stage, progress %, RAG, top risks, prioritization, capacity |
| AI-FLO | `flow-dashboard.md` | Recommended | Pipeline view: where each project sits in the chain, next hop, pending handoffs |
| AI-ILC | `idea-pipeline-dashboard.md` | Optional | Idea funnel: captured → shaped → evaluated → approved/parked/rejected |

---

## 8. Roll-Up Wiring (Per-Project → Portfolio)

In portfolio mode, AI-PPM aggregates a **standard roll-up snapshot** from each project's dashboards, keyed by `Project ID`:

| Roll-Up Field | Per-Project Source |
|---------------|--------------------|
| Phase / Stage | Active `*-state.md` + AI-FLO `flo-state.md` position |
| Progress % | Completed vs. total stages in active state file |
| RAG / Health | Derived from open issues + risk exposure + schedule |
| Top Risks | Spine `Issue_Log.md` (severity H) + risk register |
| Open Issues | Spine `Issue_Log.md` (Status = Open) |
| Milestone Status | Charter milestones vs. actuals |
| Last Updated | Latest dashboard/state timestamp |

**Flow:** per-project dashboards (PILC/GCE/TGE), read from each project's `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/management_framework/dashboards/`, emit a snapshot → AI-FLO carries position → AI-PPM aggregates into `pdlc-ws/portfolio/dashboards/portfolio-dashboard.md`. Keyed by `Project ID`. PPM correlates by `projectId`; it does not copy per-project dashboards into the portfolio area.

---

## 9. Shared Conventions

1. **Detection-by-marker** — `dashboards/DASHBOARDS.md` is the hub marker.
2. **Append-if-exists / create-if-absent** — same pattern as the spine (§4).
3. **Provenance is the ownership mechanism** — `generatedBy` front-matter identifies the producer (no subfolders, no prefixes). Keys: `generatedBy`, `generatedVersion`, `source`, `generatedOn`, `ownership`, `projectId` (camelCase, locked v1.0.1).
4. **Project-ID keyed** — every per-project dashboard records `projectId` for portfolio correlation.
5. **Silent-when-complete** — dashboards exist always, but engines only speak when there's something to report.
6. **100% generic templates** — `{placeholder}` syntax; no project-specific content.
7. **Non-destructive refresh** — overwrite only the owning package's `ownership: generated` file; preserve `<!-- custom -->` sections.
8. **RAG + freshness standard** — shared legend (🔴 Red / 🟡 Amber / 🟢 Green); `Last refreshed` timestamp; staleness note when source is newer than dashboard.
9. **One index per root** — `DASHBOARDS.md` lists Contributing Dashboards (the human entry point).
10. **Standalone honored** — a package run alone still produces its dashboard in `dashboards/`; the hub degrades gracefully to a single contributor.

---

## 10. Boundaries (What This Contract Does NOT Do)

1. **Not a package.** A shared artifact contract only — no orchestration of packages.
2. **Does not replace the spine registers.** Dashboards *visualize/roll up* registers and state files; registers remain the source of truth.
3. **Does not enforce anything at runtime.** Enforcement is AI-GCE; testing is AI-TGE; dashboards are the *report*.
4. **Does not hardcode location.** WHERE the management folder lives is always the user's choice.
5. **Does not aggregate at the edge.** AI-FLO carries position only; aggregation is AI-PPM's job.
6. **Not portfolio governance.** The portfolio *register* (managing many projects) is AI-PPM's contract, not this one.

---

## 11. Execution Phases (Build-Gated)

| Phase | What | Gated By |
|-------|------|----------|
| A | ✅ This contract + spine amendment (Plan 2.3) | Done |
| B | Relocate AI-GCE dashboard into `dashboards/` | Phase A (done); GCE exists today |
| C | AI-TGE quality dashboard template | Phase A; AI-TGE build |
| D | AI-PPM/AI-FLO portfolio dashboards | AI-PPM/AI-FLO builds (Phase 4.1) |
| E | Extended per-project dashboards (PILC, ADLC, UXD, POLC, DWG) | Each package's build/update |
| F | Cross-cutting wiring + FAMILY_STRUCTURE trees | After B–E land |

---

*Contract Version: 1.1.0 | Created: 2026-06-10 | Amended: 2026-06-17 (v1.1.0 — multi-project reconciliation: per-project dashboards in each project's spine, portfolio dashboards at `pdlc-ws/portfolio/`, `{Project ID}/` sub-partition retired) | Authored under #persona-process-designer + #persona-compliance-governance*
