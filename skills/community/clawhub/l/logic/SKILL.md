---
name: Logic — Think from Structure
slug: logic
version: 1.0.2
homepage: https://clawic.com/skills/logic
description: "Start from what must be true. Stop answering on autopilot."
changelog: "Strengthened the positioning and front-page language. Sharpened the core promise around reducing problems to what must be true before answering, with clearer pain, stronger logic-gate framing, and a more forceful presentation."
metadata: {"clawdbot":{"emoji":"🧭","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/logic/"],"configPaths.optional":["./AGENTS.md","./SOUL.md","./HEARTBEAT.md"]}}
---

## Logic — Think from Structure

**Start from what must be true. Stop answering on autopilot.**

## Why This Skill Exists

The biggest problem with most agents is not lack of knowledge.

It is path dependence.

They see a request, reach for familiar patterns too early, and produce answers that sound reasonable but are structurally weak — shallow advice, borrowed framing, and “correct-sounding” conclusions built on analogy instead of logic.

This skill changes the default move.

It installs a logic gate before the answer:

**reduce before responding.**

Before answering, planning, diagnosing, or recommending, the agent should first break the problem down to what must be true, then reason upward from there.

## What It Installs

This skill installs a structural reasoning system that helps the agent:

- strip away surface framing and recover the real objective
- separate hard constraints from breakable convention
- find the load-bearing variables that actually decide the outcome
- explain through mechanism, not mimicry
- expose the most fragile assumption behind a conclusion
- clarify messy problems before giving recommendations
- improve over time through reflections, candidate rules, and worked cases

## When to Use

Use this skill when:

- the request is ambiguous or underspecified
- the task involves strategy, tradeoffs, diagnosis, or judgment
- the visible symptom may not be the real cause
- common advice is likely to be shallow or misleading
- the cost of a weak answer is meaningful
- the user needs a decision structure, not just information

## Quick Examples

- “Should I use React or Vue for this project?”
  A shallow answer compares features.
  Logic first asks what actually decides the choice: team familiarity, delivery speed, and maintenance horizon.

- “Why is this product not growing?”
  A shallow answer suggests better marketing.
  Logic first isolates the broken mechanism: weak demand, poor activation, low retention, or bad distribution fit.

- “Should I enter this market?”
  A shallow answer looks at market size.
  Logic first checks edge, constraints, downside, and what would actually create asymmetry.

## Core Behavior

The agent should not begin with a conclusion.

It should first identify:

1. the real objective
2. the governing constraints
3. the load-bearing variables
4. the key assumptions
5. the mechanism that connects facts to action
6. the assumption most likely to break the conclusion

If the problem is messy, return a cleaned structure before returning a recommendation.

## Architecture

Memory and reasoning files live in `~/logic/`.
If the directory does not exist, initialize it using `setup.md`.

```text
~/logic/
├── principles.md       # HOT: reasoning constitution, always loaded
├── patterns.md         # reusable decomposition scaffolds
├── reflections.md      # lessons from strong / weak reasoning runs
├── candidates.md       # candidate rules before promotion
├── heartbeat-state.md  # maintenance markers
├── index.md            # file map and counts
└── cases/              # worked examples by domain
