<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Product Backlog Package (AI-POLC) → traceability-matrix.md (POLC CLUSTER)

## Purpose

Transforms the traceability linkage produced by AI-POLC (`governance/traceability.md`) into a living **traceability matrix** seed in the destination workspace. The matrix threads business intent → goal → epic → story → release so that AI-DLC v1 (during build) and AI-GCE (during enforcement) can verify that every unit of work traces to a justified product reason, and that no requirement is orphaned.

**Output:** `{workspace-root}/traceability-matrix.md`

**Condition:** Generate IF `polc-state.md` is present AND the PBP contains a traceability artefact (`governance/traceability.md` or equivalent). If POLC is present but no traceability artefact exists, generate the matrix scaffold with a single seeded row per epic and flag the gap.

**Cluster:** Product — belongs exclusively to the POLC input cluster.

---

## MANDATORY: Stage Sub-Role — Audit Specialist

During THIS activity, ALSO adopt the mindset of an **Audit Specialist**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in chains of evidence — every row must link a downstream artefact back to an upstream justification
- An orphaned story (no parent epic/goal) is a finding, not a row to silently drop
- Preserve the POLC linkage IDs verbatim — they are the correlation keys AI-GCE will audit against
- The matrix is a control, not documentation — it must be machine-checkable (stable IDs, one relationship per row)

### Anti-Patterns for This Activity
- Do NOT invent linkages POLC did not assert — if an epic has no parent goal in the PBP, mark it `UNLINKED` and flag
- Do NOT renumber or re-key POLC's epic/story IDs — copy them exactly
- Do NOT collapse many-to-many links into one row — each intent↔epic↔story↔release edge is its own row

---

## Source Inputs

**Primary source:** AI-POLC → Product Backlog Package (PBP), accessed via `polc-state.md` marker.

| PBP Document | What to Extract | Maps to Matrix Column |
|---|---|---|
| `governance/traceability.md` | Intent→epic→release linkage table | All matrix rows (primary) |
| `foundation/product-vision.md` | Business goals + goal IDs | `Goal` column |
| `strategy/epic-decomposition.md` | Epic IDs + parent goal references | `Epic` column |
| `strategy/release-slicing.md` | Release/increment groupings | `Release` column |
| `tier2/story-elaboration.md` (if present) | Story IDs under each epic | `Story` column |

### `polc-state.md` Fields Used

| Field | Used For |
|-------|----------|
| `Project ID` | Stamped in matrix front-matter as correlation key |
| `Completed Stages` | Confirms governance/traceability stage ran (expect Phase 3 complete) |
| `Depth` | Minimal → goal↔epic only; Standard/Comprehensive → full intent↔epic↔story↔release |

---

## Target Structure: traceability-matrix.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-POLC — governance/traceability.md"
generatedOn: "{generation-date}"
ownership: hybrid
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-POLC Traceability | date: {generation-date} -->

# Traceability Matrix

> Every build artefact MUST trace to a row here. Unlinked work is a governance finding.
> Maintained forward by AI-DLC v1 (adds implementation refs) and audited by AI-GCE.

## Forward Trace (Intent → Delivery)

| Trace ID | Business Intent / Goal | Epic | Story | Release | Status |
|----------|------------------------|------|-------|---------|--------|
| {TR-01} | {goal-id}: {goal} | {epic-id}: {epic} | {story-id}: {story} | {release} | {planned/in-progress/done} |
| ... | ... | ... | ... | ... | ... |

## Unlinked Items (Findings — must be resolved)
<!-- begin: PBP-sourced findings -->
| Item | Type | Why Unlinked | Suggested Parent |
|------|------|--------------|------------------|
| {id} | {epic/story} | {no parent goal in PBP} | {suggestion or "ask PO"} |
<!-- end: PBP-sourced findings -->

## Coverage Summary
- Goals with ≥1 epic: {n}/{total}
- Epics with ≥1 story: {n}/{total}
- Stories assigned to a release: {n}/{total}
- **Orphan count: {n}** (target: 0)
```

---

## Transformation Rules

### Rule 1: Linkage IDs Are VERBATIM
Copy POLC's goal/epic/story/release IDs exactly. AI-GCE correlates against these.

### Rule 2: One Edge Per Row
Each row expresses a single forward path. A story serving two epics produces two rows.

### Rule 3: Orphans Are Findings, Not Omissions
Any epic without a parent goal, or story without a parent epic, goes in the **Unlinked Items** table with a suggested parent — never silently dropped.

### Rule 4: The Matrix Is Append-Forward
AI-DLC v1 adds implementation/commit references downstream; AI-GCE audits. The seed must leave the `Status` column writable and not lock rows.

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| POLC present, no traceability artefact | Generate scaffold with one row per epic (goal↔epic only); flag: "PBP lacks traceability.md — matrix seeded at epic level only" |
| Tier 2 stories not elaborated (chain mode) | Leave `Story` column as `{deferred-to-AI-DLC v1}`; matrix still traces goal↔epic↔release |
| Goal referenced by epic but absent from vision | Unlinked finding: "epic references missing goal {id}" |
| Depth = Minimal | Produce goal↔epic columns only; omit Story/Release columns |

---

## Output Validation

- [ ] All POLC linkage IDs copied verbatim (no renumbering)
- [ ] One forward edge per row
- [ ] Orphans captured in Unlinked Items table (not dropped)
- [ ] Coverage summary computed (orphan count present)
- [ ] Status column left writable for downstream append
- [ ] Provenance front-matter + projectId present
