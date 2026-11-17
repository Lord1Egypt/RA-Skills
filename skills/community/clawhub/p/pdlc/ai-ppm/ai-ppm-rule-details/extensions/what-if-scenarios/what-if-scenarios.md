<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension E2: What-If Scenario Modeling

**Stages affected:** 9 (Portfolio Rebalancing)
**Adds:** Scenario comparison, trade-off analysis, impact prediction, sensitivity check

---

## Additional Steps for Stage 9 (replaces Step 9.5 with expanded flow)

### Step 9.E2.1: Define Scenarios

Present 2-4 alternative portfolio compositions based on the rebalancing trigger:

```markdown
## Scenario Definition

### Scenario A: {Name — e.g., "Prioritize revenue projects"}
- {Action 1}: {e.g., Pause Project C, redirect resources to Project A}
- {Action 2}: {e.g., Accelerate Project B timeline by 4 weeks}
- Philosophy: {what this scenario optimizes for}

### Scenario B: {Name — e.g., "Minimize risk"}
- {Action 1}: {e.g., Keep current ranking, absorb overrun from contingency}
- {Action 2}: {e.g., Reduce Project B scope to fit budget}
- Philosophy: {what this scenario optimizes for}

### Scenario C: {Name — e.g., "Maximum throughput"}
- {Action 1}: {e.g., Run all projects but at reduced velocity}
- {Action 2}: {e.g., Accept 3-month delay on lowest priority}
- Philosophy: {what this scenario optimizes for}
```

### Step 9.E2.2: Compare Scenarios Side-by-Side

```markdown
## Scenario Comparison

| Dimension | Current State | Scenario A | Scenario B | Scenario C |
|-----------|:------------:|:----------:|:----------:|:----------:|
| Active projects | {N} | {N} | {N} | {N} |
| Capacity utilization | {pct}% | {pct}% | {pct}% | {pct}% |
| Budget committed | ${X} | ${Y} | ${Z} | ${W} |
| Avg. strategic alignment | {score} | {score} | {score} | {score} |
| Projects on schedule | {N}/{total} | {N}/{total} | {N}/{total} | {N}/{total} |
| Estimated completion (all) | {date} | {date} | {date} | {date} |
| Risk level | {assessment} | {assessment} | {assessment} | {assessment} |
```

### Step 9.E2.3: Trade-Off Analysis

For each scenario, explicitly state gains and losses:

```markdown
## Trade-Off Analysis

### Scenario A: {Name}
| ✅ Gains | ❌ Losses |
|----------|----------|
| {gain 1} | {loss 1} |
| {gain 2} | {loss 2} |

### Scenario B: {Name}
| ✅ Gains | ❌ Losses |
|----------|----------|
| {gain 1} | {loss 1} |
| {gain 2} | {loss 2} |
```

### Step 9.E2.4: Sensitivity Check

Identify which assumptions, if wrong, would change the recommendation:

```markdown
## Sensitivity Analysis

| Assumption | Current Belief | If Wrong... | Scenario Affected |
|---|---|---|---|
| {e.g., "Team X available by Q3"} | {confident} | {Scenario A becomes unviable} | A |
| {e.g., "Market window closes Dec"} | {moderate} | {Urgency of B drops — C becomes preferred} | B, C |
| {e.g., "Budget ceiling stays at $2M"} | {uncertain} | {All scenarios need re-scoping} | All |

**Fragile assumptions:** {list assumptions that, if wrong, flip the recommendation}
**Robust recommendation:** Scenario {X} holds under most assumption changes
```

### Step 9.E2.5: Present Recommendation

```
📊 Scenario Analysis Complete

| Scenario | Optimizes For | Trade-Off | Robustness |
|----------|--------------|-----------|:----------:|
| A: {name} | {what} | {key loss} | {High/Med/Low} |
| B: {name} | {what} | {key loss} | {High/Med/Low} |
| C: {name} | {what} | {key loss} | {High/Med/Low} |

Recommended: Scenario {X}
Rationale: {why — references comparison + sensitivity}
Fragile if: {key assumption that could invalidate}

Select a scenario: [A / B / C / Modify / Need different options]
```

Selected scenario becomes the rebalancing action (continues to Step 9.6 in core flow).

---

*This extension replaces gut-feel rebalancing with structured scenario comparison — essential for high-stakes portfolio decisions.*
