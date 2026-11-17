<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Feasibility Assessment

## Stage: 6 of 16
## Phase: 🟠 ASSESSMENT
## Execution: ALWAYS

---

## Purpose

Score the initiative across four feasibility dimensions (Technical, Operational, Financial, Schedule), produce a weighted overall score, assign a feasibility rating, and list conditions that must be met before proceeding. This assessment provides the evidence base for the Business Case and informs whether the initiative should proceed, pause, or be rejected.

---

## MANDATORY: Stage Sub-Role — Risk Analyst

During THIS stage, ALSO adopt the mindset of a **Risk Analyst**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Score each dimension from evidence; when information is unknown, score conservatively (lower), not optimistically
- For every low score, identify the specific risk it represents and the condition that would mitigate it
- Treat each assumption behind a score as a risk if it proves false — note it
- Frame "conditions to proceed" as observable risk triggers, not vague hopes

### Anti-Patterns for This Stage
- Do NOT inflate scores to make the initiative look viable — score what's evidenced
- Do NOT score everything "medium/3" to avoid taking a defensible position

### Quality Check
A good output at this stage sounds like:
- "Technical feasibility scored 2/5 — driven by unproven integration X; condition to proceed: successful PoC by Week 3..."

---

## Step-by-Step Execution

### Step 1: Load Context

1. Read the Requirement Intake Form (Stage 3)
2. Read the Requirements Analysis Report (Stage 4)
3. Read Clarification outcomes (Stage 5, if executed)
4. Review Assumptions & Dependencies register
5. Note the workflow depth — this affects commentary detail, not scoring rigor

---

### Step 2: Score Technical Feasibility

Assess four criteria, each scored 1-5:

| Criteria | 1 (Very Low) | 2 (Low) | 3 (Medium) | 4 (High) | 5 (Very High) |
|----------|-------------|---------|-----------|----------|--------------|
| **Technology readiness** | Requires unproven/experimental tech | Some novel components; limited track record | Mix of proven and newer technologies | Mostly mature, well-established tech | All technology proven and widely deployed |
| **Integration complexity** | >10 external integrations, undocumented APIs | 6-10 integrations, some unclear | 3-5 integrations, mostly documented | 1-2 simple integrations | Standalone or trivial integrations |
| **Infrastructure availability** | No infrastructure exists; major procurement needed | Significant gaps; long-lead procurement | Some infrastructure available; gaps manageable | Mostly available; minor additions | Fully available and ready |
| **Skills/expertise available** | No internal capability; must build from scratch | Major skill gaps; heavy recruitment needed | Some skills present; targeted hiring needed | Most skills available; minor gaps | Full team with proven expertise |

**Scoring guidance:**
- Score based on CURRENT state, not aspirational
- If information is unknown, score conservatively (lower)
- Note evidence for each score in the Comments column

**Output format:**

```markdown
### Technical Feasibility
| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Technology readiness | {n} | {Evidence/rationale} |
| Integration complexity | {n} | {Evidence/rationale} |
| Infrastructure availability | {n} | {Evidence/rationale} |
| Skills/expertise available | {n} | {Evidence/rationale} |
| **Technical Score** | **{sum}/20** | {Summary sentence} |
```

---

### Step 3: Score Operational Feasibility

| Criteria | 1 (Very Low) | 2 (Low) | 3 (Medium) | 4 (High) | 5 (Very High) |
|----------|-------------|---------|-----------|----------|--------------|
| **Process change impact** | Fundamental org restructure required | Major process redesign across departments | Significant changes to existing workflows | Moderate adaptation of current processes | Minimal change; fits existing operations |
| **User adoption risk** | Hostile user base; strong resistance expected | Significant resistance; major change mgmt needed | Moderate resistance; structured training required | Mild disruption; users generally supportive | Seamless adoption; users are requesting this |
| **Organizational readiness** | No sponsorship; competing priorities dominate | Weak sponsorship; organization distracted | Sponsorship exists but attention divided | Strong sponsorship; organization aware and supportive | Executive champion; organization eager |
| **Training requirements** | Entire workforce needs extensive reskilling | Large user base needs significant training | Multiple roles need structured training | Targeted training for key users | Minimal training; intuitive or familiar |

**Output format:**

```markdown
### Operational Feasibility
| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Process change impact | {n} | {Evidence/rationale} |
| User adoption risk | {n} | {Evidence/rationale} |
| Organizational readiness | {n} | {Evidence/rationale} |
| Training requirements | {n} | {Evidence/rationale} |
| **Operational Score** | **{sum}/20** | {Summary sentence} |
```

---

### Step 4: Score Financial Feasibility

