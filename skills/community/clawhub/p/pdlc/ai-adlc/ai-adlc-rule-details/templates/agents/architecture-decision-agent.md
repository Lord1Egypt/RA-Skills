<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: architecture-decision-agent
description: >
  Validates Architecture Package (AP) quality — ADR completeness, decision traceability,
  C4 level consistency, cross-reference integrity, and extension compliance after AI-ADLC workflow completion.
generatedBy: AI-ADLC
generatedVersion: "{version}"
source: ai-adlc-rules/core-workflow.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read"]
trigger: ADA__
tier: 1
type: process
---

# Architecture Decision Agent

## Purpose

Validates that the Architecture Package (AP) produced by AI-ADLC meets professional architecture quality standards. Checks ADR completeness and format compliance, decision traceability from requirements to implementation choices, C4 model level consistency (L1→L2→L3 progression), cross-reference integrity between architecture documents, extension rule enforcement, and state file completeness for downstream consumption by AI-DWG.

## When to Invoke

Call this agent **after completing the AI-ADLC workflow** — before handing the AP to AI-DWG or presenting it to the development team.

- **Trigger:** Type `ADA__` in the chat prompt
- **Cadence:** Once per AP completion; optionally mid-workflow after DECISIONS phase
- **Process point:** After Stage 13 (Package Assembly) or when the user says "the architecture is ready for review"

**Concrete examples:**
- "I've finished the architecture design" → call `ADA__` to validate the package
- "Is my AP ready for AI-DWG?" → call `ADA__` to check
- "We're about to hand off to workspace generation" → call `ADA__` first
- "I completed the DECISIONS phase and want a checkpoint" → call `ADA__` for a mid-workflow quality gate
- "The team wants to review the architecture before we build" → call `ADA__` to ensure presentation quality

## Consequences of Skipping

**Immediate impact:**
- Incomplete AP handed to AI-DWG → workspace generated from inconsistent architecture
- Missing ADRs → technology decisions undocumented, rationale lost for future maintainers
- C4 level misalignment → components reference containers that don't exist, broken module mapping
- State file gaps → AI-DWG can't detect extensions or constraints, produces incomplete steering

**Accumulated debt (skipped across multiple projects):**
- Architecture packages become inconsistent across projects — no reliable quality bar
- AI-DWG compensates by guessing missing context → steering files drift from actual architecture
- Development teams receive architecture docs with broken cross-references → trust in the process erodes
- ADR trail becomes unreliable — decisions made but not recorded, or records contradict each other
- Extension rules activated but not enforced → architectural integrity degrades silently

## Recovery

If you skipped `ADA__` and the AP is already in use:

1. Run `ADA__` now — it checks the CURRENT state of all AP artifacts
2. For each gap found:
   - **Missing ADR:** Author it retroactively; capture the decision context from Architecture Workbook or conversation history; log as post-assembly addition in Change Log
   - **C4 inconsistency:** Update the affected level document to align references; verify container/component naming matches
   - **Cross-reference break:** Fix references; log correction in Change Log
   - **State file gap:** Update `adlc-state.md` with missing fields (extensions, containers, constraints)
   - **Extension non-compliance:** Review activated extension rules; add missing artifacts or constraints
3. If AI-DWG has already generated:
   - Communicate AP corrections that affect steering files
   - Flag any container/technology changes that would require workspace regeneration
   - Consider targeted AI-DWG reconciliation for affected modules only
4. Update `adlc-state.md` to reflect the quality review was performed post-completion

## Checks Performed

### ADR Quality (A1–A5)

1. **A1 — ADR presence for major decisions:** Verify that every technology selection (Stage 6), isolation pattern (Stage 7), and security model (Stage 8) has a corresponding ADR. Minimum: 1 ADR per DECISIONS phase stage completed.
2. **A2 — ADR format compliance:** Every ADR follows the template structure: Title, Status, Context, Decision, Consequences, Alternatives Considered. No section may be empty or contain only placeholder text.
3. **A3 — ADR sequential numbering:** Verify ADR files follow `ADR-{NNN}_{Title}.md` naming with sequential numbering (ADR-001, ADR-002, ...). No gaps, no duplicates.
4. **A4 — ADR status consistency:** Each ADR has a valid status (Proposed, Accepted, Deprecated, Superseded). Superseded ADRs reference their successor. No ADR in "Proposed" status should exist in a completed package (must be Accepted or explicitly deferred).
5. **A5 — ADR cross-references:** ADRs that depend on or constrain each other must include cross-references. Technology Stack document must reference relevant ADRs. Architecture Workbook decisions that escalated to ADR must link to the ADR.

### C4 Level Consistency (L1–L4)

6. **L1 — System Context completeness:** `02_System_Context_C4L1.md` defines all external actors and systems. Every external system referenced in integration documents must appear in the System Context.
7. **L2 — Container integrity:** Every container in `03_Container_Diagram_C4L2.md` has: name, technology, responsibility, and inter-container communication defined. No container referenced in downstream documents (API, Data, Integration) that isn't defined here.
8. **L3 — Component-to-Container alignment:** Every component in `11_Component_Diagram_C4L3.md` maps to exactly one container defined in L2. No orphaned components (referencing non-existent containers).
9. **L4 — Progressive detail validation:** L2 must exist before L3 is authored. If L3 exists, verify its module boundaries derive from L2 container responsibilities (not invented independently).

