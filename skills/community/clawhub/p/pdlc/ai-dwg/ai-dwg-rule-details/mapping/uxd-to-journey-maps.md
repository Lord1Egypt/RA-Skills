<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package → ux/journey-maps/ (UXD CLUSTER)

## Purpose

Carries **journey map documents** from the UX Design Package into the generated workspace. Journey maps provide end-to-end experience context across touchpoints — they inform feature integration decisions and help developers understand how individual screens fit into the broader user experience.

**Output:** `{workspace-root}/ux/journey-maps/` (one file per journey map)

**Condition:** Generate IF `uxd-state.md` is present AND the UXP contains journey map files.

**Cluster:** UX — belongs exclusively to the UXD input cluster.

**Type:** Reference document (NOT a steering file). End-to-end experience context.

---

## Source

**From:** AI-UXD → UXP, typically `03_Journey_Maps/` or `journeys/`.

| UXP Document | What to Extract |
|---|---|
| `JM-01_*.md` through `JM-NN_*.md` | Per-journey experience maps |
| Service blueprints (if present) | Cross-channel service maps |

---

## Transformation

**Copy with provenance** — reference documents. DWG copies each journey map file verbatim with provenance front-matter.

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD — 03_Journey_Maps/{filename}"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

{verbatim journey map content from UXP}
```

---

## Transformation Rules

### Rule 1: Copy All Journey Map Files
Every journey map and service blueprint is copied.

### Rule 2: Verbatim Content
Touchpoints, pain points, opportunities, and emotional states are copied exactly.

### Rule 3: Preserve Filenames
Keep original filenames.

### Rule 4: Skip If Absent
If UXP has no journey maps, SKIP. Do NOT generate empty `ux/journey-maps/` folder.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `uxd-to-personas.md` | Journey maps are authored for specific personas |
| `uxd-to-user-flows.md` | Flows detail the interaction; journeys show the broader experience context |
| `uxd-to-wireframes.md` | Wireframes implement touchpoints identified in journey maps |

---

## Output Validation

- [ ] One file per UXP journey map in `ux/journey-maps/`
- [ ] Content verbatim from UXP
- [ ] Filenames preserved
- [ ] Provenance front-matter on each file
