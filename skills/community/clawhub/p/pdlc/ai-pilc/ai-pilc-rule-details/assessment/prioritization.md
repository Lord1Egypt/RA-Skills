<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Prioritization

## Stage: 7 of 16
## Phase: 🟠 ASSESSMENT
## Execution: ALWAYS

---

## Purpose

Determine the initiative's strategic priority using three complementary methods: Strategic Alignment scoring, MoSCoW classification, and Value/Effort analysis. This produces a final priority rank that informs Business Case urgency, resource allocation decisions, and portfolio positioning.

---

## MANDATORY: Stage Sub-Role — Financial Analyst

During THIS stage, ALSO adopt the mindset of a **Financial Analyst**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Express value and effort in measurable terms wherever data supports it; qualify honestly where it doesn't
- Frame the priority decision as an investment comparison — what is the opportunity cost of doing this vs. alternatives?
- Separate strategic value (alignment) from tactical value (quick win) so the ranking is transparent
- Challenge inflated value claims and underestimated effort with a "prove it" test

### Anti-Patterns for This Stage
- Do NOT assign priority on gut feel — every score needs an evidenced rationale
- Do NOT ignore effort/cost when ranking by value — value without effort context is misleading

### Quality Check
A good output at this stage sounds like:
- "High strategic alignment (4/5) but high effort (low value/effort ratio); MoSCoW: Should-have this cycle, re-evaluate next quarter..."

---

## Step-by-Step Execution

### Step 1: Load Context

1. Read the Feasibility Assessment (Stage 6 output) — particularly the overall score and conditions
2. Read the Requirement Intake Form (Stage 3) — for business need and impact
3. Read any clarification outcomes (Stage 5) — for refined scope understanding
4. Review Decision Log for relevant decisions made so far

---

### Step 2: Score Strategic Alignment

Assess five criteria, each scored 1-5:

| Criteria | 1 (Very Low) | 2 (Low) | 3 (Medium) | 4 (High) | 5 (Very High) |
|----------|-------------|---------|-----------|----------|--------------|
| **Business strategy alignment** | No connection to organizational strategy | Tangential; nice-to-have | Supports one strategic objective | Directly enables a key strategic goal | Core to the organization's primary strategy |
| **Revenue/cost impact** | No measurable financial impact | Marginal savings or minor revenue contribution | Moderate cost reduction or revenue enablement | Significant financial impact (>5% of relevant budget/revenue) | Transformational financial impact; new revenue stream or major cost elimination |
| **Customer/user impact** | No user-facing change | Minor convenience improvement | Noticeable improvement for a user segment | Major improvement for primary user base | Fundamental improvement affecting all users |
| **Regulatory/compliance need** | No regulatory driver | Future regulation may apply (2+ years) | Regulation approaching (within 1 year) | Current compliance gap exists; audit risk | Active non-compliance; enforcement imminent |
| **Competitive advantage** | No competitive factor | Minor parity improvement | Maintains competitive position | Creates differentiation in market | Establishes significant competitive moat |

**Output format:**

```markdown
### Strategic Alignment Score

| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Alignment to business strategy | {n} | {Evidence from source/context} |
| Revenue/cost impact | {n} | {Evidence} |
| Customer/user impact | {n} | {Evidence} |
| Regulatory/compliance need | {n} | {Evidence} |
| Competitive advantage | {n} | {Evidence} |
| **Strategic Score** | **{sum}/25** | {Summary assessment} |
```

**Interpretation:**
| Score Range | Strategic Alignment Level |
|:-----------:|--------------------------|
| 21-25 | Extremely High — strategic imperative |
| 16-20 | High — strongly aligned |
| 11-15 | Moderate — supportive but not critical |
| 6-10 | Low — weak strategic connection |
| 1-5 | Very Low — misaligned or irrelevant to strategy |

---

### Step 3: Apply MoSCoW Classification

Based on strategic alignment, feasibility, and business context, classify:

