# Multi-Project Output & State — Shared Cross-Package Contract

**Version:** 1.0.0
**Date:** 2026-06-17
**Author:** Maheri
**Authored under:** `#persona-process-designer` (lead) + `#persona-cto-architect` (support)
**Status:** ADOPTED (2026-06-17) — formalizes the multi-project output & state architecture for the family. Sibling-contract amendments (Management Framework, Dashboard Framework, Naming & Ownership) follow as companion edits; see §15.

> **Amendment (2026-06-22 — family-workspace prefix):** All runtime paths in this contract now nest under the family workspace `pdlc-ws/` (e.g. `pdlc-ws/projects/PRJ-…/`, `pdlc-ws/ideas/`, `pdlc-ws/portfolio/`). The IDE root contains `pdlc-ws/`; the `projects/`, `ideas/`, `portfolio/`, `data/` areas live inside it. See `FAMILY_STRUCTURE.md` PART 2 + the install-lock design.

> **What this contract is:** the single source of truth for how the family organizes the output and state of **multiple projects in one workspace**. It defines the `projects/` layout, the per-project state model, the originator rule, the active-project pointer, and the spine carry-forward at the workspace-generation hinge.
>
> **This is a shared CONTRACT, not a package.** No package owns or orchestrates the others. Every per-project producer follows the same create-if-absent rules against shared artifacts (the per-project spine and the workspace registry).

---

## 1. Purpose

When more than one project runs in a single workspace, each package's output would otherwise pile up at the workspace root and mix with package machinery, the governance spine, and unrelated files. This contract introduces a **parent grouping (`projects/`) and a per-project umbrella** so that every project's outputs — across all packages — are nested, self-contained, and portable.

It ratifies, for the whole family, that **a workspace may hold many projects at once**. Each project moves through the chain independently; the only single-project property anywhere is the *generated dev workspace*, which is incidentally one project because it is one folder opened on its own.

---

## 2. Scope

- **Applies to:** every per-project artifact producer — **AI-PILC, AI-ADLC, AI-UXD, AI-POLC** (planning side) and **AI-DWG** (dev-workspace generator), plus the dev-workspace-side packages **AI-GCE** and **AI-TGE** which operate inside a generated workspace.
- **Idea stage (AI-ILC):** pre-project; produces *ideas*, not projects. It is out of the `projects/` model except that its approved-idea output seeds the first project producer. See §7.
- **Portfolio / orchestration (AI-PPM, AI-FLO):** registry-wide readers, not per-project operators. They are exempt from the active-project flow (§8) and are not originators (§7).

---

## 3. The Always-On Rule (Mandatory Structure)

The `projects/` structure is **mandatory in all conditions** — solo, single-project, and multi-project alike.

- There is **no flat-layout degradation**, **no adaptive activation**, and **no dual-mode branching**. A single package running on a single project uses the full `pdlc-ws/projects/{ProjectFolder}/` tree, the per-project spine, the per-project state file, and the workspace registry.
- "Standalone" means **"I do not require a predecessor to have run"** — it does **not** mean "I produce a different layout." A solo package produces the same structure as a chained one.
- This eliminates the "when does `projects/` activate?" question, removes any flat→`projects/` migration path, and keeps package logic free of mode conditionals.
- **Brownfield** is the one accommodation: if a user already has output in an older flat layout, standard brownfield detection applies — detect and offer a one-time, user-approved, non-destructive restructure, or honor an explicit user-chosen path. The `projects/` layout is the **default**, never a forced relocation.

---

## 4. Target Structure

> Illustrative project handles below (`PRJ-{ABBREV}-{slug}`) are placeholders. This contract defines WHAT must exist and WHERE it goes (always-on layout — §3).

```
{WORKSPACE-ROOT}/                                ◄ opened as the IDE root
│
└── pdlc-ws/                                    ◄ PDLC FAMILY WORKSPACE (all family output nests here)
    │
    ├── ideas/                                  ── AI-ILC (multi-idea funnel; pre-project)
    │
    ├── projects/                               ══ PROJECTS (multi-project) ══
    │   ├── PROJECTS.md                         ◄ registry + active pointer (§9)
    │   │
    │   ├── PRJ-{ABBREV}-{slug}/                 ◄ one project (★ may be the active project)
    │   │   ├── management_framework/           ◄ ONE per-project governance spine (§11)
    │   │   ├── pip/            ◄ AI-PILC  · pilc-state.md · …
    │   │   ├── architecture/   ◄ AI-ADLC · adlc-state.md · …
    │   │   ├── ux/             ◄ AI-UXD  · uxd-state.md · …
    │   │   ├── backlog/        ◄ AI-POLC · polc-state.md · …
    │   │   │
    │   │   └── {slug}-workspace/               ══ DEV WORKSPACE (generated by AI-DWG)
    │   │       │                                  opened SEPARATELY in its own IDE to build
    │   │       ├──.kiro/{steering,hooks}/     ◄ AI-GCE governs here
    │   │       ├── management_framework/       ◄ spine CARRIED FORWARD (Option A, §12)
    │   │       └── src/ · tests/ · configs …   ◄ AI-DLC v1 builds here
    │   │
    │   └── PRJ-{ABBREV2}-{slug2}/              ◄ another project, possibly at an earlier stage
    │       ├── management_framework/
    │       └── pip/  …
    │
    ├── portfolio/                              ── AI-PPM (when installed; cross-project)
    │
    └── data/                                   ── AI-DFE territory (bootstrapped at install)
```

