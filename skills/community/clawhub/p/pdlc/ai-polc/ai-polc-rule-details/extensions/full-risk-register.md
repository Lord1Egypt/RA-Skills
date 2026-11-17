<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Full Risk Register (Full Rules)

**Stage:** 9 (Product Risk & Assumptions)
**Adds:** Risk owners, detailed response plans, review cadence, trend tracking, validation experiments

---

## Additional Steps (extend Stage 9)

### Step 9.E1: Assign Risk Owners

Every HIGH and MEDIUM risk gets an owner:

| Risk | Owner | Responsibility |
|------|-------|---------------|
| Users may not adopt | PO | Monitor adoption metrics; trigger experiment if low |
| Competitor launches first | PO + Marketing | Track competitor; adjust differentiation |
| API provider changes terms | Tech Lead | Monitor provider communications; maintain abstraction |

### Step 9.E2: Detailed Response Plans

For each HIGH risk, a full mitigation plan:

```
Risk: Users may not adopt new payment flow
Owner: PO
Probability: 3/5 | Impact: 5/5 | Score: 15 (HIGH)

Response Plan:
1. MITIGATE (before release):
   - Conduct usability testing with 5 users (Sprint 2)
   - A/B test old vs. new flow with 10% traffic (Sprint 3)
   - Define adoption threshold: 60% usage in 2 weeks post-release
2. MONITOR (during release):
   - Track daily adoption rate
   - Alert if <30% after 1 week
3. CONTINGENCY (if risk materializes):
   - Rollback to old flow (feature flag)
   - Create "guided migration" epic for next sprint
   - Stakeholder communication: "iterating based on feedback"

Trigger for contingency: Adoption <40% after 2 weeks post-release
```

### Step 9.E3: Risk Review Cadence

| Review Type | Frequency | Participants | Focus |
|---|---|---|---|
| Risk scan | Every sprint | PO + Tech Lead | New risks? Existing risks changing? |
| Full review | Every release | PO + Stakeholders | Score reassessment, trend analysis |
| Post-incident | After risk materializes | PO + affected team | Root cause, response effectiveness |

### Step 9.E4: Risk Trend Tracking

Track how risks evolve over time:

| Risk | Sprint 1 | Sprint 2 | Sprint 3 | Trend |
|------|:---:|:---:|:---:|:---:|
| Adoption risk | 15 | 15 | 10 (mitigated by testing) | ↓ Improving |
| Competitor risk | 8 | 8 | 12 (competitor announced) | ↑ Worsening |

### Step 9.E5: Assumption Validation Experiments

For each unvalidated assumption, design a test:

| Assumption | Experiment Design | Duration | Cost | Success Criteria |
|---|---|---|---|---|
| Users prefer one-click | A/B test in MVP | 2 weeks | Low (existing infra) | +15% conversion |
| Market wants crypto | Smoke test landing page | 1 week | Low ($200 ads) | >500 sign-ups |

**Rules:**
- Test cheapest/fastest path first
- Define success/failure criteria BEFORE running
- Failed validation → update risk score upward

---

## Additional Output

When active, `product-risk-register.md` expands to include:
- Risk owners column
- Response plans section (one per HIGH risk)
- Review cadence definition
- Trend tracking table
- Validation experiment log
