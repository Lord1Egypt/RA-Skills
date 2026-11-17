# How to Scale Governance as a Project Matures

**Purpose:** Practical guide for progressing through AI-GCE's three governance tiers — when to activate each tier, how to assess readiness, how to handle the transition, and how to avoid the common failure of either too-fast or too-slow progression.

---

## Who This Is For

Tech leads, engineering managers, or DevOps engineers managing a project that started with Tier 1 governance and needs to know: "When do we graduate? How do we add more governance without disrupting delivery? What signals tell us we're ready?"

---

## The Three Tiers (Recap)

```
TIER 1 — Foundational        TIER 2 — Standard           TIER 3 — Advanced
(any project, day one)       (stable team, 2-4 weeks)    (production-ready, months)
                                                          
├── Author ≠ approver        ├── +Architecture boundaries ├── +Performance budgets
├── Spec before code         ├── +API contract compliance  ├── +Accessibility (WCAG)
├── Naming conventions       ├── +Full PR governance       ├── +Contract testing
├── Basic security           ├── +Test coverage thresholds ├── +Deployment governance
├── Session governance       ├── +Documentation req's      ├── +Observability standards
└── 5-8 rules, ~4 hooks     └── 15-25 rules, ~8 hooks    └── 30-45 rules, ~14 hooks
```

Each tier **includes all previous tiers**. Tier 2 = Tier 1 + Tier 2 rules. Tier 3 = everything.

---

## Readiness Signals: When to Graduate

### Tier 1 → Tier 2 Readiness

| Signal | Threshold | Why It Matters |
|--------|-----------|---------------|
| Tier 1 compliance score | ≥ 90% for 2+ consecutive weeks | Team has internalized basic rules |
| Team stability | No new members in last 2 weeks | New members need time to learn Tier 1 first |
| Delivery cadence | ≥ 1 completed sprint/cycle | Team is actually shipping, not just setting up |
| Team sentiment | No unresolved friction on Tier 1 rules | Adding more rules on top of resented rules compounds resistance |
| Architecture stability | Core boundaries defined and stable | Tier 2 enforces boundaries that must exist first |

**Typical timeline:** 2-4 weeks after Tier 1 activation.

### Tier 2 → Tier 3 Readiness

| Signal | Threshold | Why It Matters |
|--------|-----------|---------------|
| Tier 2 compliance score | ≥ 85% for 4+ consecutive weeks | Higher bar because Tier 3 is demanding |
| Production proximity | System approaching or already in production | Tier 3 rules protect production quality |
| Team maturity | Governance perceived as helpful, not burden | Team must value governance before Tier 3's weight |
| Coverage baseline | Test coverage already meeting Tier 2 thresholds | Tier 3 adds performance/accessibility — need foundations solid |
| Operational readiness | Monitoring, logging, alerting infrastructure exists | Tier 3 enforces observability standards — infra must support it |

**Typical timeline:** 2-3 months after Tier 2 activation.

---

## The Graduation Process

### Step 1: Assess Readiness

Check `.compliance-state.json`:

```json
{
  "complianceTier": 1,
  "score": 94,
  "scoreHistory": [87, 89, 91, 93, 94],
  "nextTierReadiness": {
    "tier2": {
      "complianceThreshold": true,
      "teamStability": true,
      "deliveryCadence": true,
      "architectureStability": true,
      "overallReady": true
    }
  }
}
```

When `overallReady: true` — graduation is recommended.

### Step 2: Preview New Rules

Before activating, ask AI-GCE to preview Tier 2 rules:
- How many new rules will be added?
- Which hooks will be introduced?
- What will the new enforcement look like for developers?

Review the preview with the team. No surprises.

### Step 3: Activate with Grace Period

Activate Tier 2 with a **1-week grace period:**
- New rules fire but are ADVISORY (warnings, not blockers)
- Team sees violations without being blocked
- Gives time to fix easy issues before enforcement starts
- After grace period: rules become blocking

### Step 4: Monitor and Adjust

First two weeks after graduation:
- Watch compliance score (expect a temporary dip as new rules find violations)
- Monitor team friction (are specific rules causing disproportionate pain?)
- Tune rules that have false positives
- Provide quick-fix guidance for common Tier 2 violations

---