| Criteria | 1 (Very Low) | 2 (Low) | 3 (Medium) | 4 (High) | 5 (Very High) |
|----------|-------------|---------|-----------|----------|--------------|
| **Budget availability** | No budget; no funding path visible | Budget not allocated; requires new approval cycle | Budget possible but not yet confirmed | Budget provisionally allocated; approval likely | Budget confirmed and available |
| **ROI potential** | No measurable return; pure cost | Marginal return; payback >5 years | Moderate return; payback 2-4 years | Strong return; payback 1-2 years | Exceptional return; payback <1 year |
| **Cost certainty** | Cannot estimate; too many unknowns | Wide estimate range (±50%+); high uncertainty | ROM available (±30%); manageable uncertainty | Good estimates (±15%); most costs understood | Firm estimates (<±10%); well-understood costs |
| **Funding approval likelihood** | Very unlikely; no sponsor support | Unlikely without significant justification | Possible with strong business case | Likely; sponsor supportive; precedent exists | Almost certain; pre-approved or committed |

**Output format:**

```markdown
### Financial Feasibility
| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Budget availability | {n} | {Evidence/rationale} |
| ROI potential | {n} | {Evidence/rationale} |
| Cost certainty | {n} | {Evidence/rationale} |
| Funding approval likelihood | {n} | {Evidence/rationale} |
| **Financial Score** | **{sum}/20** | {Summary sentence} |
```

---

### Step 5: Score Schedule Feasibility

| Criteria | 1 (Very Low) | 2 (Low) | 3 (Medium) | 4 (High) | 5 (Very High) |
|----------|-------------|---------|-----------|----------|--------------|
| **Timeline realism** | Stated timeline is physically impossible | Very aggressive; would require exceptional circumstances | Tight but achievable with strong execution | Reasonable with buffer for normal issues | Conservative; comfortable margin |
| **Resource availability timing** | Team won't be available for 6+ months | 3-6 month lead time to assemble team | 1-3 months to ramp; manageable | Team mostly available within weeks | Team ready now |
| **Dependency alignment** | Critical dependencies uncontrolled and unscheduled | Key dependencies exist with uncertain timelines | Dependencies identified; alignment being planned | Dependencies managed; timelines aligned | No blocking dependencies; self-contained |
| **Regulatory/deadline pressure** | Hard external deadline already at risk | Hard deadline exists; schedule is tight | Soft deadline; some flexibility | No hard deadline; business-driven timing | Entirely flexible timing |

**Output format:**

```markdown
### Schedule Feasibility
| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Timeline realism | {n} | {Evidence/rationale} |
| Resource availability timing | {n} | {Evidence/rationale} |
| Dependency alignment | {n} | {Evidence/rationale} |
| Regulatory/deadline pressure | {n} | {Evidence/rationale} |
| **Schedule Score** | **{sum}/20** | {Summary sentence} |
```

---

### Step 6: Calculate Overall Feasibility Score

Apply weighted scoring:

| Dimension | Score | Weight | Weighted Score |
|-----------|:-----:|:------:|:--------------:|
| Technical | {x}/20 | 30% | {x × 1.5} |
| Operational | {x}/20 | 25% | {x × 1.25} |
| Financial | {x}/20 | 25% | {x × 1.25} |
| Schedule | {x}/20 | 20% | {x × 1.0} |
| **Total** | | | **{sum}/100** |

**Weight rationale:**
- Technical (30%) — most common source of project failure; hardest to recover from
- Operational (25%) — adoption failure wastes entire investment
- Financial (25%) — no money = no project
- Schedule (20%) — timeline pressure is real but most negotiable dimension

---

### Step 7: Assign Feasibility Rating

| Score Range | Rating | Symbol | Meaning |
|:-----------:|--------|:------:|---------|
| 80-100 | Highly Feasible | 🟢 | Proceed with confidence; standard project management sufficient |
| 60-79 | Feasible with Conditions | 🟡 | Proceed but address specific conditions; enhanced monitoring |
| 40-59 | Challenging | 🟠 | Significant mitigation required before proceeding; consider phasing or scope reduction |
| 0-39 | Not Feasible (current form) | 🔴 | Do not proceed as-is; fundamental rethink, rescoping, or rejection needed |

---

### Step 8: Define Conditions for Proceeding

For ratings 🟡, 🟠, or 🔴, list the conditions that must be addressed:

```markdown
## Conditions for Proceeding

| # | Condition | Owner | Target Date | Blocking? |
|---|-----------|-------|:-----------:|:---------:|
| 1 | {Specific condition — what must be true} | {Role/name} | {When} | {Yes/No} |
| 2 | {Condition} | {Owner} | {When} | {Yes/No} |
```