| Category | Definition | Criteria for Assignment |
|----------|-----------|------------------------|
| **Must Have** | Critical; initiative fails without this | Strategic score ≥20 AND regulatory/compliance driver, OR existential business need, OR hard external deadline |
| **Should Have** | Important; significant value but workarounds exist | Strategic score 16-20 AND no hard deadline, OR strong ROI but not existential |
| **Could Have** | Desirable; adds value but not critical | Strategic score 11-15, OR good idea with flexible timing |
| **Won't Have (this cycle)** | Recognized value but explicitly deferred | Below threshold for current investment cycle, OR dependencies unresolved, OR better alternatives exist |

**Decision logic:**

```
IF strategic_score >= 20 AND (regulatory_score >= 4 OR business_impact = "existential"):
    MoSCoW = "Must Have"
ELIF strategic_score >= 16 OR (strategic_score >= 13 AND feasibility >= 70):
    MoSCoW = "Should Have"
ELIF strategic_score >= 10 AND feasibility >= 50:
    MoSCoW = "Could Have"
ELSE:
    MoSCoW = "Won't Have (this cycle)"
```

**Note:** This is guidance logic, not a rigid formula. The AI should apply judgment and present the classification with rationale. The user has final say.

---

### Step 4: Calculate Value/Effort Scores

#### Value Score (1-10)

Composite of multiple factors:

| Factor | Weight | Input |
|--------|:------:|-------|
| Strategic alignment | 30% | Strategic score (normalized to 10-point scale) |
| Financial benefit | 25% | ROI potential from feasibility + business need |
| User/customer impact | 20% | Customer impact score from strategic alignment |
| Risk reduction | 15% | Does this reduce existing organizational risk? |
| Enablement value | 10% | Does this unlock future capabilities? |

**Calculation:** Weighted average → round to nearest integer (1-10)

#### Effort Score (1-10)

Composite of complexity and resource demand:

| Factor | Weight | Input |
|--------|:------:|-------|
| Complexity | 30% | From Stage 2 complexity assessment |
| Team size needed | 25% | From source estimates or inferred |
| Duration | 20% | From source timeline or estimated |
| Integration work | 15% | From technical feasibility integration score |
| Organizational change | 10% | From operational feasibility change impact |

**Calculation:** Weighted average → round to nearest integer (1-10)

#### Value/Effort Ratio

```
Ratio = Value Score / Effort Score
```

| Ratio | Interpretation |
|:-----:|---------------|
| >2.0 | Exceptional — high value, low effort; immediate priority |
| 1.5-2.0 | Strong — good return on investment |
| 1.0-1.4 | Balanced — value justifies effort |
| 0.7-0.9 | Marginal — effort high relative to value; scrutinize |
| <0.7 | Poor — effort exceeds value; challenge or reject |

---

### Step 5: Assign Final Priority Rank

Combine all three methods:

| Rank | Label | Criteria |
|:----:|-------|----------|
| **P1** | Top Priority — Immediate | MoSCoW = Must Have AND Value/Effort ≥ 1.0 |
| **P2** | High Priority — Near Term | MoSCoW = Should Have AND Value/Effort ≥ 1.0, OR MoSCoW = Must Have AND Value/Effort < 1.0 |
| **P3** | Medium Priority — Planned | MoSCoW = Could Have AND Value/Effort ≥ 1.0, OR MoSCoW = Should Have AND Value/Effort < 1.0 |
| **P4** | Low Priority — Backlog | MoSCoW = Won't Have, OR Value/Effort < 0.7 regardless of MoSCoW |

**Priority context statement:**

For each rank, produce a 1-2 sentence rationale explaining WHY this priority was assigned, referencing the strongest drivers.

---

### Step 6: Produce Prioritization Summary

Add to the Feasibility Assessment document as Section 3, or produce standalone if document is already saved:

