<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Projects Registry Template (AI-PILC)

| Field | Value |
|-------|-------|
| **Artifact** | `pdlc-ws/projects/PROJECTS.md` (workspace-level registry + active pointer) |
| **Ownership** | Shared, create-if-absent — every per-project producer maintains it; AI-PPM enriches |
| **Spec Reference** | `contracts/PROJECTS_REGISTRY_SPEC.md` |
| **Not a state tier** | Regenerable index; authoritative state lives in the per-project spine + `*-state.md` |

---

## Behavior: Create-if-Absent / Append-if-Exists

```
1. Look for pdlc-ws/projects/PROJECTS.md.
2. IF absent → CREATE from the template below + add this project's row + set it ★ active.
3. IF present → APPEND this project's row if missing, else UPDATE this project's own row
                (own columns only); never delete or rewrite another project's row.
4. On active-project switch → move the ★ to the chosen row + update the header line
                              (only one ★ at a time).
```

---

## Registry File Template

> This is `pdlc-ws/projects/PROJECTS.md`. Status vocabulary is closed (downstream readers parse it):
> per-package columns = `—` / `wip` / `done`; Dev (DWG) = `—` / `generated` / `external`; Active = `★` / blank.

```markdown
<!-- Projects registry | regenerable index — not a state tier | spec: PROJECTS_REGISTRY_SPEC.md -->

# Projects Registry

Active project: ★ {project_id}

| Project ID | Folder | Active | ILC | PILC | ADLC | UXD | POLC | Dev (DWG) | Created | Updated |
|------------|--------|:------:|-----|------|------|-----|------|-----------|---------|---------|
| {project_id} | PRJ-{ABBREV}-{slug} | ★ | {✓ or —} | wip | — | — | — | — | {date} | {date} |
```

### Field notes

| Column | AI-PILC writes |
|--------|----------------|
| Project ID | the canonical `PRJ-{ABBREV}-{YYYY}-{NNN}` minted at Stage 1 (immutable) |
| Folder | `PRJ-{ABBREV}-{slug}` (relative to `projects/`) |
| Active | `★` if this is the active project, else blank |
| ILC | `✓` if seeded from an approved idea (`ilc-state.md` detected), else `—` |
| PILC | `wip` while running, `done` when the PIP is complete |
| ADLC / UXD / POLC / Dev (DWG) | `—` (AI-PILC does not write peer columns; each package owns its own) |
| Created / Updated | ISO `YYYY-MM-DD`; set Created on first write, bump Updated each change |

---

## Rules

1. AI-PILC writes **only** the Project ID, Folder, Active (if it owns the switch), ILC, its own **PILC** column, and Created/Updated. It never fills peer-package columns.
2. The registry is **workspace-local** — it is not part of a portable project bundle; an exported project folder leaves its row behind.
3. If the registry is missing/corrupt, it can be **regenerated** by scanning `pdlc-ws/projects/*/` and the per-project `*-state.md` markers (`PROJECTS_REGISTRY_SPEC.md` §7).
4. Templates stay 100% generic — `{placeholder}` syntax only.

---

*Template Version: 1.0.0 | Spec: PROJECTS_REGISTRY_SPEC.md | Package: AI-PILC*
