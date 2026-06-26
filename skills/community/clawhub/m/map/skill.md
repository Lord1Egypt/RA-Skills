---
name: Map
description: >
  Turn complex business goals into navigable strategic maps.
  Identify milestones, resource nodes, risk points, bottlenecks, and route logic
  so users can see the terrain before they move.
version: 1.0.0
---

# Map

> **Most strategic failure comes from moving before the terrain is visible.**

Map is a strategic cartographer for complex goals.

This skill is built for situations where the user is not missing ambition —
they are missing a reliable way to see the path.

Map does not generate a geographic map.
It generates a logic map:
- where the goal sits
- what must be crossed first
- where the risks are
- where the leverage is
- what milestones define progress
- what dependencies make movement possible or dangerous

Use this skill when you need to:
- break a complex goal into a navigable path
- visualize strategic dependencies before execution
- identify risk zones, resource nodes, and milestone sequence
- turn a vague ambition into a route with structure
- see whether the goal has one critical path or multiple viable paths
- reduce chaos before committing time, capital, or team focus

This skill does NOT:
- execute project management
- replace legal, financial, or operational sign-off
- guarantee that the chosen route will succeed
- act as a Gantt chart or task manager
- replace domain expertise where the terrain itself is poorly understood

---

## What This Skill Does

Map helps:
- convert abstract goals into structured route logic
- identify the critical path and optional side paths
- surface resource requirements before action begins
- expose bottlenecks, constraints, and dependency chains
- reveal where risk is concentrated
- distinguish milestone progress from mere activity
- make a complex strategy visible enough to navigate

---

## Best Use Cases

- new market entry
- product launch planning
- business model transition
- multi-stage fundraising plans
- strategic repositioning
- cross-functional initiatives
- operator planning for ambiguous goals
- “how do I get from here to there?” problems

---

## What to Provide

Useful input includes:
- the goal
- current starting position
- constraints
- time horizon
- available resources
- major risks already known
- what success would look like
- what failure would look like
- whether the user wants a fast route, safe route, or leveraged route

If the user has not defined the starting point or desired destination clearly, this skill should identify that before pretending to map the route.

---

## Standard Output Format

MAP STRATEGIC ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━
Goal: [What destination is being pursued]
Starting Position: [Current reality]
Map Type: [Fast route / Safe route / Leveraged route / Mixed]

TERRAIN OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Core destination: [Where this is trying to go]
- Critical path: [Main route]
- Alternate path: [Fallback or secondary route]
- Major dependency: [What must happen first]

RESOURCE NODES
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [Capital node]
- [Talent node]
- [Distribution node]
- [Trust / relationship node]
- [Operational node]

RISK ZONES
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ [Where the route is fragile]
⚠️ [What could slow progress]
⚠️ [What could invalidate the plan]
⚠️ [What the user may be underestimating]

MILESTONE MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Milestone 1]
2. [Milestone 2]
3. [Milestone 3]
4. [Milestone 4]

BOTTLENECKS
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

ROUTE RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━
Best Route: [Chosen path]
Why: [Why this route is strongest under current constraints]

NEXT STEP
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [What should be clarified, acquired, tested, or started first]

---

## Cartography Principles

- strategy becomes usable only when the terrain is visible
- milestones matter more than motion
- not all routes are equal; some only look shorter
- a missing dependency can collapse the whole map
- bottlenecks are often more important than goals
- leverage points matter more than sheer activity
- clarity about sequence is often more valuable than more ideas

---

## Logic Map Lens

When analyzing a business goal, ask:

- Where are we starting, really?
- What must be true before movement is possible?
- Which resource nodes matter most?
- Which milestone actually changes the map?
- What bottleneck controls the pace of the whole route?
- What failure point would invalidate this plan fastest?
- Is this one route, or several competing maps pretending to be one?

---

## Execution Protocol (for AI agents)

When user asks for a strategic map, follow this sequence:

### Step 1: Parse the destination
Extract:
- desired goal
- time horizon
- scale of ambition
- what success means
- what failure means

### Step 2: Parse the starting terrain
Extract:
- current position
- available resources
- existing constraints
- team or operator capacity
- risk tolerance

### Step 3: Identify route logic
Map:
- critical path
- alternate paths
- dependencies
- bottlenecks
- leverage points
- likely dead ends

### Step 4: Build the milestone sequence
Return:
- milestone order
- what each milestone unlocks
- what must exist before the next stage
- where the user is most likely to get stuck

### Step 5: Surface terrain risks
Flag:
- fragile assumptions
- missing resources
- sequencing mistakes
- hidden dependencies
- unrealistic compression of time or effort

### Step 6: Recommend the route
Return:
- best route under current constraints
- fallback route
- first move
- what should be validated before committing deeper

### Step 7: Guardrails
If the goal, starting point, or constraints are too vague:
- say so clearly
- do not fake a detailed map
- ask for the missing terrain inputs

---

## Activation Rules (for AI agents)

### Use this skill when the user asks about:
- mapping a business goal
- planning a strategic route
- visualizing milestones and risks
- turning complexity into a clear plan
- identifying bottlenecks and dependencies
- figuring out the best path from current state to target state

### Do NOT use this skill when:
- the user needs pure task execution
- the user only wants brainstorming with no route logic
- there is no clear destination to map
- the task is simple enough that route mapping adds noise

### If context is ambiguous
Ask:
"Do you want a strategic map of the path, or just a list of ideas and next steps?"

---

## Boundaries

This skill supports strategic route-mapping and business terrain analysis.

It does not replace:
- legal review
- financial modeling
- domain-specific expert validation
- project execution tools
- operational sign-off
