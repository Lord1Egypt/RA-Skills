<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: initiation-quality-agent
description: >
  Validates Project Initiation Package (PIP) completeness, phase-gate compliance,
  stakeholder coverage, and management register integrity after AI-PILC workflow completion.
generatedBy: AI-PILC
generatedVersion: "{version}"
source: ai-pilc-rules/core-workflow.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read"]
trigger: IQA__
tier: 1
type: process
---

# Initiation Quality Agent

## Purpose

Validates that the Project Initiation Package (PIP) produced by AI-PILC meets professional PMO quality standards. Checks deliverable completeness across all 16 stages, phase-gate compliance (no auto-progression without user approval), stakeholder coverage adequacy, management register integrity, and cross-reference consistency between artifacts.

## When to Invoke

Call this agent **after completing the AI-PILC workflow** — before handing the PIP to AI-ADLC or presenting it to the Steering Committee.

- **Trigger:** Type `IQA__` in the chat prompt
- **Cadence:** Once per PIP completion; optionally mid-workflow after PLANNING phase
- **Process point:** After Stage 16 (Package Assembly) or when the user says "the PIP is ready for review"

**Concrete examples:**
- "I've finished the project initiation" → call `IQA__` to validate the package
- "Is my PIP ready for the Steering Committee?" → call `IQA__` to check
- "We're about to hand off to architecture (AI-ADLC)" → call `IQA__` first
- "I completed the PLANNING phase and want a checkpoint" → call `IQA__` for a mid-workflow quality gate

## Consequences of Skipping

**Immediate impact:**
- Incomplete PIP handed to AI-ADLC → architecture built on incomplete foundations
- Missing stakeholders discovered mid-project → scope changes, rework, governance gaps
- Unlogged decisions → audit trail broken, rationale lost
- Gate violations undetected → workflow discipline erodes across future projects

**Accumulated debt (skipped across multiple projects):**
- Organization loses trust in the AI-PILC process ("it produces incomplete packages")
- AI-ADLC compensates by re-asking requirements → duplicated effort, conflicting artifacts
- Steering Committee receives packages of inconsistent quality → governance credibility drops
- Management registers become unreliable as source of truth

## Recovery

If you skipped `IQA__` and the PIP is already in use:

1. Run `IQA__` now — it checks the CURRENT state of all PIP artifacts
2. For each gap found:
   - **Missing deliverable:** Author it retroactively; mark as "post-initiation addition" in Decision Log
   - **Incomplete register:** Review `pilc-state.md` decision history; backfill entries
   - **Stakeholder gap:** Add to register; schedule catch-up engagement
   - **Cross-reference break:** Fix references; log correction in Change Log
3. If AI-ADLC has already started:
   - Communicate PIP updates to the architecture team
   - Flag any scope clarifications that may affect architecture decisions
4. Update `pilc-state.md` to reflect the quality review was performed post-completion

## Checks Performed

### Deliverable Completeness (C1–C4)

1. **C1 — Mandatory artifact presence:** Verify all 12 always-present files exist in the output folder (Requirement Intake Form, Feasibility Assessment, Business Case, Project Charter, Stakeholder Register, Scope Statement, Resource Plan, Risk Register, RACI Matrix, Kickoff Agenda, `pilc-state.md`, Package README).
2. **C2 — Conditional artifact presence:** If workflow depth ≥ Standard, verify Requirements Analysis Report exists. If clarification cycle executed, verify Clarification Questionnaire exists.
3. **C3 — Placeholder audit:** Scan all deliverables for unresolved `_[TBD]_` or `_[Pending]_` markers. Report count and location. Zero unresolved TBDs = pass; >0 = warn with list.
4. **C4 — State file completeness:** Verify `pilc-state.md` contains: Project ID, project name, current phase = Complete (or last completed phase if mid-workflow), all completed stages with timestamps, depth level, output structure choice.

### Gate Compliance (G1–G3)

5. **G1 — Gate log verification:** Cross-check `pilc-state.md` stage completion entries against Decision Log. Every stage completion should have a corresponding user-approval decision logged.
6. **G2 — Skip documentation:** If any stages were skipped, verify each has a Decision Log entry with rationale (D-xxx: "Stage {n} skipped — {reason}").
7. **G3 — Depth consistency:** Verify the declared depth level (Minimal/Standard/Comprehensive) is consistent with actual deliverable richness (e.g., a "Comprehensive" depth should not have 2-level WBS).

### Stakeholder Coverage (S1–S3)

8. **S1 — Stakeholder register populated:** Verify ≥3 stakeholders registered (minimum viable governance — Sponsor, PM, at least one SME or User).
9. **S2 — Power/Interest classification:** Every stakeholder has Power (H/M/L) and Interest (H/M/L) assigned. No blanks.
10. **S3 — RACI alignment:** Verify RACI Matrix roles map to registered stakeholders. Flag any role in RACI not present in Stakeholder Register (orphaned accountability).

### Management Register Integrity (R1–R4)

11. **R1 — Decision Log populated:** At minimum, D-001 (source acceptance) and one gate decision must exist. A PIP with zero decisions is invalid.
12. **R2 — Sequential numbering:** Verify register entries follow sequential numbering with phase prefix (`PILC-D-001`, `PILC-D-002`...) — no gaps, no duplicates.
13. **R3 — Cross-register consistency:** Assumptions referenced in Risk Register should appear in Assumptions & Dependencies register. Actions identified in any document should appear in Action Items.
14. **R4 — Spine marker presence:** If this is a chain execution (not standalone), verify `management_framework/MANAGEMENT_FRAMEWORK.md` spine marker file exists.

### Cross-Reference Consistency (X1–X2)

15. **X1 — Inter-artifact references:** Verify that references between documents resolve (e.g., Risk Register referencing "see Stakeholder Register for risk owner" → that stakeholder exists).
16. **X2 — Project ID consistency:** The Project ID in `pilc-state.md` must match the Project ID in Project Charter, Business Case header, and Package README.

## Output

- **If all checks pass:** Summary report:
  ```
  ✅ PIP Quality Check — PASS
  📦 {project_name} | Depth: {level} | Stages: {n}/16 complete
  📋 Deliverables: {n} present | Registers: {n} entries | Stakeholders: {n}
  🎯 Ready for AI-ADLC handoff / Steering Committee presentation.
  ```

- **If violations found:**
  - Per-check report: check ID, status (PASS/WARN/FAIL), finding, remediation suggestion
  - Summary score: `{passed}/{total} checks passed`
  - Compliance log entry appended to `.governance/compliance-log/events/{today-date}.jsonl`
  - Event type: `check`, agent: `initiation-quality-agent`, result: `pass|fail|warn`
  - Prioritized remediation list (FAIL items first, then WARN)

**Output location:** `.governance/compliance-log/events/` (if `.governance/` exists; otherwise inline report only)

## Related

- **Workflow source:** `ai-pilc-rules/core-workflow.md` (defines the 16 stages and gates)
- **Process overview:** `ai-pilc-rule-details/common/process-overview.md`
- **Content validation:** `ai-pilc-rule-details/common/content-validation.md`
- **Management framework:** `ai-pilc-rule-details/templates/management-framework.md`
- **Contract:** Agent Governance Contract §4, §5
- **Successor dependency:** AI-ADLC reads `pilc-state.md` — quality of that file directly impacts architecture phase
- **Complementary agents:** `session-discipline-agent` (AI-GCE) checks process methodology; this agent checks PIP artifact quality
