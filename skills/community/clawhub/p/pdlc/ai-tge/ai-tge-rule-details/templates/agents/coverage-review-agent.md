<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: coverage-review-agent
description: >
  Validates coverage report accuracy, gap progression trends, debt movement direction,
  and register-to-report integrity during AI-TGE Observation phase execution.
generatedBy: AI-TGE
generatedVersion: "{version}"
source: ai-tge-rules/core-engine.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read"]
trigger: CVR__
tier: 1
type: audit
agId: TGE-AG-02
---

# Coverage Review Agent

## Purpose

Validates that the test coverage artifacts produced during AI-TGE's Observation phase are accurate, consistent, and trend-aware. Checks gap analysis integrity (new gaps detected, aging tracked, regressions flagged), progress tracking (tests added vs. required, velocity), debt movement (risk score changes, bucket migrations), and register-to-report synchronization. Ensures the team's understanding of test completeness reflects reality.

## When to Invoke

Call this agent **during the Observation phase** — after coverage reports are generated or before sprint/release decisions that depend on test completeness data.

- **Trigger:** Type `CVR__` in the chat prompt
- **Cadence:** After each coverage report generation (Stage 9); at sprint boundaries; before release gates
- **Process point:** After Stage 9 (Coverage Reporting) completes and `.governance/test/coverage-report.md` is updated

**Concrete examples:**
- "I've generated a coverage report" → call `CVR__` to validate accuracy
- "Are we ready for release?" → call `CVR__` to confirm coverage trends are healthy
- "Sprint planning — what should we test next?" → call `CVR__` to verify debt priorities are current
- "Architecture changed and reconciliation ran" → call `CVR__` after the subsequent coverage report
- "The team says coverage is at 80% — is that real?" → call `CVR__` to validate the number

## Consequences of Skipping

**Immediate impact:**
- Coverage percentages may include deprecated/overridden entries → inflated confidence
- New gaps introduced by reconciliation go unnoticed → critical tests never prioritized
- Debt scorecard stale → team works on Medium-risk gaps while Critical ones grow
- Register and coverage report drift apart → conflicting quality signals

**Accumulated debt (skipped across multiple sprints):**
- Teams make release decisions on inaccurate coverage data → production incidents from untested paths
- Gap aging becomes invisible → gaps that persisted for 5 sprints get same urgency as new ones
- Velocity trends not tracked → no early warning when test debt grows faster than capacity
- Observation phase loses credibility ("the numbers don't match what we see in CI")

## Recovery

If you skipped `CVR__` and coverage decisions were already made:

1. Run `CVR__` now — it reads current `.governance/test/` state and validates against the latest coverage report
2. For each issue found:
   - **Inflated coverage:** Recalculate excluding Deprecated/Overridden; communicate corrected % to team
   - **Missing gap detection:** Run gap analysis against current register; flag new entries added since last review
   - **Stale debt scores:** Trigger Stage 12 (Debt Reassessment) to re-score all missing tests with current factors
   - **Register/report drift:** Regenerate coverage report from current register state; diff against published version
3. If a release decision was made on bad data:
   - Document the discrepancy in `.governance/test/defect-log.md` as a process finding (not a code defect)
   - Assess whether the actual coverage gap poses release risk
   - Communicate correction to decision-makers with revised risk assessment

## Checks Performed

### Category G: Gap Analysis (G1–G4)

| ID | Check | Pass Criteria |
|----|-------|---------------|
| G1 | New gaps since last observation | Coverage report identifies all register entries that moved to "Required" since last report timestamp |
| G2 | Gap aging tracked | Each missing test has a `firstDetected` date; gaps older than 2 sprints are flagged as "aging" |
| G3 | Regression detection | Any register entry that moved from "Exists" back to "Missing" is explicitly called out as regression |
| G4 | Reconciliation gaps separated | Gaps introduced by architecture reconciliation (Stage 10) are tagged separately from original strategy gaps |

