<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Scoring Model

## Purpose

This document defines HOW the compliance audit agent scores a project, what the score means, how it maps to tiers, and how individual rule violations affect the total. The scoring model ensures consistency across audits, meaningful trend tracking, and clear communication to stakeholders.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in measurable, defensible metrics: every scoring decision must be justifiable to an external auditor
- Apply conservatism: when two scores conflict, use the LOWER (protect integrity over optics)
- Consider temporal context: a score dip after tier activation is healthy, not alarming
- Ensure severity weighting reflects real-world impact, not bureaucratic checklist counting
- Communicate scores with actionable context — a number without guidance is noise

### Anti-Patterns for This Activity
- Do NOT inflate scores to make projects look compliant (honesty over comfort)
- Do NOT treat all rules as equal weight — a naming violation is NOT equivalent to missing auth
- Do NOT change scoring methodology mid-audit without documenting the change and reason

### Quality Check
A good output from this activity sounds like:
- "Final Score: min(93.3%, 84%) = 84% — one Critical failure (missing auth) correctly pulls the rating from Compliant to Needs Attention. Category breakdown shows Security at 83%, recommend immediate remediation."
- "Tier 2 activation caused expected dip from 72% to 58%. Trend shows recovery trajectory. No escalation needed."

---

## The Score Formula

```
Compliance Score = (passing_rules / total_applicable_rules) × 100
```

Where:
- **passing_rules** = rules that the project currently satisfies
- **total_applicable_rules** = rules active for the current tier AND current phase (not ALL 300+ rules)

**Key point:** The denominator is NOT fixed. It grows as the project advances through tiers and phases. A Tier 1 project is scored against ~30 rules. A Tier 3 project is scored against ~300+ rules.

---

## Score Ratings

| Score Range | Rating | Emoji | Meaning |
|:-----------:|--------|:-----:|---------|
| 90–100 | Compliant | ✅ | Ready for phase transition or release |
| 70–89 | Needs Attention | 🟡 | Minor gaps — fix before next milestone |
| 50–69 | At Risk | 🟠 | Significant gaps — prioritize remediation |
| 0–49 | Non-Compliant | 🔴 | Major governance failures — pause and fix |

---

## Severity Weighting

Not all rules are equal. A missing authentication check (🔴 Critical) matters more than a naming convention gap (🟢 Low). The scoring model applies severity-based deductions:

| Severity | Points Deducted Per Violation | Rationale |
|:--------:|:----------------------------:|-----------|
| 🔴 Critical | -5 points | Blocks phase transition; security/data risk |
| 🟠 High | -3 points | Architectural drift; governance gap; team friction |
| 🟡 Medium (Important) | -1 point | Quality improvement; consistency concern |
| 🟢 Low (Useful) | -0.5 points | Nice-to-have; best practice suggestion |

### Weighted Score Calculation

```
Raw Score = (passing / applicable) × 100

Weighted Score = 100 - sum_of_deductions
  where sum_of_deductions = Σ (severity_weight × violation_count) per severity level

Final Score = min(Raw Score, Weighted Score)
  → Use the LOWER of the two — this prevents a project from scoring 95%
    when it has 2 Critical failures but passes everything else
```

### Example

```
Project: Tier 2 | Phase: Construction
Applicable rules: 120
Passing: 112 (8 failures)

Failures:
  1× 🔴 Critical (missing auth on endpoint)     = -5
  2× 🟠 High (cross-module dependency, no DoD)  = -6
  5× 🟡 Medium (naming violations)              = -5

Raw Score: (112/120) × 100 = 93.3%
Weighted Score: 100 - 16 = 84%
Final Score: min(93.3, 84) = 84% (🟡 Needs Attention)

The Critical violation pulled the score from "Compliant" to "Needs Attention"
— which is correct. One Critical failure should prevent a "Compliant" rating.
```

---

## Per-Tier Score Targets

Each tier has a score target that represents "healthy compliance for this level of enforcement":

| Tier | Expected Score Range | What This Means |
|:----:|:-------------------:|-----------------|
| **Tier 1** | 60–70% | Basic structure + naming in place; governance artifacts may be stubs |
| **Tier 2** | 80–90% | Full governance, role segregation, CI/CD quality gates all passing |
| **Tier 3** | 92–98% | Pre-release posture: security, change management, full audit passing |

### Score Dip on Tier Activation (Expected)

When a team activates a new tier, the score DROPS temporarily because:
- New rules are now in the denominator (total_applicable increases)
- The team hasn't addressed the new rules yet (passing stays same or grows slowly)

**This is expected and healthy.** The typical pattern:

```
Tier 1 active: Score = 72%
Tier 2 activated: Score drops to 58% (new rules expose new gaps)
After 2 sprints: Score recovers to 82%
Tier 3 activated: Score drops to 71%
After remediation: Score reaches 94%
```

The dashboard tracks this trend. A dip after tier activation is NOT a problem — it's the system working correctly.

---

## Phase-Aware Scoring

Rules have phases where they become applicable. The audit agent only scores rules relevant to the current phase:

