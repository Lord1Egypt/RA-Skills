<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Product Backlog Package (AI-POLC) → backlog/epics-and-backlog.md + backlog/epics/ (POLC CLUSTER)

## Purpose

Transforms the epic decomposition produced by AI-POLC (`strategy/epic-decomposition.md`) into a **backlog scaffold** in the destination workspace: an epic overview document plus a `backlog/epics/` folder structure with full story files when Tier 2 is available. This gives the build workspace a ready-made, prioritized backbone of work — goals decomposed into epics with acceptance criteria and a stable order — instead of starting from an empty backlog.

**Output:**
- `{workspace-root}/backlog/epics-and-backlog.md` (the epic overview + prioritized order)
- `{workspace-root}/backlog/epics/EPIC-{id}-{slug}.md` (one per epic)
- `{workspace-root}/backlog/epics/EPIC-{id}_stories/` (full story files, IF Tier 2)

**Condition:** Generate IF `polc-state.md` is present AND the PBP contains epic decomposition.

**Cluster:** Product — belongs exclusively to the POLC input cluster.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS activity, ALSO adopt the mindset of a **Business Analyst** (with a resource-planning lens for ordering). ADDS a thinking dimension — does NOT replace your primary role.

### Behavioral Shifts
- Epics are containers of value, not feature buckets — preserve the goal each epic serves
- Acceptance criteria at the epic level define "done for the epic" — copy them; do not soften
- Prioritization order is a decision, not a suggestion — preserve WSJF/MoSCoW rank verbatim
- The scaffold seeds work; it does NOT pre-write stories AI-DLC v1 should elaborate

### Anti-Patterns for This Activity
- Do NOT re-prioritize epics — copy POLC's order exactly
- Do NOT invent epics not in the PBP
- Do NOT pre-decompose epics into stories unless POLC's Tier 2 already did (then carry them; otherwise leave a `## Stories (elaborated by AI-DLC v1)` placeholder)

---

## Source Inputs

**Primary source:** AI-POLC → PBP, via `polc-state.md` marker.

| PBP Document | What to Extract | Maps to |
|---|---|---|
| `strategy/epic-decomposition.md` | Epic IDs, titles, parent goal, acceptance criteria | Epic stubs + overview rows |
| `strategy/value-prioritization.md` | WSJF/MoSCoW rank + rationale | Prioritized Order section |
| `strategy/release-slicing.md` | MVP/MMP groupings | Release column |
| `tier2/story-elaboration.md` (if present) | Elaborated stories per epic | Epic stub `## Stories` section |

---

## Target Structure

### backlog/epics-and-backlog.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-POLC — strategy/epic-decomposition.md + value-prioritization.md"
generatedOn: "{generation-date}"
ownership: hybrid
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-POLC Epic Decomposition | date: {generation-date} -->

# Epics & Backlog

> Prioritized epic backbone seeded from the Product Backlog Package.
> AI-DLC v1 elaborates stories into `backlog/epics/EPIC-*_stories/`; order is POLC-authoritative.

## Prioritized Order
<!-- begin: PBP-sourced -->
| Rank | Epic ID | Epic | Parent Goal | Priority Model | Release | Stub |
|------|---------|------|-------------|----------------|---------|------|
| 1 | {epic-id} | {title} | {goal-id} | {WSJF=.. / Must} | {MVP} | `backlog/epics/EPIC-{id}-{slug}.md` |
| ... | ... | ... | ... | ... | ... | ... |
<!-- end: PBP-sourced -->

## Prioritization Rationale
<!-- begin: PBP-sourced -->
{verbatim rationale from value-prioritization.md — why this order}
<!-- end: PBP-sourced -->
```

### backlog/epics/EPIC-{id}-{slug}.md (one per epic)

```markdown
---
generatedBy: AI-DWG
source: "AI-POLC — epic-decomposition.md"
ownership: hybrid
epicId: "{epic-id}"
parentGoal: "{goal-id}"
---

# EPIC-{id}: {title}

**Parent Goal:** {goal-id} — {goal}
**Priority:** {rank} ({model})  ·  **Release:** {release}

## Epic Acceptance Criteria
<!-- begin: PBP-sourced -->
- {criterion 1}
- {criterion 2}
<!-- end: PBP-sourced -->

