<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: test-governance-agent
description: >
  Validates test strategy completeness, register integrity, coverage gap prioritization,
  and architectural commitment traceability after AI-TGE strategy phase completion.
generatedBy: AI-TGE
generatedVersion: "{version}"
source: ai-tge-rules/core-engine.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read"]
trigger: TGV__
tier: 1
type: process
agId: TGE-AG-01
---

# Test Governance Agent

## Purpose

Validates that the test governance artifacts produced by AI-TGE meet quality engineering standards. Checks strategy completeness, test register integrity (every entry traceable to an architectural commitment or baseline rule), risk scoring consistency, coverage report accuracy, and debt scorecard prioritization logic.

## When to Invoke

Call this agent **after completing the AI-TGE Strategy phase** — before entering Observation mode or presenting the test strategy to the team.

- **Trigger:** Type `TGV__` in the chat prompt
- **Cadence:** Once after Strategy phase (Stages 1–6); optionally after major reconciliation events
- **Process point:** After Stage 6 (Risk Scoring) completes and `.governance/test/debt-scorecard.md` is generated

**Concrete examples:**
- "I've finished the test strategy" → call `TGV__` to validate governance quality
- "Is the test register ready for the team?" → call `TGV__` to check traceability
- "Architecture changed and I ran reconciliation" → call `TGV__` to verify register coherence
- "We're about to start the build (AI-DLC v1)" → call `TGV__` to confirm test governance is in place

## Consequences of Skipping

**Immediate impact:**
- Incomplete test strategy → missing test types for critical architectural commitments
- Unlinked register entries → tests without traceability to design decisions
- Incorrect risk scores → low-risk gaps prioritized over critical ones
- Coverage report inaccuracies → false sense of test completeness

**Accumulated debt (skipped across multiple projects):**
- Teams lose trust in AI-TGE output ("the register is unreliable")
- Architectural commitments remain unverified → production failures from untested promises
- Risk scoring becomes arbitrary → resources allocated to wrong gaps
- Reconciliation misses stale entries → deprecated tests counted as coverage

## Recovery

If you skipped `TGV__` and the strategy is already in use:

1. Run `TGV__` now — it checks the CURRENT state of all `.governance/test/` artifacts
2. For each gap found:
   - **Missing commitment coverage:** Add register entries; re-derive from AP
   - **Broken traceability:** Link entries to source commitments; mark source type
   - **Risk score inconsistency:** Re-score using 4-factor formula; update debt scorecard
   - **Stale entries:** Mark as DEPRECATED; remove from coverage calculations

## Checks Performed

### Category T: Strategy Completeness (T1–T5)

| ID | Check | Pass Criteria |
|----|-------|---------------|
| T1 | Test pyramid defined | `test-strategy.md` has recommended ratios (unit:integration:system:acceptance) |
| T2 | Coverage goals per level | Each test level has a measurable target |
| T3 | Test data strategy present | Data approach defined (synthetic, seeded, production-masked) |
| T4 | Automation approach stated | Which tests automate, which stay manual, rationale for each |
| T5 | Entry/exit criteria defined | Per test level: what must be true to enter/exit that level |

### Category R: Register Integrity (R1–R5)

| ID | Check | Pass Criteria |
|----|-------|---------------|
| R1 | Every entry has a source | `Source` field = AP-derived / Baseline / Story-derived (never blank) |
| R2 | Every entry has a commitment link | `Commitment ID` traces to a specific AP artifact or baseline rule |
| R3 | No duplicate entries | Same commitment + same test type → single entry (not duplicated) |
| R4 | ISTQB taxonomy applied | Level × Type × Technique all populated for every entry |
| R5 | Status values valid | Only: Required / Exists / Missing / Deprecated / Overridden |

### Category S: Risk Scoring (S1–S4)

| ID | Check | Pass Criteria |
|----|-------|---------------|
| S1 | All 4 factors scored | Architectural Risk, Blast Radius, Logic Complexity, Change Frequency (1–5 each) |
| S2 | Composite calculated correctly | Score = Risk × Blast × Complexity × Frequency (1–625 range) |
| S3 | Buckets assigned correctly | Critical (400–625), High (150–399), Medium (50–149), Low (1–49) |
| S4 | Debt scorecard ordered by composite | Highest-risk gaps appear first |

### Category C: Coverage Accuracy (C1–C3)

| ID | Check | Pass Criteria |
|----|-------|---------------|
| C1 | Deprecated excluded from coverage | Coverage % excludes entries with Status = Deprecated |
| C2 | Overridden excluded from coverage | Coverage % excludes entries with Status = Overridden |
| C3 | Multi-view consistency | By-commitment, by-component, by-type, by-risk views all sum to same total |

### Category X: Cross-Reference Integrity (X1–X3)

| ID | Check | Pass Criteria |
|----|-------|---------------|
| X1 | State file reflects register stats | `tge-state.md` counts match actual register entry counts |
| X2 | AP version tracked | `tge-state.md` records which AP version was last read |
| X3 | Reconciliation flag accurate | If AP changed since last read → `Reconciliation Needed: Yes` |

## Output

```markdown
## TGV__ — Test Governance Validation Report

**Date:** {ISO-date}
**Package:** AI-TGE v{version}
**Scope:** .governance/test/ directory

### Summary
| Category | Checks | Pass | Fail |
|----------|:------:|:----:|:----:|
| T — Strategy | 5 | {n} | {n} |
| R — Register | 5 | {n} | {n} |
| S — Scoring | 4 | {n} | {n} |
| C — Coverage | 3 | {n} | {n} |
| X — Cross-Ref | 3 | {n} | {n} |
| **Total** | **20** | **{n}** | **{n}** |

### Findings
{list of failures with ID, check, finding, recommended fix}

### Verdict
{PASS — all 20 checks pass / FAIL — {n} issues found, {n} critical}
```

## Related

- **AI-TGE core-engine.md** — master orchestration defining the strategy + observation flow
- **AI-TGE `common/test-taxonomy.md`** — ISTQB classification reference
- **AI-TGE `common/two-source-model.md`** — baseline + AP-derived resolution rules
- **`AGENT_GOVERNANCE_CONTRACT.md` §4** — anatomy specification this agent follows
- **Coverage-review-agent (`CVR__`)** — complementary agent focused on observation-phase coverage trends
