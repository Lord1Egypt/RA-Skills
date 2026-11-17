<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package → ux/wireframes/ (UXD CLUSTER)

## Purpose

Carries **per-screen wireframe specifications** from the UX Design Package into the generated workspace. These are the implementation blueprints developers code from — layout grids, component placement, responsive breakpoints, interaction states, and error patterns per screen.

**Output:** `{workspace-root}/ux/wireframes/` (one file per wireframe specification)

**Condition:** Generate IF `uxd-state.md` is present AND the UXP contains wireframe specification files.

**Cluster:** UX — belongs exclusively to the UXD input cluster.

**Type:** Reference document (NOT a steering file). Per-screen implementation blueprints.

---

## Source

**From:** AI-UXD → UXP, typically `06_Wireframe_Specifications/` or `wireframes/`.

| UXP Document | What to Extract |
|---|---|
| `WF-01_*.md` through `WF-NN_*.md` | Per-screen wireframe specs |
| `Screen-Inventory.md` (if present) | Screen index/overview |

---

## Transformation

**Copy with provenance** — reference documents. DWG copies each wireframe file verbatim and adds provenance front-matter.

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD — 06_Wireframe_Specifications/{filename}"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

{verbatim wireframe specification content from UXP}
```

---

## Transformation Rules

### Rule 1: Copy All Wireframe Files
Every `WF-*` file in the UXP wireframes folder is copied. No selective omission.

### Rule 2: Verbatim Content
Do NOT paraphrase, summarize, or restructure wireframe content. Layout specs, component lists, responsive rules, and interaction states are copied exactly.

### Rule 3: Preserve Filenames
Keep original filenames (e.g., `WF-01_Employee-Onboarding.md`). Developers reference these by name.

### Rule 4: Include Screen Inventory
If a `Screen-Inventory.md` or equivalent index exists, copy it too.

### Rule 5: Skip If Absent
If UXP has no wireframe specifications, SKIP. Do NOT generate empty `ux/wireframes/` folder.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `uxd-to-design-system.md` | Design system steering defines tokens/components; wireframes show WHERE they're used per screen |
| `uxd-to-user-flows.md` | User flows show multi-screen choreography; wireframes show individual screen detail |
| `uxd-to-information-architecture.md` | Navigation structure defines routes; wireframes show screen content at each route |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| UXP has no wireframes | SKIP — no empty folder |
| Wireframes reference components not in design system | Copy anyway — flag inconsistency in validation |
| Wireframes are images only (no markdown) | SKIP — DWG handles markdown artifacts only |

---

## Output Validation

- [ ] One file per UXP wireframe specification in `ux/wireframes/`
- [ ] Content verbatim from UXP
- [ ] Filenames preserved
- [ ] Provenance front-matter on each file
- [ ] Screen Inventory included if present