```markdown
## Prioritization

### Strategic Alignment Score
| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Alignment to business strategy | {n} | {comment} |
| Revenue/cost impact | {n} | {comment} |
| Customer/user impact | {n} | {comment} |
| Regulatory/compliance need | {n} | {comment} |
| Competitive advantage | {n} | {comment} |
| **Strategic Score** | **{sum}/25** | {summary} |

### Priority Classification
| Method | Result |
|--------|--------|
| MoSCoW Category | ☑ **{category}** |
| Value Score (1-10) | **{n}** |
| Effort Score (1-10) | **{n}** |
| Value/Effort Ratio | **{n.nn}** |
| Final Priority Rank | **{Pn} — {label}** |

**Rationale:** {2-3 sentences explaining the priority assignment — referencing the strongest contributing factors}
```

---

### Step 7: Present to User

```markdown
## Stage 7: Prioritization — Complete

### Results

| Metric | Score |
|--------|:-----:|
| Strategic Alignment | {n}/25 — {level} |
| MoSCoW | {category} |
| Value | {n}/10 |
| Effort | {n}/10 |
| Value/Effort Ratio | {n.nn} |
| **Final Priority** | **{Pn} — {label}** |

**Summary:** {1-2 sentence rationale}

**Full assessment:** Updated in `{file_path}`

---

**Your response:**
- (a) **Accept prioritization** — Proceed to Business Case (Stage 8)
- (b) **Challenge ranking** — I disagree with the priority; let's discuss
- (c) **Adjust inputs** — Some factors are scored incorrectly
- (d) **Stop here** — Assessment phase is sufficient; I don't need a full PIP
```

---

### Step 8: Handle Challenges

If user disagrees with priority:
1. Ask which specific scores or classification they challenge
2. Ask what evidence changes the assessment
3. Adjust with transparent logging
4. Recalculate derived values
5. Log: "D-{nnn}: Priority adjusted from {old} to {new}. User override reason: {reason}"

---

### Step 9: Log and Transition

1. **Decision Log:** D-{nnn}: "Prioritization complete. Strategic: {n}/25. MoSCoW: {category}. V/E: {ratio}. Final: {Pn}."
2. **State File:** Stage 7 = ✅ Done; Current Phase = JUSTIFICATION; Current Stage = 8
3. **Lessons Learned (if relevant):** Capture if prioritization revealed misalignment between requestor's perception and objective analysis

Display transition:

```
✅ ASSESSMENT PHASE COMPLETE (Stages 4-7)

📊 Summary:
   • Requirements analyzed: {n} findings ({critical} critical resolved)
   • Feasibility: {score}/100 — {rating}
   • Priority: {MoSCoW} — {Pn} ({label})
   • Decisions logged: {n} this phase
   • Assumptions registered: {n}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next → JUSTIFICATION PHASE
Stage 8: Business Case Development
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'll build the investment case using the feasibility and priority data.

Proceeding...
```

---

## Priority Override Rules

The user ALWAYS has final authority over priority. However:

1. If user upgrades priority without addressing feasibility conditions → log a Risk: "Priority elevated despite unresolved feasibility conditions. Risk of proceeding without mitigation."
2. If user downgrades a "Must Have" with regulatory driver → flag: "Note: regulatory requirements exist regardless of priority classification."
3. All overrides are logged with user's stated rationale — no silent changes.

---

## Portfolio Context (Optional)

If the user provides information about other initiatives competing for resources:

- Factor relative priority into the ranking
- Note: "In context of portfolio: {n} other initiatives competing for same resources"
- Adjust the "urgency" component of the recommendation accordingly
- This is supplementary context, not a formal portfolio management process

---

## Output File

Prioritization results are merged into the Feasibility Assessment document (Section 3) rather than a standalone file:
- Numbered: `{output_root}/02_Screening_Prioritization/Feasibility_Assessment.md` (updated)
- Flat: `{output_root}/pilc-docs/assessment/Feasibility_Assessment.md` (updated)
