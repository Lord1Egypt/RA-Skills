---
name: Jupiter
description: >
  Compute the best path when multiple choices compete.
  Designed for routing logic across vendors, investments, execution options,
  and strategic decisions where the goal is best-fit path selection.
version: 1.0.0
---

# Jupiter

> **When choices multiply, bad decisions usually come from bad routing.**

Jupiter is a gravity center for best-path decision making.

This skill is designed for moments when the user is not missing options —  
they are drowning in them.

Most people fail multi-option decisions for one of three reasons:

1. they do not define what “best” actually means  
2. they compare options at the surface instead of at the tradeoff level  
3. they confuse the loudest option with the strongest route

Jupiter exists to reduce fragmented decision-making and compute the path that best fits the real objective.

---

## What Jupiter Is For

Use this skill when you need to choose between multiple viable paths, such as:

- several vendors competing for the same budget
- several suppliers with different speed / trust / cost tradeoffs
- multiple investment candidates with different upside and fragility profiles
- multiple product directions competing for the same team focus
- several partnership opportunities that cannot all be pursued at once
- several execution paths where only one has the cleanest long-term profile

This skill is especially useful when:
- the user already has 3-10 options
- each option looks “good enough”
- the real problem is not idea generation but route ranking
- the wrong decision would come from hidden tradeoffs, not lack of choice

---

## What This Skill Does

Jupiter helps:
- force clarity on the true objective function
- compare options under real constraints
- identify which option only looks good on the surface
- expose hidden tradeoffs and fragility
- rank routes by fit, not hype
- recommend the strongest route and the best fallback route

Jupiter does **not** assume the cheapest option is best,  
the fastest option is best,  
or the highest-upside option is best.

It assumes the best route is the one that best matches the objective under real-world constraints.

---

## What This Skill Does NOT Do

This skill does NOT:
- execute trades
- connect to APIs, wallets, or vendors
- provide regulated investment advice
- replace fiduciary, legal, or tax judgment
- generate endless new options when the real problem is selection discipline

---

## Core Routing Framework

Jupiter evaluates routes using six core lenses.

### 1. Objective Fit
How directly does this option serve the actual goal?

Examples:
- if the goal is speed, does this route actually shorten time-to-result?
- if the goal is downside protection, does this route reduce fragility?
- if the goal is quality, is the route truly quality-dominant or just premium-priced?

### 2. Constraint Compatibility
How well does the option fit real constraints?

Examples:
- budget ceiling
- time pressure
- trust requirements
- operational burden
- approval complexity
- switching costs

### 3. Tradeoff Clarity
What is being sacrificed if this route is chosen?

A good route has visible tradeoffs.  
A bad route hides them until after commitment.

### 4. Execution Simplicity
Can this route actually be executed cleanly?

Many “best” options fail because they require:
- too many dependencies
- too much coordination
- too much behavior change
- too much fragile optimism

### 5. Fragility Risk
How likely is this route to fail when pressure hits?

Fragile routes often depend on:
- one person
- one platform
- one assumption
- one supplier
- one ideal scenario

### 6. Reversibility
If this route is wrong, how expensive is it to recover?

Reversible routes are often underrated.  
Irreversible routes should clear a higher bar.

---

## Standard Output Format

JUPITER ROUTING ASSESSMENT  
━━━━━━━━━━━━━━━━━━━━━━━━━━  
Decision Type: [What is being chosen]  
Primary Objective: [What “best” means here]

OPTION MAP  
━━━━━━━━━━━━━━━━━━━━━━━━━━  
1. [Option A] — [what it is]  
2. [Option B] — [what it is]  
3. [Option C] — [what it is]

ROUTE RANKING  
━━━━━━━━━━━━━━━━━━━━━━━━━━  
Best Route: [Chosen path]  
Second Route: [Fallback path]  
Weakest Route: [Most structurally weak path]

WHY THE BEST ROUTE WINS  
━━━━━━━━━━━━━━━━━━━━━━━━━━  
- [Objective-fit reason]
- [Constraint-fit reason]
- [Tradeoff advantage]
- [Execution or reversibility advantage]

HIDDEN WEAKNESSES  
━━━━━━━━━━━━━━━━━━━━━━━━━━  
⚠️ [Option that looks attractive but routes poorly]  
⚠️ [Option with hidden dependency]  
⚠️ [Option mismatched to actual objective]

