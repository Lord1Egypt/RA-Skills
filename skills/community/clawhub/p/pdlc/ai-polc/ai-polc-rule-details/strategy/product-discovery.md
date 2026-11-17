<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 4: Product Discovery & Roadmap

**Phase:** Strategy
**Purpose:** Map strategic themes into time horizons, establish the product roadmap, and define the value proposition that guides all subsequent decomposition and prioritization.

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Product Strategist** sub-role:

### Behavioral Shifts
- Think in horizons (Now/Next/Later), not in fixed timelines
- Frame capabilities as value hypotheses that need validation
- Balance ambition with delivery reality — the roadmap is a plan, not a promise
- Connect every roadmap item to a product goal from Stage 2

### Anti-Patterns
- Do NOT produce a Gantt chart disguised as a roadmap — use outcome-based horizons
- Do NOT commit to dates at this stage — horizons express sequence and priority, not calendar promises
- Do NOT include implementation details in the roadmap — it's WHAT and WHY, not HOW

### Quality Check
Every roadmap item must pass: "Does this connect to a product goal, and can I explain WHY it's in this horizon?" If no → remove or reclassify.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Simple Now/Next/Later with 2-3 items per horizon. Value proposition in one sentence. |
| **Standard** | Full roadmap with strategic themes, 3-5 items per horizon, value proposition canvas. |
| **Comprehensive** | Roadmap + OKRs + JTBD framing + opportunity scoring. Extension: Advanced Discovery activated. |

---

## Steps

### Step 4.1: Confirm Strategic Themes

Recall themes from Stage 2 (Step 2.4). If not established, derive them now:

```
Strategic Themes (from goals):
1. {Theme A} — serves goals: {G1, G2}
2. {Theme B} — serves goals: {G3}
3. {Theme C} — serves goals: {G4, G5}
```

Each theme becomes a swim lane in the roadmap.

### Step 4.2: Build the Now/Next/Later Roadmap

| Horizon | Meaning | Confidence | Typical Scope |
|---------|---------|:---:|--------------|
| **Now** | Currently committed / in progress | High (80-100%) | 1-2 sprints or current quarter |
| **Next** | Planned, sequenced, waiting for Now to complete | Medium (50-80%) | Next quarter |
| **Later** | Intended direction, not yet scoped in detail | Low (20-50%) | Future quarters |

For each theme, place capabilities in horizons:

```
Theme: "Payment Excellence"
├── NOW:   Multi-currency support (serves Goal 1)
├── NEXT:  Payment provider abstraction (serves Goal 2)
└── LATER: Crypto payment research (serves Goal 3)

Theme: "User Growth"  
├── NOW:   Onboarding redesign (serves Goal 4)
├── NEXT:  Referral program (serves Goal 5)
└── LATER: Enterprise self-service (serves Goal 6)
```

### Step 4.3: Define Value Proposition

Articulate why users choose this product over alternatives:

**Simple format (Minimal depth):**
```
We help {users} to {outcome} by {approach}, unlike {alternatives} which {limitation}.
```

**Canvas format (Standard+ depth):**

| Element | Content |
|---------|---------|
| Customer segments | {who are the users?} |
| Jobs to be done | {what are they trying to accomplish?} |
| Pains | {what frustrates them today?} |
| Gains | {what would delight them?} |
| Value proposition | {how does this product uniquely address their jobs/pains/gains?} |

### Step 4.4: Context-Factor Adaptation

Adapt roadmap structure based on context:

| Context Factor | Roadmap Adaptation |
|---|---|
| Product Maturity = New (0→1) | Heavy "Now" focus; Later is speculative; MVP dominates |
| Product Maturity = Growth | Balanced horizons; growth experiments in Next |
| Product Maturity = Mature | Optimization-heavy Now; innovation in Later |
| Market = B2C | Fast-pivoting; shorter horizons; experiment-driven |
| Market = B2B | Committed items in Now (contractual); longer planning |
| Delivery = SAFe | Align horizons to PI cadence |
| Scale = Multi-team | Per-team swim lanes within themes |

### Step 4.5: Validate Roadmap Against Goals

Every roadmap item must:
- [ ] Connect to at least one product goal
- [ ] Have a clear "why this horizon" rationale
- [ ] Not contradict the PO's authority boundaries (Stage 3)
- [ ] Be achievable within the stated architecture (if AP available)

Flag any item that fails validation.

### Step 4.6: Persist Roadmap

Write `roadmap.md` with:
- Strategic themes
- Now/Next/Later table (per theme)
- Value proposition (simple or canvas)
- Goal linkage for every item
- Roadmap governance rules (who can change it, review cadence)

---

## Extension: Advanced Discovery

If triggered ("OKRs", "jobs to be done", "hypothesis testing"), load `extensions/advanced-discovery.md` and additionally produce:
- OKR hierarchy (Objective → Key Results per goal)
- JTBD framing (job stories for each user segment)
- Opportunity scoring (reach × impact × confidence × effort)
- Hypothesis backlog (assumptions to validate before building)

---

## Gate

**Gate 4 — Roadmap Confirmed:**

Present to user:
```
Roadmap established:
• Themes: {list}
• Now: {N items} | Next: {N items} | Later: {N items}
• Value proposition: "{one-line summary}"
• All items traced to product goals: ✅

Does this roadmap represent your current product direction?
Approve to proceed to Epic Decomposition.
```

User must confirm before proceeding.

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-003: Product roadmap established with {N} themes across 3 horizons.
Now: {summary}. Next: {summary}. Later: {summary}.
Value proposition: "{one-line}".
```

---

## Transition

→ **Stage 5: Epic Decomposition** (Strategy continues)

---

*Detail file for AI-POLC Stage 4 | Phase: Strategy*
