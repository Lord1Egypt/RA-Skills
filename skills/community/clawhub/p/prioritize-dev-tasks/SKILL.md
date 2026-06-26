---
name: prioritize-dev-tasks
description: Prioritize software project backlogs, bugs, technical debt, sprint tasks, release checks, and requirement pools using business impact, dependency blocking, delivery risk, security and data risk, and implementation cost. Use when a user asks to classify unfinished development work, determine execution order, identify release blockers, schedule deferred work, or remove low-value tasks.
---

# Prioritize Development Tasks

## Goal

Help the user decide which unfinished software project items to address
immediately, schedule deliberately, handle quickly, defer, merge, or remove.

Use an Eisenhower-style four-quadrant view to present classification. Determine
the actual execution order primarily by:

1. Security and data risk
2. Production incidents or core-flow availability
3. Release, acceptance, and multi-person dependency blockers
4. The current version goal
5. Cost-to-value ratio
6. General user-experience polish and long-term improvement

Answer in the language used by the user. Keep project terminology, task names,
and code identifiers as provided unless translating them is necessary for
clarity.

## Input Handling

Accept any of the following:

- A development to-do list or short task list
- A bug list
- Release-readiness checks
- Technical debt
- A sprint backlog
- A requirement pool or scheduling problem

When the user provides incomplete information:

- Give a preliminary judgment using the available evidence instead of requiring
  every field first.
- Explicitly mark conclusions that are based on incomplete information.
- Do not invent deadlines, user impact, cost, or dependency relationships.
- For potential security, data, production, or release-blocking concerns, rank
  conservatively higher and identify only the missing facts that could change
  the decision.

## Mandatory Escalation Rules

Treat the following as highest-priority candidates unless the user clearly
states that the risk is isolated, effectively mitigated, or outside the
current version scope:

- Data loss, data corruption, money errors, or incorrect critical business data
- Authorization bypass, privilege escalation, sensitive-data exposure, or a
  known security vulnerability
- Production crashes, unavailable core flows, or persistently failing critical
  APIs
- A completely blocked build, deployment, release, or acceptance process
- Work blocking multiple developers, integration, or critical testing
- Changes or failures that cannot be rolled back, or are costly to roll back

Do not lower the priority of these items merely because they take longer to
resolve.

## Assessment Dimensions

Assess each task against these dimensions:

| Dimension | Question to answer |
|---|---|
| Business impact | Does it affect a core flow, core users, delivery goals, or a primary revenue path? |
| Urgency | Is there a concrete deadline, current development/testing impact, an imminent release, or an expanding problem? |
| Blocking | Does it block integration, testing, acceptance, deployment, release, or another contributor? |
| Risk | Does it involve security, data, production stability, severe performance, or a difficult rollback? |
| Cost and value | Can a small effort remove major blockage, or is this high effort with limited present benefit? |
| Dependency order | Must it be completed before another task can proceed? |

## Quadrant Classification

| Quadrant | Meaning | Typical action |
|---|---|---|
| Important and urgent | Affects a core goal and needs prompt action | Handle immediately; reduce to a minimum deliverable fix if needed |
| Important but not urgent | Affects stability or long-term efficiency without blocking the current objective | Schedule in the current week or next sprint |
| Urgent but not important | Has time pressure but limited impact or a workable alternative | Time-box, delegate, or simplify |
| Neither important nor urgent | Has weak connection to the current objective or limited benefit | Defer, merge, return to the pool, or remove |

Use quadrants for communication, not as the sole ranking algorithm. Risk,
blocking relationships, and dependency order determine the execution order.

## Analysis Process

1. Identify the project phase: early development, integration, testing,
   pre-release, production maintenance, or refactoring.
2. Extract the current version objective, such as MVP delivery, a demo,
   scheduled release, or production recovery.
3. Check for mandatory escalation items.
4. Assess each task by impact, urgency, blocking, risk, cost-to-value ratio,
   and dependencies.
5. Classify tasks into quadrants and state the key evidence.
6. Recommend execution order: first address severe risk and blockers, then
   secure core flows, schedule important planned work, and handle low-value
   items last.
7. Explicitly identify tasks to defer, merge, or remove.
8. Ask only for missing information that could materially change the ranking.

## Output Rules

- Do not sort only by deadline.
- Do not label every task as high priority.
- List no more than three top-priority items; do not fill the list artificially.
- Always identify blockers. If none are evident, state that no clear blocker
  is identifiable from the current information.
- Always identify defer, merge, or remove candidates; if evidence is
  insufficient, state why.
- Do not rank cosmetic UI polish, speculative enhancements, or work without a
  clear requirement source as top priority unless delivery depends on it.
- When dependencies are clear, place execution order ahead of quadrant labels.

## Output Formats

### Compact Output

Use this format when there are fewer than five tasks and there is no apparent
security, data, production-incident, or release-blocking risk:

```markdown
# Development Task Priority Analysis

## Overall Judgment
- Current phase:
- Current objective:
- Basis: Preliminary judgment based on available information / sufficiently detailed information

## Ranked Tasks

| Order | Task | Quadrant | Key Reason | Recommended Action |
|---|---|---|---|---|

## Blockers And Deferrals
- Blockers:
- Defer / merge / remove candidates:

## Information To Confirm
- List only questions that could change the ranking.
```

### Full Output

Use this format when there are at least five tasks, or any security, data,
production, release, acceptance, or multi-person blocking concern is present:

```markdown
# Development Task Priority Analysis

## 1. Overall Judgment
- Current project phase:
- Current version objective:
- High-risk note:

## 2. Four-Quadrant Classification

| Quadrant | Task | Reasoning | Recommended Action |
|---|---|---|---|

## 3. Highest-Priority Items

List no more than three items. For each item state:
- Why it is prioritized
- Recommended treatment
- The risk or blockage removed when completed

## 4. Blocking Relationships

| Blocking Task | Blocked Work | Resolution Approach |
|---|---|---|

## 5. Defer, Merge, Or Remove Candidates

| Task | Recommendation | Reason |
|---|---|---|

## 6. Recommended Execution Order

1. ...
2. ...
3. ...

## 7. Information To Confirm

Ask only questions that could materially change the priority ranking.
```
