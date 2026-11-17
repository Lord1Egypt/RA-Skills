<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package → ux/personas/ (UXD CLUSTER)

## Purpose

Carries **persona documents** from the UX Design Package into the generated workspace. Personas provide user context for implementation decisions — role behaviors, device preferences, accessibility needs, and usage patterns that inform feature implementation.

**Output:** `{workspace-root}/ux/personas/` (one file per persona)

**Condition:** Generate IF `uxd-state.md` is present AND the UXP contains persona files.

**Cluster:** UX — belongs exclusively to the UXD input cluster.

**Type:** Reference document (NOT a steering file). User context for implementation decisions.

---

## Source

**From:** AI-UXD → UXP, typically `02_Personas/` or `personas/`.

| UXP Document | What to Extract |
|---|---|
| `P-01_*.md` through `P-NN_*.md` | Per-persona profiles |

---

## Transformation

**Copy with provenance** — reference documents. DWG copies each persona file verbatim with provenance front-matter.

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD — 02_Personas/{filename}"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

{verbatim persona content from UXP}
```

---

## Transformation Rules

### Rule 1: Copy All Persona Files
Every persona document is copied.

### Rule 2: Verbatim Content
Role descriptions, behaviors, accessibility needs, and device preferences are copied exactly.

### Rule 3: Preserve Filenames
Keep original filenames.

### Rule 4: Skip If Absent
If UXP has no personas, SKIP. Do NOT generate empty `ux/personas/` folder.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `uxd-to-wireframes.md` | Wireframes reference personas by role (screens serve specific personas) |
| `uxd-to-user-flows.md` | Flows are authored for specific persona journeys |
| `polc-uxd-to-vision-document.md` | Vision document references key personas |

---

## Output Validation

- [ ] One file per UXP persona in `ux/personas/`
- [ ] Content verbatim from UXP
- [ ] Filenames preserved
- [ ] Provenance front-matter on each file
