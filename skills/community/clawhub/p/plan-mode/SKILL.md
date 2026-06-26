---
name: plan
description: "Think-first execution with approval gating. Use when work is complex, ambiguous, irreversible, multi-step, worth comparing before choosing, interrupted and needs recovery, or long-running enough to need a living plan. Supports clarify, compare, execute, recover, parallel, and living planning lenses. Not for simple edits or quick questions."
---

# Plan

Use this skill to stop execution-first behavior on meaningful work.

Default pattern: **clarify → plan → approve → execute → close**.

Treat `/plan` as a **read-only planning stance** until approval. Safe reads are allowed: reading files, listing files, searching, inspecting docs, checking status, and other non-destructive exploration. Do not edit files, delete data, push commits, deploy, or run destructive or irreversible commands until the user approves a plan or explicitly says to skip planning.

Prefer the **core lenses** first. Use `parallel` and `living` only when the work is clearly big enough to justify the extra structure.

## When to stay out of the way

Do not force planning for:
- trivial single-file edits
- simple factual questions
- obvious follow-up micro-actions
- work where the user explicitly says to skip planning

## Command model

Use `/plan` as an auto-router. Pick the lens that matches the real problem.

### Core lenses

| Command | Use for | Output |
|---|---|---|
| `/plan` | Auto-pick the right lens | Short diagnosis + recommended plan |
| `/plan clarify` | Vague or political requests | Scope, assumptions, open questions, success criteria |
| `/plan compare` | Choosing between options | Option matrix, tradeoffs, recommendation |
| `/plan execute` | Clear multi-step work | Ordered plan, risks, checkpoints, definition of done |
| `/plan recover` | Interrupted or messy work | Current state, what is done, what is blocked, safest next step |

### Advanced lenses

| Command | Use for | Output |
|---|---|---|
| `/plan parallel` | Work that should split across subagents or lanes | Solo lane, parallel lanes, merge points |
| `/plan living` | Multi-session or strategic work | Persistent plan with decisions, next actions, open loops |

### Auto-router heuristics

When the user just says `/plan`, pick the simplest fitting lens:
- unclear request, fuzzy scope, or political ambiguity → `clarify`
- explicit choice between 2+ viable paths → `compare`
- clear multi-step task with real execution work → `execute`
- interrupted, messy, or half-finished work → `recover`
- only escalate to `parallel` if there are clearly separable lanes with owners and a merge point
- only escalate to `living` if the work is likely to span multiple sessions, days, or major checkpoints

If two lenses could fit, prefer the simpler one.

### Depth modifiers

Use these as optional modifiers, not separate lenses:
- `light` — use for small work, usually <= 5 steps, no lasting state needed
- `standard` — default for normal complex work
- `deep` — use for risky, irreversible, multi-day, or file-backed work

### Format guidance

#### Light
Use for short tasks.
Keep output inline:
- Goal
- Approach
- 2-5 steps
- Main risk

#### Standard
Use for most work.
Include:
- Goal
- Recommended lens
- Approach
- Using
- Steps
- Risks
- Approval ask

Keep it short enough that the user can approve it quickly.

#### Deep
Use for large or risky work.
Include:
- Goal
- Context / current state
- Option or approach rationale
- Detailed steps
- Checkpoints
- Risks and reversibility
- Definition of done
- Optional persistent file only after explicit approval if the plan should survive compaction

Examples:
- `/plan compare`
- `/plan recover light`
- `/plan living deep`
- `/plan off`

Use `/plan off` to disable auto-activation for the current session.

## What to do in each lens

### Clarify

Use when the request is still fuzzy.

Do this:
- Define the actual problem
- Surface assumptions
- List open questions only if they materially affect the plan
- State success criteria and non-goals

Do not jump into solution design too early.

### Compare

Use when multiple routes are plausible.

Do this:
- Compare 2-4 realistic options
- Show tradeoffs: speed, risk, reversibility, cost, maintenance, politics
- Recommend one path and explain why

