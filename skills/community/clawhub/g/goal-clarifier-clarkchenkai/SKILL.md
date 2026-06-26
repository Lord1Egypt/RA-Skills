---
name: goal-clarifier
description: |
  Goal Clarifier — A purpose-first skill for turning vague requests into
  executable briefs before design or execution begins. Inspired by Aristotle's
  idea of telos, it forces clarification of goal, constraints, and success
  criteria before discussing tools, APIs, dashboards, agents, or automation.
  Activates when users jump to solutions too early, ask for underspecified
  systems, mix multiple objectives together, or need a safer handoff brief for
  a downstream human or agent.
license: MIT
metadata:
  author: clarkchenkai
  version: "1.0.0"
  language: en
---

# Goal Clarifier — Define Telos Before Design

Use this skill when the user starts with a solution-shaped request, but the real objective is still ambiguous.

## Activation Triggers

Activate when the user says things like:

- "Help me build an agent"
- "Make a dashboard for this"
- "Automate this workflow"
- "Optimize this project"
- "Set up a hiring system"
- "We need a better process"

The common pattern is not lack of effort. It is lack of a stable goal definition.

## Core Protocol

Follow this four-step protocol in order. Do not skip to system design, tool choice, or implementation until the output contract is complete.

### Step 1: Translate Means into Ends

Detect where the user is naming a mechanism instead of a purpose.

- "Build a recruiting agent" may mean screening applicants faster, scheduling interviews, improving candidate quality, or raising offer acceptance.
- "Make a dashboard" may mean spotting risk earlier, aligning stakeholders, or replacing manual weekly reporting.

Ask one direct question:

> "If this works, what changes in the world that matters?"

Reference: `references/aristotle.md`

### Step 2: Force the Three Essentials

The brief is not valid until all three are explicit:

- **Goal**: the concrete outcome that should exist if the work succeeds
- **Constraints**: time, budget, policy, risk, data, people, tooling, and reversibility limits
- **Success Criteria**: observable evidence that the outcome was achieved

If any essential is missing, ask a short targeted follow-up instead of guessing.

Reference: `references/patterns.md`

### Step 3: Define Boundaries

Clarify what is out of scope.

- Which users, teams, or cases are excluded?
- Which nice-to-haves should not be included in v1?
- Which decisions must remain human-owned?

This prevents scope creep disguised as ambition.

### Step 4: Separate Blocking Ambiguities from Working Assumptions

List unresolved issues in two groups:

- **Blocking ambiguities**: must be answered before design or execution
- **Working assumptions**: can be temporarily assumed, but must be called out clearly

Do not let the conversation hide these in prose.

Reference: `references/high-risk.md`

## Output Contract

Always end with a six-part brief using these exact headings:

```markdown
## Goal
[What outcome matters]

## Constraints
[Time, risk, policy, resources, data, ownership]

## Success Criteria
[How success will be measured]

## Scope Boundary
[What is explicitly not included]

## Key Ambiguities
[Blocking questions and working assumptions]

## Recommended Next Step
[The smallest safe action from here]
```

## High-Risk Rules

When the request touches irreversible or high-stakes decisions, slow down.

Examples:

- hiring, firing, promotion, compensation, admissions
- medical, legal, tax, finance, compliance, security
- surveillance, fraud, moderation, eligibility, trust and safety
- automated action against real people with material consequences

In these cases:

1. Require explicit success criteria and human ownership.
2. Mark the decision boundary that must stay with a human.
3. Refuse to "just automate it" if the purpose is still unclear.
4. Do not output an execution plan disguised as a clarified brief.

## Question Strategy

- Prefer 1-3 sharp questions over a long questionnaire.
- Ask about outcomes before architecture.
- Ask about constraints before features.
- Ask about success criteria before milestones.
- Ask about exclusions before integrations.

If the user is impatient, compress harder, but do not skip the structure.

## Response Style

- Be direct, not bureaucratic.
- Replace fuzzy nouns with observable outcomes.
- Surface hidden tradeoffs plainly.
- Treat "faster" or "better" as incomplete until tied to a metric or decision.
- Preserve the user's domain language when it helps, but normalize the brief structure.

## Boundaries

This skill does **not**:

- design the whole system
- choose the full architecture
- produce a project plan
- justify unclear goals with confident assumptions

Its job is to make downstream design safer and sharper.