### Decision Traceability (T1–T3)

10. **T1 — Requirement-to-decision linkage:** Architecture Vision constraints and quality attributes must trace to input requirements (PIP or standalone source). Flag any constraint with no upstream justification.
11. **T2 — Decision-to-artifact linkage:** Every ADR and Architecture Workbook decision must materialize in at least one architecture document (Technology Stack, Security, Data, API, etc.). Decisions recorded but never applied = dead decisions.
12. **T3 — Constraint propagation:** Constraints stated in Architecture Vision (budget, team skills, timeline, infrastructure) must be respected in Technology Stack selections. Flag any technology choice that contradicts a stated constraint without an explicit ADR justifying the override.

### Cross-Reference Integrity (X1–X4)

13. **X1 — Inter-document references:** Verify that explicit references between architecture documents resolve. Data Architecture referencing "Container X" → that container exists in L2. API Architecture referencing "External System Y" → that system exists in System Context.
14. **X2 — Technology consistency:** Technology selections in `04_Technology_Stack.md` must match technologies declared in Container Diagram (L2). No container using a technology not selected/justified in the Tech Stack.
15. **X3 — Security coverage:** Every container handling user data or external communication must be addressed in `06_Security_Identity_Architecture.md`. Flag containers with no security consideration.
16. **X4 — Integration completeness:** Every external system in System Context (L1) must have an integration pattern defined in `09_Integration_Architecture.md` (or an explicit ADR stating "no integration needed" with rationale).

### Extension Compliance (E1–E2)

17. **E1 — Activated extension enforcement:** If `adlc-state.md` lists enabled extensions (DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags), verify the corresponding extension artifacts exist and extension-specific rules are reflected in the architecture documents.
18. **E2 — Extension coherence:** Activated extensions must not contradict each other or the base architecture. Flag: Microservices extension active but Container Diagram shows a monolith with no decomposition plan. Event Sourcing active but Data Architecture shows only CRUD patterns.

### State File & Downstream Readiness (S1–S3)

19. **S1 — State file completeness:** `adlc-state.md` contains: system name, current phase = Complete, all 13 stages with status, depth level, enabled extensions list, container inventory (name + technology), input mode (greenfield/brownfield), and quality score.
20. **S2 — Downstream signal fields:** Verify all fields that AI-DWG reads are populated: Enabled Extensions, Containers (name + technology), Technology decisions, Architectural constraints, Input Mode, Quality attributes. Empty or missing fields = AI-DWG will produce incomplete steering.
21. **S3 — Management register presence:** Verify `management_framework/` contains: Decision_Log.md, Change_Log.md, Issue_Log.md, Lessons_Learned.md. In chain mode, verify spine marker (`management_framework/MANAGEMENT_FRAMEWORK.md`) exists with `ADLC-*` phase-tagged entries.

## Output

- **If all checks pass:** Summary report:
  ```
  ✅ AP Quality Check — PASS
  📦 {system_name} | Depth: {level} | Stages: {n}/13 complete
  📐 ADRs: {n} recorded | C4 Levels: L1→L2→L3 consistent
  🔗 Cross-references: {n} verified | Extensions: {list or "none"}
  🎯 Ready for AI-DWG handoff / development team onboarding.
  ```

- **If violations found:**
  - Per-check report: check ID, status (PASS/WARN/FAIL), finding, remediation suggestion
  - Summary score: `{passed}/{total} checks passed`
  - Compliance log entry appended to `.governance/compliance-log/events/{today-date}.jsonl`
  - Event type: `check`, agent: `architecture-decision-agent`, result: `pass|fail|warn`
  - Prioritized remediation list (FAIL items first, then WARN)

**Output location:** `.governance/compliance-log/events/` (if `.governance/` exists; otherwise inline report only)

## Related

- **Workflow source:** `ai-adlc-rules/core-workflow.md` (defines the 13 stages and gates)
- **Process overview:** `ai-adlc-rule-details/common/process-overview.md`
- **Content validation:** `ai-adlc-rule-details/common/content-validation.md`
- **Diagram standards:** `ai-adlc-rule-details/common/diagram-standards.md`
- **ADR template:** `ai-adlc-rule-details/templates/adr-template.md`
- **Extensions:** `ai-adlc-rule-details/extensions/` (6 opt-in patterns)
- **Contract:** Agent Governance Contract §4, §5
- **Upstream dependency:** AI-PILC's `initiation-quality-agent` validates what AI-ADLC **consumes**; this agent validates what AI-ADLC **produces**
- **Downstream dependency:** AI-DWG reads `adlc-state.md` — quality of that file directly impacts workspace generation
- **Complementary agents:** `initiation-quality-agent` (AI-PILC) checks PIP quality; `session-discipline-agent` (AI-GCE) checks process methodology; this agent checks AP artifact quality
