<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package → ux/user-flows/ (UXD CLUSTER)

## Purpose

Carries **user flow documents** from the UX Design Package into the generated workspace. User flows describe multi-step interaction choreography — step sequences, decision points, error recovery, and cross-screen navigation that developers implement as multi-screen workflows.

**Output:** `{workspace-root}/ux/user-flows/` (one file per user flow)

**Condition:** Generate IF `uxd-state.md` is present AND the UXP contains user flow files.

**Cluster:** UX — belongs exclusively to the UXD input cluster.

**Type:** Reference document (NOT a steering file). Multi-step implementation blueprints.

---

## Source

**From:** AI-UXD → UXP, typically `05_User_Flows/` or `flows/`.

| UXP Document | What to Extract |
|---|---|
| `UF-01_*.md` through `UF-NN_*.md` | Per-flow interaction choreography |

---

## Transformation

**Copy with provenance** — reference documents. DWG copies each flow file verbatim with provenance front-matter.

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD — 05_User_Flows/{filename}"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

{verbatim user flow content from UXP}
```

---

## Transformation Rules

### Rule 1: Copy All Flow Files
Every user flow document is copied. No selective omission.

### Rule 2: Verbatim Content
Steps, decision points, error paths, and recovery patterns are copied exactly.

### Rule 3: Preserve Filenames
Keep original filenames. Developers reference flows by name.

### Rule 4: Skip If Absent
If UXP has no user flows, SKIP. Do NOT generate empty `ux/user-flows/` folder.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `uxd-to-wireframes.md` | Wireframes show screen detail; flows show the choreography between screens |
| `uxd-to-information-architecture.md` | Navigation structure defines possible paths; flows define intended paths |
| `polc-to-epics-backlog.md` | Flows often map 1:1 to epics/stories (one flow = one feature workflow) |

---

## Output Validation

- [ ] One file per UXP user flow in `ux/user-flows/`
- [ ] Content verbatim from UXP
- [ ] Filenames preserved
- [ ] Provenance front-matter on each file