---

## 5. Areas Reference

| Area | Path | Projects | Opened where | Marker(s) |
|------|------|:--------:|--------------|-----------|
| Ideas | `pdlc-ws/ideas/` | multi-idea | workspace IDE | `ilc-state.md` + per-idea folders |
| Project planning | `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/{pip,architecture,ux,backlog}/` | **multi** | workspace IDE | one `*-state.md` per package, per project |
| Dev workspace | `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/` | one folder = one project | opened **separately** in its own IDE | `.kiro/steering/workspace-rules.md`, `.kiro/hooks/` |
| Portfolio | `pdlc-ws/portfolio/` | cross-project | workspace IDE | `ppm-state.md` |
| Registry | `pdlc-ws/projects/PROJECTS.md` | index of all | workspace IDE | — (regenerable index) |

> These are folders/areas, **not** zones. Every package (including AI-DWG) runs in the one multi-project workspace; a dev workspace is generated per project and opened separately to build.

---

## 6. Naming Conventions

| Element | Rule | Example (illustrative) |
|---------|------|------------------------|
| Project folder | `PRJ-{ABBREV}-{slug}/` (short handle prefix + readable slug) | `PRJ-XYZ-web-portal/` |
| Canonical Project ID (metadata) | `PRJ-{ABBREV}-{YYYY}-{NNN}` — full key, in state files / workspace-rules / registry | `PRJ-XYZ-2026-001` |
| Slug | lower-case; spaces → hyphens; punctuation stripped | `web-portal` |
| Per-package output folder | role name | `pip/` · `architecture/` · `ux/` · `backlog/` |
| Dev workspace folder | `{slug}-workspace/` (distinct name for clean IDE logging) | `web-portal-workspace/` |
| Spine entry ID | **project-qualified, phase-prefixed:** `{PHASE}-{ABBREV}-{TYPE}-{N}` | `PILC-XYZ-D-1` · `ADLC-XYZ-C-2` |

- The **folder prefix** uses the short `PRJ-{ABBREV}` handle (a stable domain key exception); the **full** `PRJ-{ABBREV}-{YYYY}-{NNN}` remains the canonical correlation key in metadata.
- The project handle inside the spine ID (in addition to the per-project folder) makes any later cross-project reconciliation unambiguous even if rows are copied out of their folder.
- **Abbreviation-collision edge case:** if two projects in one workspace would share an abbreviation, disambiguate at that point (e.g. append the year/sequence to the folder). Not pre-solved.

---

## 7. Project Origination & the Originator Roster

A Project ID is minted **once**, at the first point a project takes shape, and is then **immutable** and adopted by every subsequent package (the correlation-key rule — mint early, write to marker, never re-mint).

**Originator rule (create-if-absent):** the **first originator-eligible package** to operate on a project mints `PRJ-{ABBREV}-{YYYY}-{NNN}` (asking the user for name/abbreviation), creates `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`, seeds the per-project spine, and writes the registry row. Every later package **detects and adopts** the existing Project ID — it never re-mints.

| Package | Originator-eligible? | Reason |
|---------|:--------------------:|--------|
| **AI-PILC** | ✅ **Default originator** | Canonical chain entry; mints at intake when present |
| **AI-ADLC** | ✅ Eligible | Produces per-project artifacts; originates if run first |
| **AI-UXD** | ✅ Eligible | Produces per-project artifacts; originates if run first |
| **AI-POLC** | ✅ Eligible | Produces per-project artifacts; originates if run first |
| **AI-DWG** | ❌ Excluded | Generates a dev workspace *from* ADLC/POLC/UXD outputs — cannot originate a project from nothing; always operates on an existing project |
| **AI-ILC** | ❌ Excluded | Pre-project — produces idea IDs; the Project ID is minted when an idea routes to a project |
| **AI-GCE / AI-TGE** | ❌ Excluded | Operate inside the generated dev workspace, not the multi-project workspace |
| **AI-FLO** | ❌ Excluded | Produces no per-project artifacts (orchestrator/courier) |
| **AI-PPM** | ❌ Excluded | Portfolio aggregator — operates registry-wide, produces no per-project artifacts |