### Category P: Progress Tracking (P1–P4)

| ID | Check | Pass Criteria |
|----|-------|---------------|
| P1 | Tests added vs. required ratio | Coverage report shows both absolute numbers (N added / M required) and delta since last report |
| P2 | Velocity trend calculated | If ≥2 observation cycles exist, trend direction stated (improving / stable / degrading) |
| P3 | Sprint target alignment | If sprint targets were set (Stage 5 strategy), progress measured against them specifically |
| P4 | Zero-progress flag | If no new tests were added since last observation and gaps remain, report explicitly states "no progress" |

### Category D: Debt Movement (D1–D4)

| ID | Check | Pass Criteria |
|----|-------|---------------|
| D1 | Score recalculation current | Debt scorecard timestamps match or post-date the latest coverage report |
| D2 | Bucket migrations logged | Any test gap that moved between risk buckets (e.g., Medium → Critical) is explicitly noted with reason |
| D3 | Critical count trend | Report shows Critical-bucket count over time (growing = alarm, shrinking = healthy) |
| D4 | Addressed debt acknowledged | Tests that moved from "Missing" to "Exists" are removed from debt scorecard and noted as resolved |

### Category I: Integrity (I1–I3)

| ID | Check | Pass Criteria |
|----|-------|---------------|
| I1 | Register ↔ coverage report sync | Total entries in register matches total referenced in coverage report (no orphans either direction) |
| I2 | Observation timestamp current | Coverage report `lastGenerated` date is within the current sprint/iteration (not stale from prior sprint) |
| I3 | Story-derived entries included | If Stage 8 (Story Acceptance Mapping) added entries, coverage report includes them in calculations |

## Output

```markdown
## CVR__ — Coverage Review Report

**Date:** {ISO-date}
**Package:** AI-TGE v{version}
**Scope:** .governance/test/coverage-report.md + .governance/test/debt-scorecard.md + .governance/test/test-register.md

### Summary
| Category | Checks | Pass | Fail |
|----------|:------:|:----:|:----:|
| G — Gap Analysis | 4 | {n} | {n} |
| P — Progress | 4 | {n} | {n} |
| D — Debt Movement | 4 | {n} | {n} |
| I — Integrity | 3 | {n} | {n} |
| **Total** | **15** | **{n}** | **{n}** |

### Coverage Snapshot
| Metric | Value |
|--------|-------|
| Tests Required | {N} |
| Tests Existing | {N} |
| Tests Missing | {N} |
| Coverage % | {N}% |
| Critical Gaps | {N} |
| Gaps Aging >2 sprints | {N} |
| Regressions | {N} |

### Findings
{list of failures with ID, check, finding, recommended fix}

### Trend (if ≥2 observations)
| Metric | Previous | Current | Direction |
|--------|----------|---------|-----------|
| Coverage % | {N}% | {N}% | {↑/↓/→} |
| Critical Gaps | {N} | {N} | {↑/↓/→} |
| Velocity (tests/sprint) | {N} | {N} | {↑/↓/→} |

### Verdict
{PASS — all 15 checks pass / FAIL — {n} issues found, {n} critical}
```

## Related

- **AI-TGE core-engine.md** — master orchestration defining the observation flow (Stages 7–12)
- **AI-TGE `common/two-source-model.md`** — baseline + AP-derived resolution rules
- **AI-TGE `common/test-taxonomy.md`** — ISTQB classification reference
- **`AGENT_GOVERNANCE_CONTRACT.md` §4** — anatomy specification this agent follows
- **Test-governance-agent (`TGV__`)** — complementary agent focused on strategy-phase validation
- **AI-GCE `compliance-audit-agent`** — checks code compliance (does NOT validate test governance)
- **Stage 9 (Coverage Reporting)** — produces the artifacts this agent validates
- **Stage 12 (Debt Reassessment)** — re-scores debt; run before `CVR__` if factors changed
