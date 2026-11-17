<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 9: Product Risk & Assumptions

**Phase:** Governance
**Purpose:** Identify product-level risks (market, usability, value, adoption) and track assumptions that need validation — separate from project risks (AI-PILC) and technical risks (AI-ADLC).

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Risk Analyst** sub-role:

### Behavioral Shifts
- Think in terms of probability × impact — not just "what could go wrong" but "how likely and how bad"
- Distinguish product risks (value, adoption, market) from project risks (budget, timeline, resources)
- Treat assumptions as untested risks — every assumption is a risk waiting to materialize
- Design validation plans: how do we PROVE or DISPROVE each assumption before it's too late?

### Anti-Patterns
- Do NOT list risks without response strategies — a risk without a plan is just worry
- Do NOT confuse product risks with technical risks (those belong in AP/AI-ADLC)
- Do NOT over-engineer risk governance for Minimal depth — 5 risks with simple mitigation is enough
- Do NOT treat all risks equally — scoring forces attention on the ones that matter

### Quality Check
Every risk must pass: "Is this a PRODUCT risk (value/adoption/market) or something else? And do I have a plan if it materializes?" If it's not product-level → redirect. If no plan → add one.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | 3-5 product risks as a simple list. Assumptions noted. No scoring. |
| **Standard** | 5-10 risks with P×I scoring. Assumption log with validation plans. Response strategies. |
| **Comprehensive** | 10-20 risks with full scoring, response strategies, risk owners, review cadence. Extension: Full Risk Register activated. |

---

## Steps

### Step 9.1: Identify Product Risks

Scan for risks in these categories:

| Category | Question | Example |
|----------|----------|---------|
| **Value risk** | Will users find this valuable? | "Users may not adopt the new payment flow" |
| **Usability risk** | Can users figure out how to use it? | "Multi-currency selection may confuse users" |
| **Adoption risk** | Will users switch to/find this? | "Existing users may resist migration from old system" |
| **Market risk** | Will the market still want this when it ships? | "Competitor may launch equivalent feature before us" |
| **Feasibility risk** | Can we actually deliver the value promised? | "Payment provider API may not support required operations" |
| **Compliance risk** | Will regulatory changes affect the product? | "New PCI requirements may invalidate current approach" |

Sources:
- PIP risk register (project-level → filter for product implications)
- AP technical risks (filter for product-facing ones)
- Context factors (compliance, market type, product maturity)
- Epic dependency chain (what if a dependency fails?)

### Step 9.2: Score Risks (Standard+ Depth)

| Risk | Probability (1-5) | Impact (1-5) | Score (P×I) | Priority |
|------|:---:|:---:|:---:|:---:|
| Users may not adopt new payment flow | 3 | 5 | 15 | HIGH |
| Competitor launches first | 2 | 4 | 8 | MEDIUM |
| API provider changes terms | 1 | 5 | 5 | MEDIUM |
| Onboarding too complex | 3 | 3 | 9 | MEDIUM |

**Priority bands:** HIGH (15-25) | MEDIUM (6-14) | LOW (1-5)

### Step 9.3: Define Response Strategies

For each HIGH and MEDIUM risk:

| Strategy | When to Use | Example |
|----------|------------|---------|
| **Mitigate** | Reduce probability or impact | "Prototype payment flow with 5 users before full build" |
| **Avoid** | Eliminate the risk entirely | "Use payment abstraction layer → not locked to one provider" |
| **Transfer** | Shift to someone else | "Use managed payment service → compliance is their problem" |
| **Accept** | Risk is low enough or unavoidable | "Accept competitor risk; focus on differentiation instead" |

### Step 9.4: Build Assumption Log

Assumptions are beliefs we're treating as true but haven't validated:

| # | Assumption | Confidence | Validation Method | Deadline | Status |
|---|-----------|:---:|---|---|:---:|
| A1 | Users prefer one-click payment over manual entry | Medium | A/B test in MVP | Before R2 | Unvalidated |
| A2 | Stripe API supports multi-currency natively | High | Technical spike | Before R1 | Validated ✅ |
| A3 | Target users have >1 payment method | Low | User survey | Before R1 | Unvalidated |

**Rule:** High-impact unvalidated assumptions connected to MVP scope → must validate BEFORE building the dependent epic.

### Step 9.5: Connect Risks to Backlog

For each HIGH risk, identify:
- Which epics are affected if this risk materializes?
- Is there a mitigation epic that should exist? (Add to backlog if yes)
- Should any epic's priority change based on risk assessment?

If risk analysis reveals new epics needed → add them and re-run Stage 6 (prioritization).

### Step 9.6: Persist Risk Register

Write `product-risk-register.md` with:
- Risk table (category, description, P×I, priority, response strategy)
- Assumption log (assumption, confidence, validation method, deadline, status)
- Risk-to-epic mapping (which risks affect which epics)
- Review cadence (when to reassess)

---

## Extension: Full Risk Register

If triggered ("full risk management"), load `extensions/full-risk-register.md` and additionally produce:
- Risk owners (who monitors each risk)
- Detailed response plans (step-by-step mitigation actions)
- Risk review cadence (formal sessions)
- Risk trend tracking (are risks increasing or decreasing over time?)
- Assumption validation experiments (designed tests for each assumption)

---

## Gate

**Gate 9 — Risks & Assumptions Confirmed:**

Present to user:
```
Product risks identified: {N}
• HIGH: {N} (response strategies defined)
• MEDIUM: {N}
• LOW: {N}

Assumptions logged: {N}
• Unvalidated: {N} (validation plans assigned)
• Validated: {N}

Any risks missing? Any assumptions you want to challenge?
Approve to proceed to Traceability.
```

User must confirm before proceeding.

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-008: Product risk register established. {N} risks identified
({N} HIGH, {N} MEDIUM, {N} LOW). {N} assumptions logged.
Response strategies defined for all HIGH/MEDIUM risks.
```

---

## Transition

→ **Stage 10: Traceability Spine** (Governance continues)

---

*Detail file for AI-POLC Stage 9 | Phase: Governance*