> This makes origination **a role any planning-side producer can fill** (PILC/ADLC/UXD/POLC) — not a hard PILC dependency — preserving solo use while guaranteeing the structure is always created.

---

## 8. Active-Project Pointer & Selection Flow

Exactly **one** project is `active` (the default target) at a time. Every per-project producer follows this flow on start:

```
1. Scan pdlc-ws/projects/*/ for the predecessor marker (§13).
2. Read pdlc-ws/projects/PROJECTS.md → identify the ★ active project.
3. Prompt: "Work on the active project {X}, or pick another?"  (default = active)
4. Operate inside the chosen project's folder; update its *-state.md + the registry row.
5. If the user switches active project, update the ★ pointer in PROJECTS.md.
```

**Exempt from this flow (registry-wide readers, not per-project operators):**
- **AI-FLO** — reasons over the *whole* registry to route/orchestrate; has no single active project; writes no per-project state.
- **AI-PPM** — operates portfolio-wide; reads/enriches the registry; produces portfolio-level output; not bound to the active pointer.

---

## 9. Workspace Registry — `pdlc-ws/projects/PROJECTS.md`

> **Detailed specification:** `PROJECTS_REGISTRY_SPEC.md` is the authority for the registry's full schema, field semantics, lifecycle operations, and regeneration. This section is the in-contract summary.

**Purpose:** the workspace-level index of all projects + the active pointer + per-package progress (a cross-project integrity index).

**Ownership:** shared, standalone artifact — every per-project producer maintains it (create-if-absent, append-if-exists — the same pattern as the spine). It is **not** owned by AI-PPM; PPM *enriches/reads* it when installed (graceful standalone,).

**Not a state tier:** the registry is a **regenerable index** — rebuildable by scanning project folders. It holds no authoritative state of its own (§10).

**Scope:** workspace-local. If a project folder is exported elsewhere, the registry row stays behind; re-import re-registers it.

**Indicative schema:**
```markdown
# Projects Registry

Active project: ★ PRJ-{ABBREV}-{YYYY}-{NNN}

| Project ID            | Folder                  | Active | ILC | PILC | ADLC | UXD | POLC | Dev (DWG) |
|-----------------------|-------------------------|:------:|-----|------|------|-----|------|-----------|
| PRJ-{ABBREV}-2026-001 | PRJ-{ABBREV}-{slug}     |   ★    | ✓   | done | done | wip | wip  | generated |
| PRJ-{ABBR2}-2026-002  | PRJ-{ABBR2}-{slug2}     |        | ✓   | done | —    | —   | —    | —         |
```

---

## 10. State Model (Two-Tier, Per-Project)

The two state tiers both live **inside the project folder**, so a project is fully self-contained and portable (lift the folder → its spine + all package states move with it).

- **Tier 1 — per-project governance spine** (`pdlc-ws/projects/PRJ-{ABBREV}-{slug}/management_framework/`): the project's governance state (decisions, changes, issues, lessons), with project-qualified phase IDs (§6, §11).
- **Tier 2 — per-project package state files** (`pdlc-ws/projects/PRJ-{ABBREV}-{slug}/{package}/*-state.md`): each package's workflow state for that project, doubling as the chain marker the next package detects.

**Not a state tier:** the workspace registry (`PROJECTS.md`, §9) is a regenerable index + active pointer. **There is no per-package global state file.**

---

## 11. Management-Framework Spine (Per-Project, Carried Forward)

- During planning there is **ONE consolidated spine** per project at `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/management_framework/`, with **project-qualified, phase-prefixed IDs** of the form `{PHASE}-{ABBREV}-{TYPE}-{N}` (e.g. `PILC-XYZ-D-1`). This extends the shared-spine contract's namespace with a project handle so multi-project workspaces never collide across projects. The `{N}` counter is assigned per the **ID Assignment Protocol** in `MANAGEMENT_FRAMEWORK_CONTRACT.md` §8 (scan-and-increment against the register file).
- This **amends** `MANAGEMENT_FRAMEWORK_CONTRACT.md`, whose ID format was `{PHASE}-{TYPE}-{NNN}`. See §15.
- When AI-DWG generates the dev workspace, the spine is **carried forward** (Option A) into `{slug}-workspace/management_framework/`. The dev-workspace packages (DWG/GCE/TGE) append there, because the dev workspace is opened on its own and cannot reach the planning-side spine one level up.
- Net: one continuous per-project record — the planning-side copy is the planning record; the dev-workspace copy is the live build-phase record.
- **Known edge (deferred):** a planning-side change *after* dev started makes the two copies diverge → cross-hinge reconciliation/downstream-signaling. Deferred to a later version.

