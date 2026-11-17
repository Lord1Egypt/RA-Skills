<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Project Initiation Package Assembly

## Stage: 16 of 16
## Phase: 🚀 MOBILIZATION
## Execution: ALWAYS (Final Stage)

---

## Purpose

Consolidate all deliverables produced throughout the AI-PILC workflow into a complete, cross-referenced, quality-checked Project Initiation Package (PIP). Perform a final audit, flag unresolved items, and produce a package README that serves as the table of contents and handoff summary.

---

## Step-by-Step Execution

### Step 1: Inventory All Artifacts

Scan the output directory and compile a complete inventory of what exists:

```markdown
## Package Inventory

### Core Deliverables

| # | Deliverable | Stage | File Path | Status |
|---|-------------|:-----:|-----------|:------:|
| 1 | Requirement Intake Form | 3 | {path} | ✅ Complete |
| 2 | Requirements Analysis Report | 4 | {path} | ✅ / ⏭️ Skipped |
| 3 | Clarification Questionnaire & Responses | 5 | {path} | ✅ / ⏭️ Skipped |
| 4 | Feasibility Assessment & Prioritization | 6-7 | {path} | ✅ Complete |
| 5 | Business Case | 8 | {path} | ✅ Complete |
| 6 | Project Charter | 9 | {path} | ✅ Complete |
| 7 | Stakeholder Register | 10 | {path} | ✅ Complete |
| 8 | Scope Statement & WBS | 11 | {path} | ✅ Complete |
| 9 | Resource & Budget Plan | 12 | {path} | ✅ Complete |
| 10 | Risk Register | 13 | {path} | ✅ Complete |
| 11 | RACI Matrix & Governance Plan | 14 | {path} | ✅ Complete |
| 12 | Kickoff Agenda & Materials | 15 | {path} | ✅ Complete |

### Management Registers

| # | Register | File Path | Entries |
|---|----------|-----------|:-------:|
| 1 | Decision Log | {path} | {n} entries |
| 2 | Change Log | {path} | {n} entries |
| 3 | Issue Log | {path} | {n} entries |
| 4 | Action Items | {path} | {n} entries ({m} open) |
| 5 | Assumptions & Dependencies | {path} | {n} entries ({m} unvalidated) |
| 6 | Lessons Learned | {path} | {n} entries |

### State & Metadata

| File | Path | Purpose |
|------|------|---------|
| pilc-state.md | {path} | Workflow state and progress tracker |
| Package README | {path} | This summary document (produced in this stage) |
```

---

### Step 2: Completeness Audit

Check each expected deliverable against the workflow's expected outputs:

```markdown
## Completeness Audit

| Check | Expected | Actual | Gap? |
|-------|:--------:|:------:|:----:|
| Core deliverables produced | 12 (max) | {n} | {Yes/No — list missing} |
| Skipped stages (with justification) | — | {n} | {Logged in Decision Log?} |
| All decisions logged | — | {n} in log | {Any unlogged decisions?} |
| All assumptions captured | — | {n} in register | {Any implicit assumptions?} |
| All open actions tracked | — | {n} open | {Any untracked actions?} |
| Management registers initialized | 6 | {n} | {Any missing?} |
```

**For any gaps found:**
1. If a deliverable was intentionally skipped → verify Decision Log entry exists with rationale
2. If a deliverable is missing unexpectedly → flag as an issue; ask user if it should be produced now or noted as incomplete
3. If a register is empty but should have entries → review prior stages for missed logging

---

### Step 3: Cross-Reference Integrity Check

Verify consistency across all documents:

| Check | What to Verify | Documents Involved |
|-------|---------------|-------------------|
| **Project name** | Same everywhere | All documents |
| **Project ID** | Consistent | Charter, Scope, Risk Register, Budget |
| **Stakeholder names** | Consistent spelling, role titles | All documents referencing people |
| **Scope items** | In-scope list matches across documents | Intake Form, Charter, Scope Statement, WBS |
| **Out-of-scope items** | Consistent exclusions | Charter, Scope Statement |
| **Budget figures** | ROM matches where referenced | Business Case, Resource Plan, Charter |
| **Timeline/milestones** | Dates/durations consistent | Business Case, Charter, Scope Statement, Kickoff |
| **Risk references** | Top risks cited in Charter match Risk Register | Charter, Risk Register |
| **Decision references** | Decisions cited in documents match Decision Log IDs | All documents, Decision Log |
| **Methodology** | Same approach stated everywhere | Charter, Governance, Kickoff |

