---
name: jahids-mission-planner
description: Turn a user goal into a bounded, verifiable mission plan with tasks, dependencies, budgets, risks, and approval points.
---

# JAHIDS Mission Planner

## Use when
A request needs multiple coordinated steps, agents, tools, or verifiable deliverables.

## Inputs
- User goal and acceptance criteria
- Available tools and execution environment
- Constraints, deadlines, budget, and autonomy level

## Procedure
1. Restate the goal as measurable outcomes.
2. Identify missing information; ask only for blockers.
3. Split work into small tasks with dependencies and owners.
4. Mark external side effects, sensitive data, and irreversible actions.
5. Define budget, timeout, retry, and stop conditions.
6. Identify approval gates before consequential actions.
7. Define evidence and verification for every deliverable.

## Output
A mission plan with scope, task graph, risks, approvals, budget, stop conditions, and acceptance tests.

## Authority boundary
Planning does not authorize execution. The JAHIDS Governor decides permissions and approvals.
