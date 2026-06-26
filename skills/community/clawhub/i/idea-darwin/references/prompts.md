# Prompt Templates

Prompt templates for each action. When executing an action, replace variables with actual values and use as a thinking guide.

---

## Universal Template Structure

All action prompts follow this structure:

```
You are the {action_name} module in the "Idea Iteration Incubation System."

Your task is to perform the {action_name} operation on the idea below.

【Current Idea Card】
{idea_card}

【Current Round Context】
- round: {round_id}
- current stage: {stage}
- available budget: {budget_level}
- related ideas: {related_ideas_summary}

【Operation Goal】
{goal_description}

【Operation Requirements】
1. Maintain logical rigor — no vague filler.
2. Preserve the idea's core intent as much as possible.
3. If you spot an obvious flaw, call it out.
4. If generating new ideas, they must have a clear relationship to the original.
5. Output must be structured.
```

---

## Deepen Prompt

```
Perform a "deepen" operation on this idea. This is not a surface rewrite — it's about filling in the logical structure.

Expand from these angles:
1. What problem does it actually solve?
2. Who is the target user?
3. Why does this approach work?
4. What is the minimum viable version?
5. What is the biggest risk?
6. What key assumptions still need validation?

Output:
- Enriched idea description
- Core assumptions
- User scenarios
- MVP version
- Risks and open questions
- Suggested next action
```

---

## Derive Prompt

```
Based on the idea below, derive 2–3 high-quality variants.

Pull apart along these dimensions:
- User segment differences
- Scenario differences
- Business model differences
- Product form differences
- Technical path differences

Requirements:
1. Each variant must retain the original idea's core DNA
2. But must have a clear differentiator
3. Do not generate variants that are merely rephrased duplicates

Output format (per variant):
- Variant title
- Core change point
- Why it's worth keeping
- Relationship to the original idea
```

---

## Cross Prompt

```
Cross-pollinate the two ideas below to find new combined directions.

【Idea A】
{idea_a_card}

【Idea B】
{idea_b_card}

First analyze:
1. What do they have in common?
2. Where do they complement each other?
3. Are there conflicts between them?

Then output:
1. 1–3 new hybrid ideas
2. The core mechanism of each hybrid
3. Why this cross is meaningful
4. The biggest risk
5. Whether it's worth advancing to the next round
```

---

## Critique Prompt

```
Perform a critical review of the idea below.

Focus on:
1. Is it logically consistent?
2. Is it just conceptual packaging with no substance?
3. Does it lack real demand?
4. Is the cost prohibitively high?
5. Is there a simpler alternative?
6. Where is this idea most likely to fail?

Output:
- Core flaws
- Risk level (High / Medium / Low)
- Recommendation: continue or not
- If continuing, what should be fixed first
```

---

## Scoring Prompt

```
Score this idea across 6 dimensions (1–10 each) with reasoning:

- Novelty (weight 0.1): Is there a genuine breakthrough, or just repetition?
- Feasibility (weight 0.2): Is this technically, resource-wise, and path-wise achievable?
- Value (weight 0.2): How much impact would this create if successful?
- Logic (weight 0.2): Is it internally consistent, with no obvious gaps?
- CrossPotential (weight 0.1): How likely is this to spark something new when combined with other ideas?
- Verifiability (weight 0.2): Can we design an experiment or minimum validation path?

Then calculate:
Survival = 0.10×Novelty + 0.20×Feasibility + 0.20×Value + 0.20×Logic + 0.10×CrossPotential + 0.20×Verifiability

Output as JSON:
{
  "novelty": 0,
  "feasibility": 0,
  "value": 0,
  "logic": 0,
  "cross_potential": 0,
  "verifiability": 0,
  "survival_score": 0.0,
  "reasoning": {
    "novelty": "...",
    "feasibility": "...",
    "value": "...",
    "logic": "...",
    "cross_potential": "...",
    "verifiability": "..."
  },
  "suggested_action": "deepen / derive / cross / critique / dormant"
}
```

---

## Validation Prompt

```
Run a two-layer validation check on this idea.

【Layer 1: Fatal Flaw Check】
Answer these 4 questions (Yes/No + reasoning):
1. Does it have a logical flaw? (Is the core assumption self-contradictory or clearly invalid?)
2. Does it lack real demand? (Is there no identifiable target user or use case?)
3. Is it completely infeasible? (Are there insurmountable barriers in technology/resources/path?)
4. Is it a near-duplicate of an existing idea? (Is it just a rephrased version?)

If any answer is Yes, mark validated: false with a brief explanation.

【Layer 2: Value Judgment】(only if Layer 1 is all No)
1. Is it worth continuing to invest resources?
2. What should the next action be?
3. What is the current biggest risk?

Output as JSON:
{
  "hard_check": {
    "logic_flaw": {"result": "Yes/No", "reason": "..."},
    "no_real_demand": {"result": "Yes/No", "reason": "..."},
    "not_feasible": {"result": "Yes/No", "reason": "..."},
    "duplicate": {"result": "Yes/No", "reason": "..."}
  },
  "validated": true/false,
  "value_judgment": {
    "worth_continuing": "Yes/No",
    "next_action": "...",
    "biggest_risk": "..."
  }
}
```

---

## Round Report Template

```markdown
# Round {round_id} Report

## Summary
- Timestamp: {timestamp}
- Total ideas in pool: {total} (active {active} / dormant {dormant})
- Ideas processed this round: {processed}
- New ideas generated: {new_count}

## Actions Taken

| Idea ID | Title | Action | Result Summary |
|---|---|---|---|
| IDEA-XXXX | ... | deepen | ... |

## Newly Generated Ideas

| Idea ID | Title | Source | Initial Priority |
|---|---|---|---|
| IDEA-XXXX | ... | derived from IDEA-XXXX | 6.5 |

## Top 5 Score Changes

| Idea ID | Title | Priority Change | Reason |
|---|---|---|---|
| IDEA-XXXX | ... | +1.2 | Logic more complete after deepening |

## Failed Validation (User Decision Required)

| Idea ID | Title | Failure Reason | Suggested Action |
|---|---|---|---|
| IDEA-XXXX | ... | Near-duplicate of IDEA-XXXX | Merge or dormant |

## Recommendations for Next Round
- Priority processing: IDEA-XXXX, IDEA-XXXX
- Suggested cross: IDEA-XXXX × IDEA-XXXX
- Watch: IDEA-XXXX unchanged for 3 consecutive rounds
```
