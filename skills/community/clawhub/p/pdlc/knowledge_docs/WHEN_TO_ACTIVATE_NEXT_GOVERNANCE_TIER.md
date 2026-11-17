# When to Activate the Next Governance Tier

**Decision:** My team is on Tier 1 (or Tier 2) — is it time to graduate to the next level, or should we stay where we are?

**Derived from:** Pattern: Progressive Activation + Pattern: Gate Before Transition

---

## The Decision at a Glance

| Signal | Tier 1 → 2 | Tier 2 → 3 |
|--------|:---:|:---:|
| Compliance score sustained | ≥90% for 2+ weeks | ≥85% for 4+ weeks |
| Team stable (no churn) | ✅ Required | ✅ Required |
| No unresolved friction on current tier | ✅ Required | ✅ Required |
| Delivery cadence active | ≥1 sprint completed | ≥3 sprints completed |
| Architecture boundaries defined | ✅ Required for Tier 2 | Already enforced |
| Production infrastructure exists | Not required | ✅ Required for Tier 3 |
| Team WANTS more governance | Strong positive signal | Strong positive signal |

---

## Don't Activate If...

### Tier 1 → 2: Hold If Any of These Are True

- Compliance score is fluctuating (85% one week, 92% the next) — not sustained
- A new team member joined in the last 2 weeks (they need to learn Tier 1 first)
- The team has unresolved complaints about existing rules
- Architecture is still being designed (Tier 2 enforces boundaries that must exist first)
- The team hasn't shipped anything yet (no delivery cadence = no context for enforcement)

### Tier 2 → 3: Hold If Any of These Are True

- Tier 2 compliance hasn't stabilized (still climbing or dipping)
- No production infrastructure (monitoring, CI/CD, alerting) — Tier 3 rules assume it exists
- The team feels governance is "just barely manageable" at Tier 2
- No performance/accessibility requirements exist (Tier 3 rules would be irrelevant)
- A major architecture change is planned (stabilize first, then add Tier 3)

---

## Activate When...

### Tier 1 → 2: Ready When ALL Are True

- [ ] Score ≥90% for 2+ consecutive audit periods
- [ ] Zero critical violations in last audit
- [ ] Team members no longer mention Tier 1 rules in retros (internalized)
- [ ] Architecture boundaries are defined (`module-structure.md` exists)
- [ ] API contracts exist (needed for API-* rules)
- [ ] Team has shipped at least one increment (delivery rhythm established)

### Tier 2 → 3: Ready When ALL Are True

- [ ] Score ≥85% for 4+ consecutive audit periods
- [ ] Production infrastructure operational (monitoring, alerting, CI/CD)
- [ ] Team perceives governance as helpful (not just tolerated)
- [ ] Performance/accessibility NFRs documented
- [ ] System is approaching or in production (Tier 3 protects production quality)
- [ ] No major architecture pivot planned in next 8 weeks

---

## The Graduation Process

```
Readiness signals met (check .compliance-state.json)
    │
    ├── Discuss with team: "We're ready for Tier 2 — here's what it adds"
    │
    ├── Preview new rules: show the team what Tier 2 enforces (no surprises)
    │
    ├── Team agrees → Activate with grace period (1 week advisory-only)
    │
    ├── Grace period: new rules fire as WARNINGS (not blocks)
    │   └── Team fixes easy issues, asks questions, adjusts
    │
    └── Grace period ends → full enforcement
        └── .compliance-state.json updated: tier = 2
```

---

## Partial Activation (Category-by-Category)

You don't have to activate the entire tier at once:

**Example Tier 2 partial rollout:**
- Week 1: Activate ARCH-* (architecture boundary rules)
- Week 3: Add API-* (contract compliance)
- Week 5: Add TEST-* (coverage thresholds)
- Week 7: Add GOV-PR-* (PR governance)
- Week 8: Full Tier 2 active

**When to use partial:** Team can absorb rules in one domain at a time. Especially useful for large teams where different roles are affected by different categories.

---

## What If the Team Says "Not Yet"?

Respect it. Readiness signals are SUGGESTIONS, not mandates. If the team says "we're not ready despite the score," investigate:
- Is there a specific rule they're worried about?
- Is there team fatigue from recent process changes?
- Is there an upcoming deadline that makes adding friction risky?

Wait. Revisit in 2-4 weeks. Forced governance fails (see: `WHAT_IF_TEAM_REJECTS_GOVERNANCE.md`).

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Progressive Activation | `knowledge_docs/PATTERN_PROGRESSIVE_ACTIVATION.md` |
| How Tiered Governance Works | `knowledge_docs/HOW_TIERED_GOVERNANCE_WORKS.md` |
| How to Scale Governance as Project Matures | `knowledge_docs/HOW_TO_SCALE_GOVERNANCE_AS_PROJECT_MATURES.md` |
| What If Team Rejects Governance | `knowledge_docs/WHAT_IF_TEAM_REJECTS_GOVERNANCE.md` |
| Why Progressive Governance Matters | `knowledge_docs/WHY_PROGRESSIVE_GOVERNANCE_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