**If inconsistency found:**
1. Identify which document is authoritative (latest approved version)
2. Flag to user: "Inconsistency found: {document A} says X, {document B} says Y. Which is correct?"
3. Update the incorrect document
4. Log correction in Change Log

---

### Step 4: Placeholder Audit

Scan all documents for unresolved placeholders:

```markdown
## Unresolved Placeholders

| # | Document | Placeholder | Context | Resolution Path |
|---|----------|-------------|---------|:---------------:|
| 1 | {Document} | `_[TBD]_` | {What this is — e.g., "Technical Lead name"} | A-{nnn} |
| 2 | {Document} | `_[Pending]_` | {Context} | {How to resolve} |
| 3 | {Document} | `_[To be confirmed]_` | {Context} | A-{nnn} |
```

**Classification:**
- **Critical placeholders** — Must be resolved before project can execute (e.g., PM name, budget approval)
- **Non-critical placeholders** — Can be resolved during early execution (e.g., specific tool selection, meeting room bookings)

**Rules:**
- Every critical placeholder MUST have a corresponding Action Item with an owner
- Non-critical placeholders are acceptable in a handoff package — they become early execution tasks
- Count total placeholders and report in package summary

---

### Step 5: Open Items Summary

Compile all unresolved items across all registers:

```markdown
## Open Items Requiring Resolution

### Open Action Items
| ID | Action | Owner | Due | Blocking? |
|:--:|--------|:-----:|:---:|:---------:|
| A-{nnn} | {Action description} | {Role} | {Date/Phase} | {Yes/No} |

### Unvalidated Assumptions
| ID | Assumption | Risk if Wrong | Validate By |
|:--:|-----------|--------------|:-----------:|
| ASM-{nnn} | {Assumption text} | {Consequence} | {When} |

### Deferred Decisions
| ID | Decision Needed | Context | Decide By |
|:--:|----------------|---------|:---------:|
| D-{nnn} | {What needs deciding} | {Stage where deferred} | {When} |

### Open Issues
| ID | Issue | Impact | Owner | Resolution Path |
|:--:|-------|--------|:-----:|----------------|
| I-{nnn} | {Issue description} | {Impact} | {Role} | {How to resolve} |
```

---

### Step 6: Produce Package Quality Score

Assess overall package quality:

| Dimension | Score (1-5) | Criteria |
|-----------|:-----------:|----------|
| **Completeness** | {n} | All expected deliverables present; minimal gaps |
| **Consistency** | {n} | Cross-references match; no contradictions |
| **Clarity** | {n} | Documents are understandable by target audience |
| **Actionability** | {n} | Next steps are clear; team can start executing |
| **Traceability** | {n} | Requirements trace through all artifacts; decisions logged |

**Overall Package Quality: {sum}/25**

| Score | Rating |
|:-----:|--------|
| 22-25 | 🟢 Excellent — ready for handoff |
| 18-21 | 🟡 Good — minor gaps; can proceed |
| 13-17 | 🟠 Adequate — notable gaps; proceed with caution |
| 5-12 | 🔴 Incomplete — significant work needed before execution |

---

### Step 7: Produce Package README

Create the final summary document:

```markdown
# Project Initiation Package — {project_name}

## Package Summary

| Field | Value |
|-------|-------|
| Project | {project_name} |
| Project ID | {PRJ-ID} |
| Sponsor | {name} |
| Product Owner | {name} |
| Project Manager | {name or TBD} |
| Priority | {MoSCoW} — {Pn} |
| Feasibility | {score}/100 — {rating} |
| ROM Budget | {$range} |
| Timeline | {duration estimate} |
| Team Size | {min}-{max} FTE |
| Package Quality | {score}/25 — {rating} |
| Date Produced | {date} |
| Produced Via | AI-PILC v1.0.0 |

---

## Package Contents

{Inventory table from Step 1}

---

## Key Decisions Made ({n} total)

| # | Decision | Summary |
|---|:--------:|---------|
| D-001 | {date} | {summary} |
| D-002 | {date} | {summary} |
{Top 10 most significant decisions}

(Full log: `{decision_log_path}`)

---

## Open Items for Execution Team ({n} total)

{Summary of blocking items, critical placeholders, and immediate actions from Step 5}

---

## Handoff Recommendations

1. **Before scheduling kickoff:** Resolve all {n} blocking pre-kickoff items
2. **First week of execution:** Address {n} open action items marked for early resolution
3. **First month:** Validate {n} unvalidated assumptions
4. **Ongoing:** Maintain management registers throughout execution; review at every steering meeting

---

## How This Package Was Produced

This Project Initiation Package was produced using **AI-PILC (AI-Driven Project Initiation Life Cycle) v1.0.0** — a structured, interactive workflow guiding project initiation from raw requirement to execution-ready package.

- **Phases completed:** {n}/6
- **Stages completed:** {n}/16
- **Sessions:** {n} interaction sessions
- **Workflow depth:** {Minimal/Standard/Comprehensive}
- **Source document:** {path or description}

---

*Package produced: {date}*
*Status: Ready for sponsor review and kickoff scheduling*
```