---

## 12. Dev Workspace Generation & Carry-Forward (Option A)

- **AI-DWG is multi-project.** For a selected project, it reads that project's planning outputs and generates that project's dev workspace at `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/`. Many projects can each have their own.
- The dev workspace is **opened as its own IDE root** (separate window), **never** copied to the planning root — this avoids `.kiro/` steering collision and re-cluttering.
- DWG **carries the spine forward** (§11). Switching the build project = open a different project's dev workspace. Regenerating after an upstream change = **delta reconciliation** — non-destructive, proposes changes, preserves the carried-forward spine. There is no lock and nothing to "re-bind."
- **External-path export** is a supported-but-not-default escape hatch: allowed **with a clear warning** that exporting outside the project folder **breaks the feedback loop** (reconciliation, spine carry-forward, and any parent-workspace process cannot reach it without manual intervention). When used, the project state stores a `devWorkspacePath` pointer so DWG can locate it; portability is weakened.

---

## 13. Marker Auto-Detection (Extended Scan Paths)

Detection is by **marker, never by hardcoded path**. Because outputs now nest under `projects/`, every per-project producer extends its predecessor-marker scan to include:

```
pdlc-ws/projects/*/{predecessor-package}/{predecessor}-state.md
../projects/*/{predecessor-package}/{predecessor}-state.md
```

in addition to its existing scan locations. Without this extension, nesting under `projects/` would defeat auto-detection.

---

## 14. Brownfield

Every per-project producer asks: "is there already output here in an older flat layout?" If so:
- detect it, and offer a **one-time, user-approved, non-destructive** restructure into `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`, **or**
- operate in the standard `projects/` layout alongside the legacy output (never force-move existing files).

The `projects/` layout is the default *and the mandatory target* for new work. Existing human entries and IDs are never renumbered destructively.

---

## 15. Relationship to Sibling Contracts (Supersession Notes)

This contract is the source of truth for the `projects/` layout. It introduces the following dated amendments to its siblings (applied as companion edits):

| Sibling contract | Amendment |
|------------------|-----------|
| `MANAGEMENT_FRAMEWORK_CONTRACT.md` | "Project root" = `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/` in multi-project mode; spine entry ID changes from `{PHASE}-{TYPE}-{NNN}` to **project-qualified** `{PHASE}-{ABBREV}-{TYPE}-{N}`; spine is **carried forward** into the dev workspace at the DWG hinge. |
| `NAMING_AND_OWNERSHIP.md` | Adds the `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/` folder convention as a stable-domain-key exception; notes "project root" = the per-project folder. |
| `DASHBOARD_FRAMEWORK_CONTRACT.md` | Per-project dashboards live in each project's own `management_framework/dashboards/`; portfolio dashboards live at `pdlc-ws/portfolio/`. The prior single-root mutually-exclusive-modes framing is reconciled to many per-project spines + one portfolio area. |
| `TRACEABILITY_CONTRACT.md` | No change in single-family scope — `projectId` remains the correlation key, reinforced by this contract. (A second Family-ID tier is reserved for a future multi-family world and is out of scope here.) |

> Each sibling carries a dated amendment note pointing back to this contract — no silent divergence.

---

## 16. Boundaries (What This Contract Does NOT Do)

1. **Not a package.** It orchestrates nothing; it is a shared layout/state contract.
2. **Fixed standard layout.** The `projects/` structure and per-package output folders (`pip/`, `architecture/`, `ux/`, `backlog/`, `{slug}-workspace/`) are deterministic. Brownfield is the only accommodation for pre-existing layouts.
3. **Does not enforce compliance.** Runtime governance remains AI-GCE's responsibility, inside the dev workspace.
4. **Not portfolio governance.** Cross-project roll-up is AI-PPM; this contract only guarantees the registry + per-project structure PPM reads.
5. **Does not define drift detection.** The dev-workspace drift baseline is a deferred future feature (§17) and is not part of this rollout.

---

## 17. Deferred / Out of Scope

- **Drift-baseline feature** (the as-generated reference a dev workspace measures tampering against — form, placement, and who-checks). Deferred to a future version; not a dependency for this architecture.
- **Cross-hinge spine reconciliation** for late planning-side changes (planning spine vs carried-forward dev spine divergence). Deferred.
- **Abbreviation-collision disambiguation** (two projects, same abbreviation). Resolved when first encountered.
- **Multi-family / Family-ID tier.** This contract covers the single-family world. A second correlation tier and a cross-family registry topology are reserved for when a second family exists.

---

*Contract Version: 1.0.0 | Created: 2026-06-17 | Authored under #persona-process-designer + #persona-cto-architect*
