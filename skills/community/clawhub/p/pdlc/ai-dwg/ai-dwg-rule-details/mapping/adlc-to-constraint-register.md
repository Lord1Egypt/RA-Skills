<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Architecture Package → architecture/constraint-register.md (ADLC CLUSTER)

## Purpose

Carries the **full constraint register** from the Architecture Package into the generated workspace as a reference document. Steering rules reference individual constraints by ID (C-01, C-03, etc.) but developers need the complete set for novel decisions not yet covered by existing steering.

**Output:** `{workspace-root}/architecture/constraint-register.md`

**Condition:** Generate IF `adlc-state.md` is present AND the AP contains a constraint register document.

**Cluster:** Tech — belongs exclusively to the ADLC input cluster.

**Type:** Reference document (NOT a steering file). Does not influence AI behavior per code change. Provides human-readable lookup material.

---

## Source

**From:** AI-ADLC → AP, typically `constraints/constraint-register.md` or `foundation/constraint-register.md`.

| AP Document | What to Extract |
|---|---|
| `constraint-register.md` | Full register: hard constraints, derived constraints, IDs, rationale, source |

---

## Transformation

**Copy with provenance** — this is a reference document. DWG copies the constraint register verbatim and adds provenance front-matter. No distillation, no summarization.

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-ADLC — constraints/constraint-register.md"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

{verbatim constraint register content from AP}
```

---

## Transformation Rules

### Rule 1: Verbatim Copy
Copy the full document — all constraints, IDs, rationale, sources. Do NOT paraphrase or summarize.

### Rule 2: Provenance Only
The only DWG addition is the front-matter metadata block. No other modifications to content.

### Rule 3: Skip If Absent
If the AP does not contain a constraint register, SKIP this output entirely. Do NOT fabricate constraints.

### Rule 4: Reference, Not Steering
This file is for human lookup. It does NOT generate AI steering rules — those are handled by existing mappings (`security-to-steering.md`, `api-to-steering.md`, etc.) which distill constraints into enforceable rules.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `security-to-steering.md` | Distills security constraints into `security-rules.md` steering — constraint-register is the full reference behind those rules |
| `api-to-steering.md` | Distills API constraints into `api-standards.md` — register has the full rationale |
| `data-to-steering.md` | Distills data constraints into `database-rules.md` — register has the full set |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| AP has no constraint register | SKIP entirely — no empty file generated |
| Constraints split across multiple AP files | Concatenate all constraint sources into one register (note sources in provenance) |
| Register references ADRs by number | Ensure `architecture/architecture-decision-records.md` is also generated (see `adlc-to-adrs.md`) |

---

## Output Validation

- [ ] File exists at `architecture/constraint-register.md`
- [ ] Content is verbatim from AP (no paraphrase)
- [ ] Provenance front-matter present with correct source path
- [ ] Constraint IDs match those referenced in steering files
