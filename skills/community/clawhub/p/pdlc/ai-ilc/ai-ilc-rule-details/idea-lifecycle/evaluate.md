<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 3: Evaluate

**Lead persona:** `#persona-product-manager`
**Sub-role:** `#persona-subrole-financial-analyst` (value scoring, investment framing, cost-of-not-doing)
**Execution:** ALWAYS
**Purpose:** Score the idea consistently against criteria and articulate its strategic value — providing the evidence base for the go/no-go decision.

---

## Why This Stage Exists

Without structured evaluation, ideas are approved (or rejected) on gut feeling, politics, or recency bias. Evaluation provides: a comparable score, a recorded rationale per criterion, and a value analysis that articulates WHY this matters — not just whether it passes a threshold.

---

## Two-Source Evaluation Model

The scoring rubric uses two sources:

1. **Default baseline rubric** (built into this stage) — 7 universal criteria that work for any idea in any domain. Ships as the standard model.
2. **Enterprise customization** (optional) — the organization can override criteria, weights, or thresholds. When present, custom criteria replace the corresponding baseline on a per-criterion basis. When absent, the baseline stands alone.

**Resolution:**
- Enterprise provides custom → use custom
- Enterprise silent on a criterion → use baseline default
- No customization at all → full baseline (still functional)

---

## Depth Adaptation

| Depth | Evaluation Behavior |
|-------|--------------------|
| **Minimal** | Quick score (7 criteria, 1-line rationale each). Skip Value Analysis if score < 25. |
| **Standard** | Full scoring + 4-dimension Value Analysis. One iteration. |
| **Comprehensive** | Full scoring + Value Analysis + competitive positioning + cost-of-delay analysis + stakeholder-impact framing. May iterate. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Read `ilc-state.md` — confirm idea is Shaped, load depth level
2. Load the Idea Statement produced in Stage 2
3. Activate the Financial Analyst sub-role: investment framing, NPV-style thinking, cost-benefit lens

### Step 2: Score Against the 7 Criteria

For each criterion, score 1-5 with a rationale:

| # | Criterion | Question It Answers |
|---|-----------|-------------------|
| 1 | **Problem Clarity** | Is the problem well-defined and unambiguous? |
| 2 | **User Need** | Do real users actually need this, or is it theoretical? |
| 3 | **Strategic Fit** | Does this align with organizational strategy/goals? |
| 4 | **Differentiation** | Is this genuinely new, or does something else already cover it? |
| 5 | **Feasibility** | Can this actually be done with available capabilities? |
| 6 | **Reusability** | Would this work across different contexts/teams/projects? |
| 7 | **Chain Value** | Does this make the broader ecosystem more valuable? |

**Scoring scale:**
| Score | Meaning |
|:-----:|---------|
| 1 | Very weak — significant concerns |
| 2 | Weak — notable gaps or doubts |
| 3 | Adequate — meets minimum bar |
| 4 | Strong — clear positive signal |
| 5 | Excellent — compelling case |

**Present the score table to the user:**

```markdown
## Evaluation Score: {Idea Name}

| Criterion | Score (1-5) | Rationale |
|-----------|:-----------:|-----------|
| Problem Clarity | {n} | {one sentence referencing the shaped content} |
| User Need | {n} | {evidence from shaping} |
| Strategic Fit | {n} | {why it fits or doesn't} |
| Differentiation | {n} | {what exists vs. what's new} |
| Feasibility | {n} | {capability assessment} |
| Reusability | {n} | {breadth of applicability} |
| Chain Value | {n} | {ecosystem contribution} |
| **TOTAL** | **{n}/35** | |

**Band:** {Strong Proceed / Proceed / Conditional / Park / Reject}
```

### Step 3: Check Automatic Blockers

| Blocker | Condition | Action |
|---------|-----------|--------|
| Any criterion = 1 | Single critical weakness | Flag: "Criterion X scored 1 — this must be addressed before proceeding. Can you provide more information or adjust the idea?" |
| Strategic Fit AND Differentiation both ≤ 2 | Doesn't belong and already exists | Recommend Reject with rationale |
| Feasibility ≤ 2 | Can't be done | Recommend Park until conditions change |