## Stories
<!-- If POLC Tier 2, stories are in backlog/epics/EPIC-{id}_stories/ -->
{IF Tier 2: "See `EPIC-{id}_stories/` for full elaborated stories."}
{IF Tier 1 only: "_Stories elaborated by AI-DLC v1 during build._"}
```

### backlog/epics/EPIC-{id}_stories/ (IF Tier 2 — full story files)

When POLC Tier 2 elaboration is complete, DWG copies the **full story files** into this folder. These are the acceptance criteria developers build against.

```markdown
backlog/epics/EPIC-001_stories/
├── US-001_{slug}.md
├── US-002_{slug}.md
└── US-00N_{slug}.md
```

Each story file is copied from the PBP with provenance front-matter added:

```markdown
---
generatedBy: AI-DWG
source: "AI-POLC — tier2/story-elaboration.md"
ownership: generated
epicId: "{epic-id}"
storyId: "{story-id}"
projectId: "{project-id}"
generatedOn: "{generation-date}"
---

{full story content from PBP — verbatim copy including G/W/T ACs}
```

**Generation rules for story files:**
- Copy verbatim — do NOT paraphrase, summarize, or restructure
- Preserve all Given/When/Then acceptance criteria exactly as written
- One file per story (same filename as in PBP if available, else `US-{NNN}_{slug}.md`)
- Add provenance front-matter only — no other modifications to content

---

## Transformation Rules

### Rule 1: Order Is VERBATIM
Copy POLC's prioritization rank exactly. Never re-rank.

### Rule 2: One Stub Per Epic
Every epic in the PBP gets exactly one `backlog/EPIC-*.md`. No epic dropped, none invented.

### Rule 3: Acceptance Criteria Copied, Not Paraphrased
Epic-level acceptance criteria are quoted verbatim.

### Rule 4: Full Story Files Copied When Tier 2 Available
When POLC Tier 2 story elaboration is complete (detected via `polc-state.md` status or presence of `tier2/story-elaboration.md`):
- Copy ALL elaborated story files into `backlog/epics/EPIC-{id}_stories/`
- Add provenance front-matter to each file
- Generate `backlog/README.md` confirming stories are present
- Cross-link from epic stubs to their stories folder

When Tier 2 is NOT available (Tier 1 only):
- Leave epic stubs with placeholder: "_Stories elaborated by AI-DLC v1 during build._"
- Do NOT generate empty `_stories/` folders
- `backlog/user-stories.md` is NOT generated (no Tier 2 content to index)

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `polc-to-traceability.md` | Epic IDs here MUST match the traceability matrix `Epic` column. |
| `polc-to-user-stories.md` | Story stubs/specs land under each epic stub when Tier 2 stories exist. |
| `quality-to-dod.md` | Epic acceptance criteria reference the same DoD bar. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| POLC present, no epic decomposition | Skip backlog seed; flag: "PBP has no epics — backlog left empty for AI-DLC v1" |
| Epics have no rank | Use document order; mark `Priority Model = unranked (PO to confirm)` |
| Tier 2 stories present | Copy full story files into `backlog/epics/EPIC-{id}_stories/`; populate `backlog/user-stories.md` index |
| Tier 1 only (no story elaboration) | Leave epic stub placeholders; do NOT generate empty `_stories/` folders or `user-stories.md` |
| Epic references missing goal | Keep epic; flag goal gap (also surfaces in traceability matrix) |
| Story file has no structured G/W/T | Copy verbatim anyway — format is POLC's responsibility, not DWG's |

---

## Output Validation

- [ ] One `backlog/epics/EPIC-*.md` per PBP epic (exhaustive)
- [ ] Prioritized order matches POLC rank verbatim
- [ ] Epic acceptance criteria copied verbatim
- [ ] Epic IDs consistent with traceability matrix
- [ ] IF Tier 2: full story files present in `backlog/epics/EPIC-{id}_stories/`
- [ ] IF Tier 2: story content copied verbatim (no paraphrase)
- [ ] IF Tier 1: stories placeholder present, no empty `_stories/` folders
- [ ] Provenance front-matter + projectId present on all generated files
- [ ] All outputs located under `backlog/` (nothing at workspace root)