TRADEOFFS  
━━━━━━━━━━━━━━━━━━━━━━━━━━  
- [What is sacrificed for the chosen route]
- [What still needs validation]
- [What could change the ranking]

RECOMMENDED NEXT STEP  
━━━━━━━━━━━━━━━━━━━━━━━━━━  
- [What to choose, test, validate, or negotiate next]

---

## Example Scenarios

### Example 1: Vendor Selection
A startup has 4 vendors for outbound lead enrichment.

- Vendor A is cheapest but slow and thin on support
- Vendor B is expensive but proven
- Vendor C is fast but immature
- Vendor D is balanced but weaker internationally

Jupiter should not ask “which is best in general?”  
It should ask:

- Is the startup optimizing for cost, reliability, speed, or scale?
- Is this a test phase or a long-term stack decision?
- How painful is switching later?
- Which option is robust under actual usage, not just in a demo?

### Example 2: Investment Shortlist
An operator is comparing 3 possible allocations:

- one has the highest upside
- one has the most liquidity
- one has the cleanest downside profile

Jupiter should route based on:
- whether the user wants upside, preservation, or optionality
- how much volatility or illiquidity is acceptable
- whether reversibility matters more than maximum gain

### Example 3: Strategic Product Focus
A founder has 3 product directions:

- enterprise feature set
- creator workflow tool
- API-first infrastructure

All three have some merit.  
Jupiter should identify:
- which route best matches current team capability
- which route fits current go-to-market reality
- which route has the cleanest path from now to traction
- which route is mostly “exciting in theory”

---

## Common Routing Mistakes

Jupiter should actively resist these mistakes:

### Mistake 1: Comparing Features Instead of Routes
Users often compare lists of features instead of the full path:
- adoption burden
- integration pain
- switching costs
- hidden complexity

### Mistake 2: Letting the Objective Stay Vague
If “best” is undefined, ranking becomes performance art.

### Mistake 3: Overweighting Upside, Underweighting Execution
A route with massive upside but poor executability is often weaker than it appears.

### Mistake 4: Treating More Options as More Freedom
Past a certain point, more options mostly create noise.

### Mistake 5: Ignoring Reversibility
An option that is slightly weaker but easy to reverse may dominate a stronger but sticky mistake.

---

## When NOT to Use Jupiter

Do not use this skill when:
- there is only one realistic option
- the user needs broad ideation rather than decision routing
- the user wants emotional reassurance instead of tradeoff analysis
- the user has not defined any objective or constraints at all
- the user needs regulated financial, legal, procurement, or fiduciary approval

---

## Execution Protocol (for AI agents)

When user asks for route comparison or option selection, follow this sequence:

### Step 1: Parse the choice set
Extract:
- available options
- objective
- constraints
- risk tolerance
- time sensitivity
- reversibility needs
- what failure would look like

### Step 2: Clarify the objective function
Determine whether “best” means:
- lowest risk
- highest upside
- strongest trust
- fastest speed
- highest reliability
- cleanest long-term path
- best value under budget

If objective is vague, say so and force clarification.

### Step 3: Compare each route
Review each option for:
- objective fit
- constraint compatibility
- hidden tradeoffs
- execution burden
- fragility
- reversibility

### Step 4: Rank the paths
Return:
- best route
- fallback route
- weakest route
- why the best route wins under current assumptions

### Step 5: State uncertainty honestly
If the ranking depends on unknown inputs:
- list them clearly
- do not fake certainty
- explain what additional data would most change the decision

---

## Activation Rules (for AI agents)

### Use this skill when the user asks about:
- best path selection
- comparing multiple options
- vendor comparison
- supplier routing
- opportunity ranking
- route optimization
- strategic choice under constraints
- “which of these should I choose?”

### Do NOT use this skill when:
- the user wants direct execution
- the user needs regulated investment advice
- the user wants pure brainstorming instead of route selection
- there are no meaningful alternatives to compare

### If context is ambiguous
Ask:
"Do you want help selecting the best route among multiple options, or are you looking for broader ideation?"

---

## Boundaries

This skill supports structured route selection and option comparison.

It does not replace:
- legal advice
- tax advice
- fiduciary or regulated investment advice
- procurement sign-off
- direct execution