---

### Step 8: Save All Final Files

1. Save Package README:
   - Numbered: `{output_root}/PROJECT_INITIATION_PACKAGE_README.md`
   - Flat: `{output_root}/pilc-docs/PROJECT_INITIATION_PACKAGE_README.md`

2. Update state file:
   - Stage 16: ✅ Done
   - Status: Complete
   - Last Updated: {timestamp}

3. Final Decision Log entry:
   - D-{nnn}: "Project Initiation Package assembled and quality-checked. Score: {n}/25. {critical_placeholders} critical items remain open."

4. Final Lessons Learned entry:
   - LL-{nnn}: "AI-PILC workflow completed in {n} sessions. Depth: {level}. Key insight: {main observation about the process or project}."

---

### Step 9: Present Final Summary

```markdown
🎉 AI-PILC WORKFLOW COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Project Initiation Package for "{project_name}" is ready.

📊 Package Summary:
   • Phases completed: {n}/6
   • Deliverables produced: {n}
   • Decisions logged: {n}
   • Risks identified: {n}
   • Open actions: {n} (require human follow-up)
   • Unresolved placeholders: {n} ({critical} critical)
   • Package quality: {score}/25 — {rating}

📁 Package location: {output_root}/
📋 Package README: {readme_path}
📊 State file: {state_path}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Next Steps (Human):
   1. Sponsor reviews and signs the Charter
   2. Budget formally approved by Finance
   3. Resolve {n} blocking items on pre-kickoff checklist
   4. Schedule and conduct kickoff meeting
   5. Transition to execution methodology — run AI-POLC with this PIP as input

🔀 **Chain Navigation (what's next in the AI-* Family):**
   • Sequential next: **AI-POLC** (`_POLC_`) — Product Ownership Life Cycle
   • Or ask AI-FLO: type `_FLO_` for routing guidance based on your project state
   • Dashboard data: type `DAT__ pdlc/pilc` to update the family dashboard

⚠️ **IMPORTANT: Start the next package (AI-POLC) in a NEW session.**
   Each AI-* package loads a full workflow into context;
   a fresh session keeps it fast and focused.

Thank you for working through this process. The package is ready for
sponsor review, signature, and kickoff scheduling.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| User completed only some phases (stopped early) | Produce a partial package; note which stages were skipped; score reflects incompleteness |
| User revisited and changed earlier deliverables | Verify cascading updates were applied; cross-reference check is critical |
| Multiple versions of same document exist | Use latest approved version; archive or note earlier versions |
| Registers have no entries (quiet project) | Acceptable for Change Log, Issue Log if no changes/issues arose; Decision Log should always have entries |
| User wants package in a different format | Offer to reorganize (e.g., single consolidated document vs. folder structure); note this is a presentation choice, not content change |

---

## Package Assembly Anti-Patterns

| Anti-Pattern | Why It's Wrong | What to Do Instead |
|-------------|---------------|-------------------|
| Assembly without quality check | Inconsistencies shipped to execution team | Always run cross-reference and placeholder audits |
| No open items summary | Execution team doesn't know what's unresolved | Always produce explicit open items list |
| Missing traceability | Decisions appear without context | Every decision references its source stage and question |
| Overly optimistic summary | Hides gaps and risks | Be honest about quality score and open items |
| No handoff recommendations | Execution team doesn't know what to do first | Always provide prioritized next steps |