**Condition types:**
- **Blocking** — must be resolved before Business Case (Stage 8) can be approved
- **Non-blocking** — should be resolved before Charter (Stage 9) or Planning

For each condition, also create an Action Item in the register.

---

### Step 9: Produce the Feasibility Assessment Document

Using template `templates/feasibility-assessment.md`, produce the full document with:

1. Header (project, assessor, date, request ID)
2. Section 1: Feasibility Dimensions (four scored tables with comments)
3. Section 2: Overall Feasibility Score (weighted calculation table + rating)
4. Section 3: Prioritization (populated in Stage 7 — leave placeholder for now)
5. Section 4: Conditions for Proceeding (if applicable)
6. Section 5: Recommendation (Approve / Approve with Conditions / Hold / Reject)

---

### Step 10: Formulate Recommendation

Based on the rating:

| Rating | Recommendation |
|--------|---------------|
| 🟢 Highly Feasible | "Approve — proceed to Business Case development" |
| 🟡 Feasible with Conditions | "Approve with Conditions — proceed to Business Case subject to conditions in Section 4" |
| 🟠 Challenging | "Hold — address conditions before proceeding. Consider scope reduction or phased approach." |
| 🔴 Not Feasible | "Reject in current form — recommend fundamental rescoping, alternative approach, or cancellation." |

**Important:** For 🟠 and 🔴 ratings, present options to the user:

```markdown
### Q-ASS-{nn}: Path Forward

**Context:** Feasibility score is {score}/100 ({rating}). The initiative faces significant challenges in its current form.

**Options:**
- (a) **Proceed anyway** — Accept higher risk; business imperative overrides feasibility concerns
- (b) **Reduce scope** — Remove high-risk elements; improve feasibility with smaller first delivery
- (c) **Phase the delivery** — Split into a feasible Phase 1 and a deferred Phase 2
- (d) **Pause** — Address conditions first; return when conditions are met
- (e) **Cancel** — Do not proceed with this initiative

**Recommended:** {Based on specifics}
**Rationale:** {Why}
```

---

### Step 11: Present to User

```markdown
## Stage 6: Feasibility Assessment — Complete

### Overall Score: {score}/100 — {rating_symbol} {rating_name}

| Dimension | Score | Rating |
|-----------|:-----:|:------:|
| Technical | {x}/20 | {commentary} |
| Operational | {x}/20 | {commentary} |
| Financial | {x}/20 | {commentary} |
| Schedule | {x}/20 | {commentary} |

### Recommendation: {recommendation_summary}

{If conditions exist: "Subject to {n} conditions — see full document."}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Accept assessment** — Proceed to Prioritization (Stage 7)
- (b) **Challenge scores** — I disagree with specific ratings; let's discuss
- (c) **Adjust scope** — I want to modify scope to improve feasibility
- (d) **Stop here** — This assessment is the final output needed
```

---

### Step 12: Handle User Challenges

If user disagrees with scores:
1. Ask which specific criteria they challenge
2. Ask what evidence or context changes the score
3. Adjust if user provides valid information the AI didn't have
4. Log adjustment in Decision Log: "D-{nnn}: Feasibility score for {criteria} adjusted from {old} to {new}. Reason: {user's input}"
5. Recalculate weighted total
6. Re-present summary

---

### Step 13: Log and Transition

1. **Decision Log:** D-{nnn}: "Feasibility assessment complete. Score: {x}/100 ({rating}). Recommendation: {proceed/conditions/hold/reject}."
2. **Assumptions Register:** Add any assumptions made during scoring
3. **State File:** Stage 6 = ✅ Done; Current Stage = 7
4. **Lessons Learned (if applicable):** Note if scoring revealed unexpected issues

Transition to Stage 7 (Prioritization).

---

## Scoring Integrity Rules

1. **Evidence-based** — every score must cite evidence from requirements, source, or user input
2. **Conservative on unknowns** — if information is missing, score lower (not middle)
3. **No inflation** — don't score favorably just because the user is enthusiastic
4. **No deflation** — don't score low to appear rigorous; be accurate
5. **Adjustable** — user can challenge any score with evidence; adjust transparently
6. **Logged** — all scores and their rationale are permanently recorded
7. **Comparable** — same project scored twice should get similar results (methodology is repeatable)

---

## Output File

Save to:
- Numbered: `{output_root}/02_Screening_Prioritization/Feasibility_Assessment.md`
- Flat: `{output_root}/pilc-docs/assessment/Feasibility_Assessment.md`
