<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 9: Portfolio Rebalancing

**Phase:** Optimization
**Purpose:** When portfolio conditions change (new data, new project, crisis, completed project), reassess priorities and rebalance the portfolio. This is the adaptive engine's core loop — the portfolio is never static.

---

## MANDATORY: Stage Sub-Role — Risk Analyst

During THIS stage, ALSO adopt the mindset of a **Risk Analyst**. This does NOT replace your primary role (Portfolio Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Identify what changed and WHY it matters to the portfolio
- Assess cascading impact: "If we pause X, what happens to Y and Z?"
- Challenge status quo: "Should the current ranking still hold given new information?"
- Think in terms of portfolio resilience: can the portfolio absorb this shock?

### Anti-Patterns for This Stage
- Do NOT rebalance without stating the trigger (what changed?)
- Do NOT change rankings without showing the before/after delta

### Quality Check
A good rebalancing sounds like:
- "Trigger: Project B's budget overrun (+40%) consumes capacity allocated to Project C. Recommended action: Pause Project C (rank #5, lowest strategic alignment at 12/25) to redirect $80K and 2 FTEs to Project B (rank #2, on critical regulatory deadline). Impact: C slips 8 weeks. Alternative: absorb overrun from contingency (exhausts 60% of portfolio reserve)."

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Identify trigger, re-check top 3, propose one action. Quick decision. |
| **Standard** | Full re-scoring if needed, cascade analysis, formal rebalancing proposal. |
| **Comprehensive** | Full re-scoring + what-if scenario comparison (Extension E2) + financial impact model (E6). |

---

## Step-by-Step Execution

### Step 9.1: Identify Rebalancing Trigger

Why are we rebalancing? State explicitly:

| Trigger Type | Example |
|---|---|
| **New project admitted** | "Project D entered at rank #2 — displaces existing schedule" |
| **Health deterioration** | "Project B went 🔴 — budget overrun + velocity drop" |
| **Project completion** | "Project A finished — capacity freed for reallocation" |
| **External change** | "Market shift — strategic objective #3 now urgent" |
| **Scheduled review** | "Quarterly strategic portfolio review" |
| **User request** | "User wants to reassess the portfolio" |
| **Resource crisis** | "Key team member departed — affects 3 projects" |

```
📋 Rebalancing triggered by: {trigger description}
   Impact scope: {which projects are affected}
   Last prioritization: {date} — {days} ago
```

### Step 9.2: Resurface Current State

Show the current portfolio ranking and health:

```
Current portfolio state:
| Rank | Project | Score | State | Health | Since Last Review |
|:----:|---------|:-----:|:-----:|:------:|-------------------|
| 1 | {A} | 84 | Active | 🟢 | No change |
| 2 | {B} | 74 | Active | 🔴 | ⬇️ Was 🟢 |
| 3 | {C} | 52 | Active | 🟢 | No change |
| 4 | {D} | — | New | ⚪ | Just registered |
```

### Step 9.3: Assess Impact

For the trigger identified, analyze:

1. **Direct impact:** What does this change about affected project(s)?
2. **Cascade impact:** What does this mean for other projects? (shared resources, dependencies, budget)
3. **Portfolio-level impact:** Does this change the overall health ratio, budget trajectory, or strategic balance?

```
📊 Impact analysis:

Direct: {what changed for the affected project}
Cascade: {what this means for {N} other projects}
Portfolio: {effect on overall health/budget/balance}
```

### Step 9.4: Determine Action Needed

| Possible Actions | When |
|---|---|
| **No change** | Trigger is informational; current ranking still holds |
| **Re-score affected projects** | Scores may have changed (e.g., urgency increased, risk increased) |
| **Full re-prioritization** | Multiple projects affected; ranking may have shifted |
| **Governance action needed** | Pause/retire/accelerate a specific project |
| **Constraint adjustment** | Change budget ceiling, timeline, or team allocation |
| **Capacity reallocation** | Move resources from lower-priority to higher-priority |

```
Q-{NN}: What level of rebalancing is appropriate?

(a) No change needed — acknowledge trigger, maintain current ranking
(b) Re-score affected project(s) only — limited re-prioritization
(c) Full re-prioritization — all projects rescored (returns to Stage 4)
(d) Governance action — specific decision needed (routes to Stage 5)
(e) Let me see the options compared (what-if analysis — requires Extension E2)

Recommended: {option}
Rationale: {why}
```

### Step 9.5: Execute Rebalancing

**If re-scoring:**
- Return to Stage 4 scoring for affected projects only
- Show before/after comparison
- Highlight rank changes

**If governance action:**
- Route to Stage 5 for specific project decision
- Pre-fill the governance question with rebalancing context

**If constraint adjustment:**
- Update the dispatch authorization for affected project(s)
- Notify (via record) that constraints changed post-dispatch

### Step 9.6: Produce Rebalancing Proposal

Generate `rebalancing-proposal-{date}.md`:

```markdown
---
generatedBy: AI-PPM
generatedVersion: 1.0.0
source: portfolio-governance
generatedOn: {ISO-date}
ownership: generated
---

# Rebalancing Proposal — {date}

## Trigger
{What changed and why it matters}

## Impact Analysis
- **Direct:** {affected project(s)}
- **Cascade:** {other projects impacted}
- **Portfolio-level:** {overall health/budget/balance effect}

## Recommended Actions

| # | Action | Project | Effect | Risk |
|---|--------|---------|--------|------|
| 1 | {action} | {project} | {what changes} | {risk of this action} |
| 2 | {action} | {project} | {what changes} | {risk of this action} |

## Before/After Comparison

| Project | Before (Rank/Score) | After (Rank/Score) | Change |
|---------|:-------------------:|:------------------:|:------:|
| {A} | #1 / 84 | #1 / 84 | — |
| {B} | #2 / 74 | #3 / 68 | ⬇️ -1 |
| {D} | New | #2 / 76 | ⬆️ New entry |

## Decision Required
{What the portfolio manager needs to approve}
```

### Step 9.7: Confirm & Apply

```
📋 Rebalancing proposal ready.

Summary: {one-line summary of proposed changes}
Projects affected: {N}
Rank changes: {list}
Governance actions needed: {Yes (→ Stage 5) / No}

Apply this rebalancing? [Yes / Modify / Reject — keep current state]
```

If governance actions needed → route to Stage 5.

---

## Gate

User approves the rebalancing proposal → changes applied to register and state.

---

## Outputs

| Artifact | Status |
|---|---|
| Rebalancing proposal document | Created |
| `portfolio-register.md` | Updated (if ranks changed) |
| `prioritization-scorecard.md` | Updated (if re-scored) |
| `ppm-state.md` | Updated (last rebalanced date, session history) |

---

## Management Framework Contribution

Entry: `PPM-C-{NNN}: Portfolio rebalanced. Trigger: {trigger}. Changes: {summary}. {N} projects re-ranked.`

---

## Extension Check — What-If Scenarios (E2)

If Extension E2 is active:
- Before committing to a rebalancing action, present 2-3 scenario comparisons
- "Scenario A: Pause C → B gets resources. Scenario B: Absorb from contingency. Scenario C: Accept delay on B."
- User selects preferred scenario → that becomes the rebalancing action

---

*This stage runs whenever the portfolio needs adjustment — triggered by anomalies, new entries, reviews, or crises.*
