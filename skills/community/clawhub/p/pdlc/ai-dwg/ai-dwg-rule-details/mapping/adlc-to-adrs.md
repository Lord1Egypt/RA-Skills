<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Architecture Package → architecture/architecture-decision-records.md (ADLC CLUSTER)

## Purpose

Carries the **Architecture Decision Records (ADRs)** from the Architecture Package into the generated workspace as a reference document. Steering rules reference ADRs by number (ADR-001, ADR-004, etc.) but developers need the full rationale — options considered, decision drivers, and consequences — when questioning "why" behind a rule.

**Output:** `{workspace-root}/architecture/architecture-decision-records.md`

**Condition:** Generate IF `adlc-state.md` is present AND the AP contains ADR document(s).

**Cluster:** Tech — belongs exclusively to the ADLC input cluster.

**Type:** Reference document (NOT a steering file). Provides the "why" behind architecture rules that steering enforces as "what."

---

## Source

**From:** AI-ADLC → AP, typically `decisions/architecture-decision-records.md` or `adrs/` folder.

| AP Document | What to Extract |
|---|---|
| `architecture-decision-records.md` | Full ADR register: ID, title, status, context, decision, consequences |
| `adrs/ADR-*.md` (if split) | Individual ADR files — consolidate into single register |

---

## Transformation

**Copy with provenance** — reference document. DWG copies the ADR register verbatim and adds provenance front-matter.

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-ADLC — decisions/architecture-decision-records.md"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

{verbatim ADR content from AP}
```

If ADRs are split across multiple files, consolidate into a single document with clear ADR boundaries.

---

## Transformation Rules

### Rule 1: Verbatim Copy
Copy the full ADR content — all decisions, rationale, options, consequences. Do NOT paraphrase.

### Rule 2: Consolidate If Split
If AP has individual ADR files (`ADR-001.md`, `ADR-002.md`, etc.), merge them into one `architecture-decision-records.md` with clear `## ADR-NNN: Title` separators.

### Rule 3: Skip If Absent
If the AP does not contain ADRs, SKIP. Do NOT fabricate architectural decisions.

### Rule 4: Reference, Not Steering
This file answers "why." Steering files answer "what must be done." Both are needed; they serve different purposes.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `api-to-steering.md` | Steering references ADR IDs for API decisions — ADR doc has the full rationale |
| `security-to-steering.md` | Steering references ADR IDs for security decisions |
| `adlc-to-constraint-register.md` | Constraints and ADRs often cross-reference each other |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| AP has no ADRs | SKIP entirely |
| ADRs in ADLC state file but no standalone document | Extract from `adlc-state.md` ADR Register section |
| Some ADRs are "Superseded" or "Deprecated" | Include ALL — status field tells the reader which are active |

---

## Output Validation

- [ ] File exists at `architecture/architecture-decision-records.md`
- [ ] Content is verbatim from AP
- [ ] ADR IDs match those referenced in steering files
- [ ] Provenance front-matter present
- [ ] If consolidated from multiple files, each ADR clearly separated