| Phase | Rules in Scope | Approximate Count (Tier 3) |
|-------|---------------|:--------------------------:|
| Setup | PG-SETUP-*, GOV-INIT-*, NC-* (basic), GOV-SESSION-* (basic) | ~30 |
| Foundation | + PG-FOUND-*, SEC-* (baseline), GOV-SESSION-* (full) | ~70 |
| Construction | + PG-INCEP through PG-TEST-*, GOV-PR-*, GOV-CICD-*, GOV-ROLE-*, GOV-TT-*, GOV-DEVOPS-* | ~200 |
| Integration | + PG-CONST-*, PG-INTEG-*, CM-* | ~270 |
| Go-Live | + SEC-* (SOX/GDPR), all remaining | ~310+ |

**Result:** A project in Setup phase is NOT penalized for missing Construction-phase artifacts. The score reflects "how compliant are you for WHERE you are right now?"

---

## Category Breakdown (In Audit Report)

The audit agent reports scores per category so teams know WHERE to focus:

```
📊 COMPLIANCE AUDIT — Category Breakdown

| Category                    | Applicable | Passing | Score | Status |
|-----------------------------|:----------:|:-------:|:-----:|:------:|
| Architecture Compliance     |     15     |   14    |  93%  |   ✅   |
| API-First                   |      8     |    8    | 100%  |   ✅   |
| Security                    |     12     |   10    |  83%  |   🟡   |
| Naming Conventions          |     20     |   18    |  90%  |   ✅   |
| Phase Gates                 |      6     |    6    | 100%  |   ✅   |
| Role Isolation              |     10     |    7    |  70%  |   🟡   |
| Session Governance          |      8     |    8    | 100%  |   ✅   |
| DevOps & Deployment         |     15     |   12    |  80%  |   🟡   |
| ...                         |    ...     |   ...   |  ...  |  ...   |
|─────────────────────────────|────────────|─────────|───────|────────|
| TOTAL                       |    120     |  112    |  84%  |   🟡   |
```

This tells the team: "Your architecture compliance is great. Focus on Role Isolation and DevOps."

---

## Score Trend Tracking

The audit agent maintains score history in `.compliance-state.json`:

```json
"dashboard": {
  "scoreHistory": [
    { "date": "2025-06-01", "tier": 1, "phase": "setup", "score": 68, "event": "Initial audit" },
    { "date": "2025-06-15", "tier": 1, "phase": "foundation", "score": 74, "event": "Phase transition" },
    { "date": "2025-06-22", "tier": 2, "phase": "foundation", "score": 58, "event": "Tier 2 activated" },
    { "date": "2025-07-06", "tier": 2, "phase": "construction", "score": 82, "event": "Sprint 3 audit" }
  ]
}
```

### Trend Direction

| Trend | Condition | Dashboard Shows |
|-------|-----------|----------------|
| ↑ Improving | Current score > average of last 3 audits | Green arrow |
| → Stable | Current score within ±3 points of average | Neutral arrow |
| ↓ Declining | Current score < average of last 3 audits | Red arrow (action needed) |

---

## Exception and Remediation Impact on Score

### Active Exceptions

A rule with an active exception (formally bypassed with approval) is:
- **NOT counted as a violation** — it's acknowledged debt
- **NOT counted as passing** — it's excluded from both numerator and denominator
- Result: exception reduces `total_applicable` (neutral score impact while active)

### Expired Exceptions

A rule with an EXPIRED exception (past `expiresAt` date) is:
- **Counted as a violation** — the bypass expired; the team had time to fix it
- **Flagged as escalation** — in the audit report and in the dashboard

### Open Remediations

A rule with an open remediation:
- **Counted as a violation** — it's failing until resolved
- **Tracked for MTTR** — time-to-remediate feeds into operational metrics
- **Past-SLA items highlighted** — Critical violations past 24h SLA are escalated

---

## Scoring for Brownfield Projects (Mode 3)

Brownfield projects have a different scoring model during the adoption period:

### Dual Score

```
Overall Score:   Scored against ALL applicable rules (includes legacy violations)
New-Code Score:  Scored against rules checked on NEW code only (post-adoption)
```

The dashboard shows BOTH:
- **Overall** tells stakeholders the true compliance posture
- **New-Code** tells the team "everything we've written since governance started is clean"

### Baseline Exclusion

During the adoption window (12 weeks default):
- Violations documented in `brownfield-baseline.md` are marked as "acknowledged baseline debt"
- They count toward Overall Score (reality) but are visually separated from new violations
- After the adoption window expires: all violations count equally (no more baseline protection)

---

## Escalation Triggers

| Trigger | Action |
|---------|--------|
| Score drops below 50% | Audit agent recommends pausing new feature work; focus on remediation |
| 🔴 Critical rules failing | Phase-gate transition is BLOCKED until resolved |
| Score declining for 3 consecutive audits | Audit agent flags in dashboard; suggests team retrospective on compliance |
| Score improves past tier target | Audit agent suggests activating next tier |

---

## What the Score Does NOT Measure

- ❌ Code quality (that's linters and tests — not compliance rules)
- ❌ Feature completeness (that's sprint/backlog tracking)
- ❌ Team velocity (that's PM metrics)
- ❌ Customer satisfaction
- ❌ Test coverage (included as ONE rule — not the whole score)

The compliance score measures: **"Is this project following the architecture, governance, and methodology decisions that were made?"** Nothing more, nothing less.
