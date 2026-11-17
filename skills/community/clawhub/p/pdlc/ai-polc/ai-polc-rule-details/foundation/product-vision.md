<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 2: Product Vision & Goals

**Phase:** Foundation
**Purpose:** Distill business intent into a crisp product vision, measurable product goals, and success metrics that anchor all subsequent prioritization and scope decisions.

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Product Strategist** sub-role:

### Behavioral Shifts
- Think in terms of market positioning, value propositions, and measurable outcomes
- Frame goals as testable hypotheses about value delivery
- Challenge vague aspirations — demand specificity and measurability
- Connect every goal to a user outcome or business metric

### Anti-Patterns
- Do NOT accept "improve the product" as a goal — insist on measurable definition
- Do NOT conflate project objectives (AI-PILC territory) with product goals
- Do NOT produce vision statements that only an insider can understand

### Quality Check
Every goal must pass: "Can someone measure whether this goal was achieved 6 months from now?" If no → refine until yes.

---

## Purpose

The product vision is the north star. Without it, prioritization is arbitrary, epics accumulate without coherence, and nobody can answer "are we building the right thing?" This stage establishes the "why" that everything else flows from.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Extract vision from PIP/user input with minimal questioning. 2-3 goals. Accept user's stated metrics. |
| **Standard** | Collaborative refinement. 3-5 goals with explicit success metrics. Challenge weak goals. |
| **Comprehensive** | Deep exploration. 5-8 goals. OKR structure. Multiple metric options per goal. Strategic themes mapped. Market positioning discussed. |

---

## Steps

### Step 2.1: Extract Business Intent

**Chain mode:** Read from PIP:
- Business objectives (from business case)
- Scope statement (what's in/out)
- Success criteria (from project charter)
- Stakeholder expectations

Synthesize into a draft product vision.

**Standalone mode:** Ask the user:
```
What is this product? In 1-2 sentences, describe:
• Who it's for
• What problem it solves
• Why it matters (what changes if it succeeds)
```

### Step 2.2: Craft the Product Vision Statement

Write a vision statement that passes the "elevator test":
- A stranger reads it and understands the product's purpose
- It's aspirational but bounded (not "change the world")
- It names the user segment and the value delivered
- It fits in 1-2 sentences

**Format:**
```
For {target users} who {need/problem}, {product name} is a {category}
that {key benefit}. Unlike {alternatives}, our product {key differentiator}.
```

Present to user. Iterate until confirmed.

### Step 2.3: Define Product Goals

Product goals are the measurable waypoints toward the vision. They answer: "How will we know we're succeeding?"

**At minimum, establish:**
- 2-3 goals (Minimal depth)
- 3-5 goals (Standard depth)
- 5-8 goals with OKR structure (Comprehensive depth)

**Each goal must have:**

| Element | Description | Example |
|---------|------------|---------|
| Goal statement | What we want to achieve | "Reduce payment processing time" |
| Success metric | How we measure it | "Average transaction completes in <2 seconds" |
| Baseline | Current state (if known) | "Currently 8 seconds average" |
| Target | Desired state | "<2 seconds by Q3" |
| Time horizon | When we expect to hit it | "6 months" |

### Step 2.4: Map Goals to Strategic Themes (Standard+)

Group goals into 2-4 strategic themes that will later become roadmap horizons:

```
Theme: "Payment Excellence"
├── Goal: Reduce processing time to <2s
├── Goal: Support 3 payment providers
└── Goal: Achieve PCI-DSS compliance

Theme: "User Growth"
├── Goal: Reach 10K monthly active users
└── Goal: Reduce onboarding drop-off to <20%
```

Themes become the organizing principle for the roadmap (Stage 4).

### Step 2.5: Validate Against Upstream (Chain Mode)

If PIP available, verify:
- Product goals align with project business objectives
- No contradictions between project scope and product vision
- Stakeholder expectations are reflected in goals

If misalignment detected, flag to user:
```
⚠️ Potential misalignment:
• PIP states objective: "{X}"
• Product goal implies: "{Y}"
These may conflict. Which takes priority, or how do they reconcile?
```

### Step 2.6: Persist Vision & Goals

Write `product-vision.md` with:
- Vision statement
- Goals table (goal, metric, baseline, target, horizon)
- Strategic themes (if established)
- Source traceability (which PIP section or user statement each goal derives from)

---

## Gate

**Gate 2 — Vision & Goals Confirmed:**

Present to user:
```
Product Vision: "{vision statement}"

Goals established: {N}
{List each goal with its metric in one line}

Strategic themes: {list themes}

Does this accurately capture what the product should achieve?
Approve to proceed, or adjust.
```

User must confirm before proceeding.

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-001: Product vision and goals established.
Vision: "{summary}". Goals: {N} goals across {N} themes.
Source: {PIP reference or "user-defined"}.
```

---

## Transition

→ **Stage 3: PO Charter & Authority** (Foundation continues)

---

*Detail file for AI-POLC Stage 2 | Phase: Foundation*
