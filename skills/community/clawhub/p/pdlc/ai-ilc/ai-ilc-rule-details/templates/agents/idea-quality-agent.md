<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: idea-quality-agent
description: >
  Validates Idea Brief completeness, evaluation scoring integrity, routing decision quality,
  and governance record compliance after AI-ILC workflow completion.
generatedBy: AI-ILC
generatedVersion: "{version}"
source: ai-ilc-rules/core-workflow.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read"]
trigger: IQC__
tier: 1
type: audit
---

# Idea Quality Agent

## Purpose

Validates that the output produced by AI-ILC (Approved Idea Brief, Feature Brief, or Change Request Brief) meets professional innovation-governance standards. Checks brief completeness, evaluation scoring integrity, routing decision rationale, and management register entries — before the idea proceeds to its next destination (AI-PILC, AI-POLC, or AI-DLC v1).

## When to Invoke

Call this agent **after completing the AI-ILC workflow** — before handing the idea brief to its next destination.

- **Trigger:** Type `IQC__` in the chat prompt
- **Cadence:** Once per idea completion (after Stage 6 — Route & Handoff)
- **Process point:** After the routing decision is made and the handoff brief is assembled

**Concrete examples:**
- "I've finished evaluating this idea" → call `IQC__` to validate the output
- "Is this idea brief ready for AI-PILC?" → call `IQC__` to check
- "We're about to hand off to the project initiation phase" → call `IQC__` first
- "The idea was approved — validate before routing" → call `IQC__`

## Consequences of Skipping

**Immediate impact:**
- Incomplete idea brief handed to AI-PILC → project initiated on weak foundations
- Missing evaluation scores → decision not defensible (why was this approved over other ideas?)
- Routing decision without rationale → downstream package confusion (why did it come here?)
- Unlogged governance decisions → audit trail gap at the very start of the lifecycle

**Accumulated debt (skipped across multiple ideas):**
- Portfolio funnel loses credibility ("ideas just get approved without proper scoring")
- AI-PPM can't prioritize reliably (missing scoring data)
- Rejected ideas lack documented rationale → same ideas resurface
- Organization can't learn from idea-stage decisions (no lessons captured)

## Recovery

If you skipped `IQC__` and the idea is already in the next stage:

1. Run `IQC__` now — it checks the CURRENT state of all ILC artifacts
2. For each gap found:
   - **Missing brief section:** Backfill from `ilc-state.md` history and original input
   - **Scoring gap:** Re-run evaluation criteria against the shaped idea; record scores retroactively
   - **Routing rationale missing:** Document why this route was chosen, mark as "retrospective"
   - **Register gap:** Backfill governance entries from `ilc-state.md` decision trail
3. If AI-PILC has already started:
   - Communicate any clarifications to the initiation workflow
   - Update the idea brief with missing context
4. Update `ilc-state.md` to reflect the quality review was performed post-completion

## Checks Performed

### Brief Completeness (C1–C4)

1. **C1 — Output artifact exists:** Verify the appropriate brief exists based on routing decision:
   - Route = `project` → Approved Idea Brief present
   - Route = `feature` → Feature Brief present
   - Route = `change` → Change Request Brief present
   - Route = `park`/`reject` → Decision Record present
2. **C2 — Required sections populated:** Verify the brief contains all mandatory sections (Problem Statement, Proposed Solution, Scope Boundary, Dependencies, Success Criteria, Risks). No section may be empty or placeholder-only.
3. **C3 — State file completeness:** Verify `ilc-state.md` contains: Idea title, status (Complete/Approved/Rejected/Parked), route decision, scoring results, all stage completions with timestamps.
4. **C4 — Placeholder audit:** Scan brief for unresolved `{placeholder}`, `_[TBD]_`, or `_[Pending]_` markers. Zero unresolved = pass; >0 = warn with list.

### Evaluation Integrity (E1–E3)

5. **E1 — Scoring completeness:** Verify all evaluation dimensions have been scored (per the scoring model used — at minimum: strategic alignment, feasibility, value/impact, urgency).
6. **E2 — Scoring justification:** Each score dimension has a one-line rationale (not just a number). A score without rationale is not defensible.
7. **E3 — Go/No-Go decision recorded:** The approval/rejection decision exists as a formal entry with: decision (approve/reject/park/defer), rationale, conditions (if any), and decision authority.

### Routing Quality (R1–R3)

8. **R1 — Route field present:** `ilc-state.md` contains a `Route:` field with one of: `project`, `feature`, `change`, `park`, `reject`.
9. **R2 — Route rationale documented:** A Decision Record entry explains WHY this route was chosen (e.g., "Route: project because scope exceeds feature-level and requires dedicated resources").
10. **R3 — Handoff context sufficient:** The brief contains enough context for the receiving package to start without asking "what is this about?" — minimum: problem, scope, constraints, dependencies.

### Governance Records (G1–G3)

11. **G1 — Decision Log populated:** At minimum, the Go/No-Go decision must be logged. An idea with zero decision entries is invalid.
12. **G2 — Sequential numbering:** Register entries follow `ILC-D-{NNN}` format (if governance spine mode) or sequential numbering (standalone). No gaps, no duplicates.
13. **G3 — Spine marker awareness:** If `management_framework/MANAGEMENT_FRAMEWORK.md` exists, verify ILC entries use `ILC-*` phase prefix. If standalone, verify entries exist in local output.

## Output

- **If all checks pass:** Summary report:
  ```
  ✅ Idea Quality Check — PASS
  💡 {idea_title} | Route: {route} | Score: {composite_score}
  📋 Brief: complete | Scoring: {n} dimensions | Governance: {n} entries
  🎯 Ready for handoff to {destination}.
  ```

- **If violations found:**
  - Per-check report: check ID, status (PASS/WARN/FAIL), finding, remediation suggestion
  - Summary score: `{passed}/{total} checks passed`
  - Compliance log entry appended to `.governance/compliance-log/events/{today-date}.jsonl`
  - Event type: `check`, agent: `idea-quality-agent`, result: `pass|fail|warn`
  - Prioritized remediation list (FAIL items first, then WARN)

**Output location:** `.governance/compliance-log/events/` (if `.governance/` exists; otherwise inline report only)

## Related

- **Workflow source:** `ai-ilc-rules/core-workflow.md` (defines the 6 stages and gates)
- **Process overview:** `ai-ilc-rule-details/common/process-overview.md`
- **Content validation:** `ai-ilc-rule-details/common/content-validation.md`
- **Templates:** `ai-ilc-rule-details/templates/` (brief templates, decision record)
- **Contract:** Agent Governance Contract §4, §5, §8
- **Successor dependency:** AI-PILC reads the Approved Idea Brief; AI-POLC reads the Feature Brief — quality of the brief directly impacts downstream
- **Complementary agents:** `initiation-quality-agent` (AI-PILC) checks PIP quality; this agent checks what feeds into PILC
