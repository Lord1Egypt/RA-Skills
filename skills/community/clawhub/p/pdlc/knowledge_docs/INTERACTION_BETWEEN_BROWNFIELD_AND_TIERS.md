# Interaction Between Brownfield Mode and Governance Tiers

**Purpose:** Maps how brownfield adoption (existing codebase) interacts with the tier progression model — how baselines work with tiers, why brownfield projects often start at Tier 1 longer, and how "enforce forward" intersects with tier graduation.

---

## The Interaction

```
BROWNFIELD PROJECT (existing code with existing violations)
    │
    ├── BASELINE recorded (existing violations acknowledged, not penalized)
    │
    ├── TIER 1 activated (enforce on NEW code only)
    │       │
    │       └── Score based on: new violations only (not baseline)
    │               │
    │               └── Tier 2 readiness: based on NEW CODE compliance
    │
    └── Over time: baseline shrinks (files touched → fixed)
                   tiers progress (new code compliant → graduation)
```

---

## How Score Is Calculated in Brownfield

**Greenfield formula:** `score = (checked - violations) / checked × 100`

**Brownfield formula:** `score = (checked - new_violations) / checked × 100`

Where `new_violations` = violations introduced AFTER `enforceFrom` date.

| Violation Category | Counted in Score? | Blocking? |
|-------------------|:-----------------:|:---------:|
| Baseline violations (pre-governance) | ❌ | ❌ |
| New violations (post-governance, in new code) | ✅ | ✅ |
| Violations in modified files (touched post-governance) | ✅ | ✅ |
| Resolved baseline violations | ❌ (positive signal, tracked separately) | N/A |

**Key insight:** A brownfield project can have 47 baseline violations and still show 95% compliance — because the score measures NEW CODE behavior, not historical debt.

---

## Tier Graduation in Brownfield

### Readiness Signals (Modified for Brownfield)

| Signal | Greenfield Threshold | Brownfield Threshold |
|--------|:---:|:---:|
| Compliance score for graduation | ≥90% (Tier 1→2) | ≥90% of NEW code (baseline excluded) |
| Zero critical violations | Absolute | In new code only (baseline criticals tracked separately) |
| Team stability | 2+ weeks | Same |
| Delivery cadence | 1+ sprint | Same |
| Baseline trend | N/A | Declining (positive signal, not required) |

**Brownfield projects CAN graduate tiers** even with high baseline violation counts — as long as NEW code is clean. The baseline is a separate improvement track.

### When to Graduate Despite Baseline

| Scenario | Graduate? | Rationale |
|----------|:---------:|-----------|
| 47 baseline violations, 0 new violations in 3 weeks | ✅ Yes | New code is governed; team has internalized Tier 1 |
| 47 baseline violations increasing (new code adds more) | ❌ No | Team hasn't internalized current tier |
| Baseline decreasing (team fixing on touch) | ✅ Strong positive | Team is proactively improving |
| Baseline static (team avoids touching those files) | ⚠️ Maybe | Governance is working for new code; old code is deferred debt |

---

## The Dual-Track Model

Brownfield projects run two parallel improvement tracks:

```
TRACK 1: Tier Progression (new code quality)
──────────────────────────────────────────────
Tier 1 ────────────→ Tier 2 ─────────────→ Tier 3
(2-4 weeks)          (2-4 months)          (production)

TRACK 2: Baseline Reduction (legacy debt)
──────────────────────────────────────────────
47 violations → 35 → 28 → 19 → 12 → 5 → 0
(as files are touched and fixed over months)
```

**These tracks are INDEPENDENT.** You can be at Tier 3 with 20 remaining baseline violations. The tiers govern new code quality; the baseline governs legacy debt. Both improve, at different rates.

---

## Tier 2+ Rules on Brownfield Code

When Tier 2 activates (e.g., ARCH boundary rules):

| Code Age | Behavior |
|----------|----------|
| New files (post-Tier-2-activation) | Full ARCH enforcement |
| Existing files (pre-Tier-2, never modified) | Violations added to baseline (not blocking) |
| Existing files (modified after Tier 2) | ARCH rules enforced on the change (you touched it, you fix it) |

**Each tier activation extends the baseline.** Tier 2 activation may find 15 new "baseline" violations in existing code (boundary violations that exist but were never checked before). These are baselined, not penalized.

---

## Brownfield + Tiers: Common Scenarios

### Scenario: Large Legacy Codebase, Small Team

```
Day 0: Brownfield overlay → 120 baseline violations detected
Day 1: Tier 1 activated → enforce on new code only
Week 4: Score 95% (new code clean) → ready for Tier 2
Week 5: Tier 2 activated → 30 more baseline violations discovered (boundaries)
         New baseline total: 120 + 30 = 150 (but score still counts new code only)
Week 12: Score 88% (Tier 2 new code) → still climbing
Week 16: Score 92% → approaching Tier 3 readiness
Month 8: Baseline down to 60 (natural fix-on-touch)
```

### Scenario: Active Development, Frequent File Touches

```
Day 0: 80 baseline violations
Week 4: Team touches many files → "fix when touched" enforces
Week 8: Baseline down to 45 (rapid improvement because high file-touch rate)
Week 12: Baseline down to 20
Month 6: Baseline near zero (most files have been touched and fixed)
```

### Scenario: Stable Codebase, Few Changes

```
Day 0: 50 baseline violations
Month 3: Baseline still at 48 (only 2 files touched)
Month 6: Baseline at 45 (very slow reduction)
Year 1: Baseline at 30 (gradual)

→ Consider: dedicated cleanup sprints to accelerate baseline reduction
```

---

## Dedicated Cleanup vs. Fix-on-Touch

| Strategy | Best For | Speed | Disruption |
|----------|----------|:-----:|:----------:|
| **Fix-on-touch** | Active codebases with frequent changes | Gradual | None (part of normal work) |
| **Dedicated cleanup sprint** | Stable code with stagnant baseline | Fast | Moderate (sprint diverted) |
| **Rule-by-rule cleanup** | Targeting one specific violation type | Medium | Low (focused effort) |
| **Module-by-module cleanup** | Targeting one area of the codebase | Medium | Low (scoped) |

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Retrofit Governance on Existing Code | `knowledge_docs/HOW_TO_RETROFIT_GOVERNANCE_ON_EXISTING_CODE.md` |
| How Tiered Governance Works | `knowledge_docs/HOW_TIERED_GOVERNANCE_WORKS.md` |
| How DWG Brownfield Detection Works | `knowledge_docs/HOW_DWG_BROWNFIELD_DETECTION_WORKS.md` |
| When to Use Brownfield vs Greenfield | `knowledge_docs/WHEN_TO_USE_BROWNFIELD_VS_GREENFIELD.md` |
| Pattern: Non-Destructive Reconciliation | `knowledge_docs/PATTERN_NON_DESTRUCTIVE_RECONCILIATION.md` |
| Pattern: Progressive Activation | `knowledge_docs/PATTERN_PROGRESSIVE_ACTIVATION.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