### Step 4: Decision Thresholds

| Total Score | Band | Default Decision |
|:-----------:|------|-----------------|
| 30-35 | **Strong Proceed** | Advance — high confidence |
| 25-29 | **Proceed** | Advance — address any low-scoring areas in Scope |
| 20-24 | **Conditional** | Needs rework — return to Shape with specific guidance |
| 15-19 | **Park** | Not ready — revisit when conditions change |
| 7-14 | **Reject** | Doesn't fit — log rationale and close |

### Step 5: Value Analysis (if score ≥ 25)

Produce four dimensions of strategic value:

```markdown
## Value Analysis

### Value to the User
{What does the end user gain? Time saved, risk reduced, quality improved, decisions made easier?}

### Value to the Organization / Ecosystem
{How does this make the org/ecosystem stronger, more complete, or more competitive?}

### Value Differentiators
{What makes this uniquely valuable vs. alternatives (manual process, existing tools, doing nothing)?}

### Cost of NOT Doing This
{What gap persists if this stays unbuilt? What workarounds continue? What risk accumulates?}
```

### Step 6: Present Evaluation to User

```
## Evaluation Complete

📊 Score: {n}/35 — {band}
{blocker warnings if any}

{Score table}

{Value Analysis — if applicable}

**Recommended decision:** {Proceed / Park / Reject}
**Rationale:** {why}

Your call: [Proceed / Park / Reject / Challenge a score / Request deeper analysis]
```

### Step 7: Handle User Response

| Response | Action |
|----------|--------|
| "Proceed" | Continue to Stage 4 (Scope) |
| "Park" | Ask for revisit date; log rationale; close cleanly |
| "Reject" | Log rationale; close cleanly |
| "Challenge score on criterion X" | Re-evaluate that criterion with user's additional context; re-score; re-present |
| "Request deeper analysis" | Upgrade to Comprehensive depth for remaining evaluation; add competitive/cost-of-delay analysis |

### Step 8: Finalize

1. Update `ilc-state.md`:
   - Status: Evaluated
   - Current Stage: 4 (if Proceed) or terminal (if Park/Reject)
   - Score fields populated
2. Update Idea Register: Status = Evaluated, Score = {n}/35
3. Log in Decision Log: "D-{nn} | Evaluation complete. Score: {n}/35, Band: {band}. Decision: {Proceed/Park/Reject}. Rationale: {summary}."

---

## Gate

**Condition to proceed:** User explicitly confirms Proceed (score ≥ 25, no unresolved blockers).

**Early exit paths:**
- Park → State = Parked, workflow pauses cleanly (revisit date logged)
- Reject → State = Rejected, workflow closes cleanly (rationale logged)
- Conditional (20-24) → Return to Shape with guidance on what to improve; re-evaluate after

**Post-gate actions (if Proceed):**
1. Decision logged
2. State updated to Stage 4

---

## Transition Message

```
───────────────────────────────────────────────────────
Moving to Stage 4: SCOPE

The idea passes evaluation. Now let's define boundaries:
what's in for the first version, what's deferred, rough
effort, and key risks.

Activating: Resource Planner lens (WBS-like boundary
setting, effort estimation, dependency mapping)
───────────────────────────────────────────────────────
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Score is borderline (24-25) | Present both options honestly: "This is on the border. Proceeding means accepting that {weak criterion} needs attention during scoping. Parking means revisiting when {condition}. Your call." |
| User disagrees strongly with a score | Don't defend the score — ask what evidence they have. Re-score with their input. The user's context trumps the AI's inference. |
| Enterprise has custom criteria | Load custom criteria if available in workspace config; merge with baseline per two-source model |
| Idea scored 35/35 | Still present the full analysis — a perfect score doesn't skip the gate. User still explicitly confirms. |
| User wants to proceed despite blockers | Flag the risk explicitly: "Proceeding with criterion X at 1 means {specific risk}. If you accept this risk, I'll log it and continue." Log as an accepted risk in Decision Log. |

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*
