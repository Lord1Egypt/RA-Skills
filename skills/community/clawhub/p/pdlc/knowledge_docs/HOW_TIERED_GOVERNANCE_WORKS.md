# How Tiered Governance Works

**Purpose:** Explains the internal mechanics of AI-GCE's three-tier governance model — how tiers are defined, how rules are assigned to tiers, how graduation works, and how the tier state is tracked and enforced.

---

## What Tiered Governance Is

Tiered governance is a progressive activation model where compliance rules are organized into three levels of increasing rigor. Teams start at Tier 1 (essential rules with minimal friction) and graduate to higher tiers as they demonstrate readiness. This prevents governance rejection while ensuring eventual comprehensive coverage.

```
┌─────────────────────────────────────────────────────────────────────┐
│  TIER 3 — Advanced (production-ready)                                │
│  +15-20 rules: performance, accessibility, deployment, observability │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │  TIER 2 — Standard (stable team)                                │ │
│  │  +10-17 rules: architecture, API, PR, testing, documentation    │ │
│  │                                                                  │ │
│  │  ┌─────────────────────────────────────────────────────────────┐│ │
│  │  │  TIER 1 — Foundational (always active)                      ││ │
│  │  │  5-8 rules: author≠approver, spec-first, naming, security  ││ │
│  │  └─────────────────────────────────────────────────────────────┘│ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

Each tier INCLUDES all rules from lower tiers. Tier 3 = Tier 1 + Tier 2 + Tier 3 rules.

---

## Tier Definitions

### Tier 1 — Foundational

**Activation:** Immediate (day one of governance adoption)
**Philosophy:** Rules that no reasonable developer objects to.

| Rule ID | Rule | Source |
|---------|------|--------|
| GOV-01 | Author ≠ approver (no self-merge) | Built-in baseline |
| GOV-02 | Spec before implementation | Built-in baseline |
| SESSION-01 | Structured session discipline | `session-governance.md` |
| NAME-01 | File naming follows convention | `naming-conventions.md` |
| SEC-01 | No secrets in source code | Built-in baseline |
| SEC-02 | Input validation on public interfaces | `security-rules.md` |
| GOV-03 | PR description required | Built-in baseline |

### Tier 2 — Standard

**Activation:** When Tier 1 compliance ≥ 90% for 2+ weeks
**Philosophy:** Architecture and process enforcement for teams that have internalized basics.

| Rule Category | Rules Added | Source |
|--------------|:-----------:|--------|
| ARCH-* | Module boundary enforcement, dependency direction | `module-structure.md` |
| API-* | Contract-first, versioning, error format | `api-standards.md` |
| GOV-PR-* | Required reviewers, linked issues, description template | `project-governance.md` |
| TEST-* | Coverage thresholds, test presence on new code | `testing-strategy.md` |
| DOC-* | Public interface documentation required | `naming-conventions.md` |

### Tier 3 — Advanced

**Activation:** When Tier 2 compliance ≥ 85% for 4+ weeks
**Philosophy:** Production-grade quality controls for mature projects.

| Rule Category | Rules Added | Source |
|--------------|:-----------:|--------|
| PERF-* | Bundle size budgets, response time limits | `performance-budgets.md` (conditional) |
| A11Y-* | Accessibility compliance (WCAG) | `accessibility.md` (conditional) |
| CONTRACT-* | Consumer-driven contract testing | `api-standards.md` + `testing-strategy.md` |
| DEPLOY-* | Blue-green/canary rules, rollback requirements | `deployment.md` (conditional) |
| OBS-* | Logging, metrics, tracing standards | `logging-observability.md` |

---

## How Rules Are Assigned to Tiers

AI-GCE uses assignment criteria during derivation:

| Criterion | Tier Assignment |
|-----------|:---------------:|
| Universal methodology rule (applies to any project) | Tier 1 |
| Requires architecture decisions to exist first | Tier 2 |
| Requires production infrastructure | Tier 3 |
| Zero false-positive risk | Tier 1 |
| Moderate false-positive risk (needs tuning) | Tier 2 |
| High environmental dependency (CI/CD, monitoring) | Tier 3 |
| Basic human decency in software (don't merge your own PR) | Tier 1 |
| Professional engineering practice (test your code) | Tier 2 |
| Operational excellence (measure everything) | Tier 3 |

---

## The Graduation Mechanism

### State Tracking

`.compliance-state.json` maintains:

```json
{
  "complianceTier": 1,
  "score": 94,
  "scoreHistory": [87, 89, 91, 93, 94],
  "tierActivatedOn": {
    "tier1": "2026-05-01",
    "tier2": null,
    "tier3": null
  },
  "nextTierReadiness": {
    "tier2": {
      "complianceThreshold": true,
      "consecutiveWeeks": 3,
      "requiredWeeks": 2,
      "overallReady": true
    }
  }
}
```

### Readiness Check (Automated)

AI-GCE evaluates readiness on every audit:

**Tier 1 → Tier 2:**
- [ ] Tier 1 score ≥ 90% for ≥ 2 consecutive weeks
- [ ] No critical violations in last audit
- [ ] Team stable (no readiness signal overriding)

**Tier 2 → Tier 3:**
- [ ] Tier 2 score ≥ 85% for ≥ 4 consecutive weeks
- [ ] Production infrastructure exists (monitoring, CI/CD)
- [ ] No high-severity findings unresolved

### Activation Flow

```
Readiness signals met
    ↓
AI-GCE flags: "Team is ready for Tier 2"
    ↓
Team/lead confirms activation
    ↓
Grace period begins (1 week advisory-only)
    ↓
Grace period ends → full enforcement
    ↓
.compliance-state.json updated: tier = 2
```

---

## Tier Rollback (Regression Handling)

If a tier isn't working:

| Scenario | Response |
|----------|----------|
| Score drops 5-10% for 1 week | Advisory: investigate cause |
| Score drops below tier minimum for 2+ weeks | Recommend partial rollback (disable specific categories) |
| Team requests rollback | Downgrade tier, log rationale |
| Critical false-positive pattern | Disable offending rules, keep tier |

**Rollback is never punitive** — it's a signal that the tier was activated too early or rules need tuning.

---

## Partial Activation

Teams can activate CATEGORIES within a tier instead of the full tier:

```json
{
  "complianceTier": 2,
  "tier2ActiveCategories": ["ARCH", "API"],
  "tier2InactiveCategories": ["TEST", "DOC", "GOV-PR"],
  "tier2FullActivationTarget": "2026-07-15"
}
```

This allows teams to absorb Tier 2 incrementally (architecture rules first, then testing, then PR governance) without jumping to full Tier 2 overnight.

---

## Rule Lifecycle Within Tiers

| State | Meaning | Counted in Score? |
|-------|---------|:-----------------:|
| Active | Rule is enforced at current tier | ✅ |
| Dormant | Rule is generated but tier is above current | ❌ |
| Disabled | Rule manually turned off with rationale | ❌ |
| Overridden | Rule replaced by project-specific alternative | ❌ |
| Deprecated | Rule removed during re-derivation (steering changed) | ❌ |

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How Hook Generation Works | `knowledge_docs/HOW_HOOK_GENERATION_WORKS.md` |
| How GCE Compliance Audit Works | `knowledge_docs/HOW_GCE_COMPLIANCE_AUDIT_WORKS.md` |
| How to Scale Governance as Project Matures | `knowledge_docs/HOW_TO_SCALE_GOVERNANCE_AS_PROJECT_MATURES.md` |
| Why Progressive Governance Matters | `knowledge_docs/WHY_PROGRESSIVE_GOVERNANCE_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