## Partial Tier Activation

You don't have to activate an entire tier at once:

| Approach | When to Use |
|----------|------------|
| **Full tier activation** | Team is clearly ready across all dimensions |
| **Category-by-category** | Team is ready for some Tier 2 areas but not others |
| **Rule-by-rule** | Specific pain points that one rule addresses |

**Category-by-category example:**
- Week 1: Activate architecture boundary rules (ARCH-*)
- Week 3: Activate API contract rules (API-*)
- Week 5: Activate test coverage rules (TEST-*)
- Week 7: Activate PR governance rules (GOV-PR-*)

This spreads the learning curve and lets the team absorb each category before the next arrives.

---

## Handling Governance Regression

Sometimes compliance drops after initial success:

| Regression Pattern | Cause | Response |
|-------------------|-------|----------|
| Score drops 5-10% over 1 week | New team member, sprint pressure | Advisory mode for affected rules, re-train |
| Score drops 10-20% sustained | Rules too aggressive for current maturity | Consider partial tier rollback, tune thresholds |
| Score drops below Tier 1 baseline | Team resistance, cultural rejection | Stop, address root cause (usually: rules don't match reality) |
| One category consistently low | Specific rules are impractical | Review those rules — are they right for this project? |

**Key principle:** Never force governance. If a tier isn't working, the answer is to adjust the tier or the timeline — not to punish the team.

---

## The Governance Maturity Curve

```
Compliance
Score (%)
    │
100 ┤                                          ┌──────── Tier 3 stable
    │                                     ┌────┘
 90 ┤                    ┌────────────────┘
    │               ┌────┘  ↑ Tier 2 grace period dip
 80 ┤          ┌────┘       (recovers in 1-2 weeks)
    │     ┌────┘
 70 ┤┌────┘  ↑ Tier 1 initial learning
    ││       (rises quickly)
 60 ┤│
    ││
 50 ┤│ ← Starting point (first baseline)
    │
    └─────────────────────────────────────────────────── Time
    Week 1    Week 4     Week 8     Week 16    Week 24
```

**Expected pattern:** Each tier activation causes a temporary score dip (new rules find new violations), followed by rapid recovery as the team adapts, then gradual climb to readiness for the next tier.

---

## Scaling Beyond Tier 3

For teams that master Tier 3:

| Extension | What It Adds | Activate When |
|-----------|-------------|--------------|
| Custom rules | Project-specific enforcement not in standard tiers | Recurring manual reviews catch the same issue |
| Cross-project governance | Portfolio-level consistency rules (AI-PPM) | Organization has multiple projects needing alignment |
| Compliance certification prep | SOC 2, ISO 27001, HIPAA-specific rules | Certification timeline approaching |
| Advanced metrics | Governance effectiveness scoring, trend analysis | Leadership wants quantified improvement data |

These are extensions to the tier model — not a "Tier 4." The three tiers cover professional software development. Beyond Tier 3 is regulatory/organizational specialization.

---

## Tips for Smooth Progression

1. **Celebrate graduation.** Make tier progression visible to the team. "We graduated to Tier 2 because our compliance score has been >90% for 3 weeks" is a team achievement worth acknowledging.

2. **Let the team choose timing.** Present readiness signals and let the team decide when to activate. Imposed governance fails; chosen governance sticks.

3. **Grace periods are not optional.** Even a 3-day grace period where new rules are advisory (not blocking) prevents the "everything broke on Monday morning" experience.

4. **Don't skip tiers.** Tier 2 readiness requires Tier 1 mastery. Teams that jump to Tier 3 without Tier 1 foundations collapse under the weight.

5. **Regression is information, not failure.** A score dip tells you something — listen to it. Maybe the team grew, maybe the sprint was unusually pressured, maybe a rule doesn't fit. Diagnose before prescribing.

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |
| How to Retrofit Governance on Existing Code | `knowledge_docs/HOW_TO_RETROFIT_GOVERNANCE_ON_EXISTING_CODE.md` |
| Why Governance Automation Matters | `knowledge_docs/WHY_GOVERNANCE_AUTOMATION_MATTERS.md` |
| Why Progressive Governance Matters | `knowledge_docs/WHY_PROGRESSIVE_GOVERNANCE_MATTERS.md` (planned) |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