Prefer recommendation over fence-sitting.

### Execute

Use for normal complex work.

Do this:
- State goal and approach
- List concrete steps
- Flag irreversible or high-risk actions with `⚠️`
- State dependencies, checkpoints, and definition of done
- Ask for approval before acting

### Recover

Use when work already exists and the problem is continuity, not invention.

Do this:
- Summarize current state
- Distinguish completed / partial / blocked / unknown
- Give the safest next step
- Say what should be discarded, preserved, or verified

Prefer stabilization over cleverness.

### Parallel

Use only when splitting work clearly improves speed or clarity.

Do this:
- Separate solo work from delegable work
- Define lanes with owners
- Define merge points and shared assumptions
- Keep parallelism minimal and purposeful

Do not parallelize tiny tasks just because you can.

### Living

Use for long-running projects.

Do this:
- Before creating a new living plan, first check whether one already exists for the project
- Do not write or update a living-plan file until the user explicitly approves persistent storage
- Once approved, persist the plan to file when useful
- If the project has no existing convention, default to a simple plan file under `docs/plans/` or another clearly named project folder
- Keep these sections updated:
  - current focus
  - next actions
  - decisions
  - open loops
  - risks
- On session start, resume, or after compaction, reload the latest approved living plan before continuing
- If the living plan is stale enough to be doubtful, say so and refresh it before acting

Prefer living plans for strategy, negotiations, and multi-day builds.

## Approval contract

Until approval:
- Stay read-only
- Inspect files, docs, and current state
- Audit available tools and skills using local/project context first
- Do not create or update plan files
- Do not make external network lookups for toolbox audit unless the user explicitly approves that broader search
- Compare approaches
- Ask only the minimum blocking questions

After approval:
- Execute only the approved scope
- Respect partial approvals like “do 1-3, hold on 4”
- If reality changes materially, stop and re-plan

Recognize these approval patterns:
- `go`
- `do it`
- `do steps 1-3`
- `hold on 4`
- `skip plan`
- `cancel`
- similar clearly positive approval language such as "sounds good" or "yes, proceed"

Control semantics:
- `/plan off` = stop auto-activating this skill for the current session
- `cancel` before execution = abort the plan and do nothing
- `cancel` during partial execution = stop immediately, report what has already been done, and do not assume rollback unless explicitly asked

## Surprise policy

Pause and report when:
- a required tool, file, or dependency was missing from the plan
- risk becomes meaningfully higher than planned
- destructive action becomes necessary unexpectedly
- new information changes the recommendation

Do not silently widen scope.

## Toolbox audit

Before presenting an execute-oriented plan:
- Check relevant installed skills first
- Prefer local/project-available capabilities over reinvention
- Only check external registries such as ClawHub when it materially changes the recommendation and the user has approved that broader search
- Do not send plan contents, secrets, or private project details to external services during toolbox audit

Show this briefly in a `Using:` section when it materially changes the approach.

## Likely failure modes to avoid

- Using `parallel` for work that is still unclear
- Using `living` for tasks that are actually small and one-shot
- Presenting too many lenses at once instead of recommending one
- Turning `/plan` into ceremony on obvious work

## Example patterns

### Example: compare
User: “Should we launch in market A or market B first?”

Output:
- Option A: Market A first
- Option B: Market B first
- Tradeoffs
- Recommendation

### Example: execute
User: “Migrate auth from sessions to JWT.”

Output:
- Goal
- Approach
- Using
- Ordered steps
- `⚠️` irreversible cleanup step
- Approval ask

### Example: recover
User: “Everything is all over the place. Pick this back up.”

Output:
- Current state
- What is done
- What is blocked
- Safest next step

### Example: parallel
User: “Review the repo, draft migration steps, and prep the rollout note.”

Output:
- Solo lane
- Parallel lanes with owners
- Merge point
- Approval ask

### Example: living
User: “Track this negotiation through 14 April.”

Output:
- Current focus
- Next actions
- Decisions
- Open loops
- Resume instruction
