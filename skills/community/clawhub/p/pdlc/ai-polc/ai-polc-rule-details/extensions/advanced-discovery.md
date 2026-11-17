<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Advanced Discovery (Full Rules)

**Stage:** 4 (Product Discovery & Roadmap)
**Adds:** OKR hierarchy, JTBD framing, opportunity scoring, hypothesis backlog

---

## Additional Steps (append to Stage 4)

### Step 4.E1: Build OKR Hierarchy

For each strategic theme, define Objectives and Key Results:

```
Objective: {Qualitative, inspirational goal}
├── KR1: {Quantitative, measurable result} — Target: {X} by {date}
├── KR2: {Quantitative, measurable result} — Target: {X} by {date}
└── KR3: {Quantitative, measurable result} — Target: {X} by {date}
```

**Rules:**
- 2-4 Objectives per quarter/cycle
- 2-4 Key Results per Objective
- Key Results are MEASURABLE (number, percentage, binary)
- Objectives are ASPIRATIONAL (not "maintain" — push growth)
- OKRs align to product goals (Stage 2) — they're the same goals in OKR format

### Step 4.E2: JTBD Framing

For each user segment, define jobs:

```
When {situation},
I want to {motivation/job},
So I can {expected outcome}.
```

**Job categories:**
- Functional jobs (what they're trying to do)
- Emotional jobs (how they want to feel)
- Social jobs (how they want to be perceived)

Map jobs to epics: which epics address which jobs?

### Step 4.E3: Opportunity Scoring (RICE)

Score each roadmap item:

| Item | Reach | Impact | Confidence | Effort | RICE Score |
|------|:---:|:---:|:---:|:---:|:---:|
| {Capability A} | 5000 users | 3 (high) | 80% | 2 sprints | 6000 |
| {Capability B} | 1000 users | 2 (medium) | 50% | 4 sprints | 250 |

**RICE = (Reach × Impact × Confidence) / Effort**

Use RICE to validate/adjust the roadmap horizon placement.

### Step 4.E4: Hypothesis Backlog

For uncertain capabilities, frame as testable hypotheses:

| # | Hypothesis | Test Method | Success Criteria | Epic Impact |
|---|-----------|------------|-----------------|-------------|
| H1 | Users prefer {X} over {Y} | A/B test | +15% conversion | EPIC-005 |
| H2 | Market wants {feature} | Smoke test landing page | >500 sign-ups/week | EPIC-009 |

**Rules:**
- Hypotheses are tested BEFORE full build commitment
- Failed hypothesis → epic deprioritized or removed
- Validated hypothesis → proceed with confidence

---

## Additional Output

When this extension is active, `roadmap.md` additionally contains:
- OKR section (Objectives + Key Results)
- JTBD mapping (jobs → epics)
- RICE scores (if used for opportunity scoring)
- Hypothesis backlog (linked to relevant epics)
