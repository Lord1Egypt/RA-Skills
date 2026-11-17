# Projects Registry — `pdlc-ws/projects/PROJECTS.md` Specification

**Version:** 1.0.0
**Date:** 2026-06-17
**Author:** Maheri
**Authored under:** `#persona-process-designer` (lead) + `#persona-cto-architect` (support)
**Status:** ADOPTED (2026-06-17) — companion to `OUTPUT_AND_STATE_CONTRACT.md` (which is the source of truth for the `projects/` layout). This spec details the registry artifact that contract §9 summarizes.

> **Amendment (2026-06-22 — family-workspace prefix):** The registry lives at `pdlc-ws/projects/PROJECTS.md` (the `projects/` area now nests under the family workspace `pdlc-ws/`). All paths below carry the `pdlc-ws/` prefix; semantics and schema are unchanged.

> **What this specifies:** the structure, ownership, and lifecycle of `pdlc-ws/projects/PROJECTS.md` — the workspace-level index of every project, the active-project pointer, and per-package progress. It is a **regenerable index**, not a state tier.

---

## 1. Role

`pdlc-ws/projects/PROJECTS.md` is the **cross-project integrity index** for one workspace. It answers three questions at a glance:

1. **What projects exist here?** (one row per project)
2. **Which one is active?** (the ★ pointer — the default target for per-project producers)
3. **How far has each project progressed per package?** (the per-package status columns)

It is **not** authoritative state. Every fact in it is rebuildable by scanning the project folders and their `*-state.md` markers. If the registry is deleted, any originator-eligible package can regenerate it. The authoritative state lives in the per-project spine and the per-project `*-state.md` files (contract §10).

---

## 2. Ownership — Shared, Create-if-Absent

The registry is a **shared, standalone artifact** maintained by every per-project producer (AI-PILC, AI-ADLC, AI-UXD, AI-POLC), using the same pattern as the governance spine:

```
1. Look for pdlc-ws/projects/PROJECTS.md.
2. IF absent → CREATE it with the header + this project's row + set this project ★ active.
3. IF present → APPEND this project's row if missing, else UPDATE this project's row
                (own columns only); never delete or rewrite another project's row.
```

- **Not owned by AI-PPM.** PPM *reads and enriches* the registry when installed (graceful standalone,) — it adds portfolio columns/annotations but does not own the file.
- **AI-FLO** reads the whole registry to route/orchestrate; it writes no per-project rows.
- **Append/update is non-destructive at the row level** — a package edits only its own project's row and only its own columns.

---

## 3. Location & Marker

| Element | Value |
|---|---|
| **Path** | `pdlc-ws/projects/PROJECTS.md` (workspace-local) |
| **Marker semantics** | presence of the file = "a registry exists here" |
| **Detection** | scan `pdlc-ws/projects/PROJECTS.md`; if absent, create on first project origination |

The registry is **workspace-scoped**: it is not part of a portable project bundle. If a project folder is exported elsewhere, its row stays behind; re-importing the folder lets a producer re-register it.

---

## 4. Schema

```markdown
<!-- Projects registry | regenerable index — not a state tier -->

# Projects Registry

Active project: ★ {Canonical Project ID}

| Project ID            | Folder                  | Active | ILC | PILC | ADLC | UXD | POLC | Dev (DWG) | Created    | Updated    |
|-----------------------|-------------------------|:------:|-----|------|------|-----|------|-----------|------------|------------|
| PRJ-{ABBREV}-2026-001 | PRJ-{ABBREV}-{slug}     |   ★    | ✓   | done | done | wip | wip  | generated | 2026-01-01 | 2026-01-09 |
| PRJ-{ABBR2}-2026-002  | PRJ-{ABBR2}-{slug2}     |        | ✓   | done | —    | —   | —    | —         | 2026-01-05 | 2026-01-05 |
```

### 4.1 Field semantics

| Column | Meaning | Written by |
|--------|---------|-----------|
| **Project ID** | Canonical immutable key `PRJ-{ABBREV}-{YYYY}-{NNN}` (contract §6) | originator (mint); others read-only |
| **Folder** | The project folder name `PRJ-{ABBREV}-{slug}` (relative to `projects/`) | originator |
| **Active** | `★` for exactly one project; blank otherwise | whichever package switches the active project |
| **ILC** | Idea provenance present? `✓` if seeded from an approved idea, else `—` | first producer (from idea handoff) |
| **PILC / ADLC / UXD / POLC** | Per-package progress: `—` (not started) · `wip` · `done` | that package, its own column only |
| **Dev (DWG)** | `—` (not generated) · `generated` · `external` (exported, see contract §12) | AI-DWG |
| **Created** | Date the project row was first written (ISO `YYYY-MM-DD`) | originator |
| **Updated** | Date of the most recent change to this row | last writer |

### 4.2 Status vocabulary

- Per-package columns use exactly: `—`, `wip`, `done`.
- `Dev (DWG)` uses exactly: `—`, `generated`, `external`.
- `Active` uses exactly: `★` or blank.

> Keep the vocabulary closed — downstream readers (PPM roll-up, FLO routing) parse these values. Do not invent new tokens without updating this spec.

---

## 5. Active-Project Pointer

- **Exactly one** project carries `★` in the `Active` column, mirrored in the `Active project:` header line.
- The default target of every per-project producer is the active project (contract §8 flow).
- **Switching** the active project updates both the header line and the `Active` column atomically (one edit). Only one row may hold `★` at a time — a writer that sets a new `★` must clear the previous one.
- **AI-PPM and AI-FLO do not change the pointer** — they read across all rows regardless of which is active (contract §8 exemption).

---

## 6. Lifecycle Operations

| Operation | Trigger | Effect |
|-----------|---------|--------|
| **Create registry** | first project originated in a workspace with no registry | write header + first row + set it ★ active |
| **Register project** | a new project is originated | append a row; optionally set it ★ active (ask the user) |
| **Update progress** | a package advances on a project | set its own column (`wip`/`done`) + bump `Updated` |
| **Switch active** | user/active-project trigger | move `★` to the chosen row + update header |
| **Mark dev generated** | AI-DWG generates a dev workspace | set `Dev (DWG)` = `generated` (or `external`) |
| **Regenerate registry** | registry missing/corrupt | rebuild by scanning `pdlc-ws/projects/*/` folders + their `*-state.md` markers |

---

## 7. Regeneration (Why It Holds No Authoritative State)

The registry can always be reconstructed:

1. Scan `pdlc-ws/projects/*/` for project folders.
2. For each, read the canonical Project ID from the per-project spine / `*-state.md` markers.
3. Derive each package column from the presence/stage of that package's `*-state.md`.
4. Derive `Dev (DWG)` from the presence of `{slug}-workspace/` (or a `devWorkspacePath` pointer for `external`).
5. Choose the active project (ask the user if ambiguous; default to the most recently updated).

Because every value is derivable, the registry is an **index**, not state — losing it is recoverable, never catastrophic.

---

## 8. Boundaries

1. **Not a state tier** — authoritative state is the per-project spine + `*-state.md` (contract §10).
2. **Not portfolio governance** — PPM produces portfolio output under `pdlc-ws/portfolio/`; it only *enriches* this index.
3. **Workspace-local** — does not travel with an exported project folder.
4. **One workspace, one registry** — in the single-family world. (A multi-family world makes the registry per-family with FLO aggregating across them — reserved, out of scope here.)

---

*Spec Version: 1.0.0 | Created: 2026-06-17 | Companion to OUTPUT_AND_STATE_CONTRACT.md | Authored under #persona-process-designer + #persona-cto-architect*
