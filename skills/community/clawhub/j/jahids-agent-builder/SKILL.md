---
name: jahids-agent-builder
description: Specify bounded JAHIDS agents with clear responsibilities, tools, inputs, outputs, limits, and verification.
---

# JAHIDS Agent Builder

## Use when
Designing a new worker agent or revising an existing agent manifest.

## Procedure
1. Define one primary responsibility and explicit non-goals.
2. Specify typed inputs, outputs, and failure states.
3. List only the tools required for the responsibility.
4. Define read/write scope, data classification, tenant boundary, and allowed environments.
5. Set time, token, cost, concurrency, and retry budgets.
6. Define handoff, escalation, and human approval conditions.
7. Add tests for normal, malformed, unauthorized, and adversarial inputs.

## Output
An agent specification, tool allowlist, policy requirements, tests, and operational limits.

## Authority boundary
Agents are bounded workers. They do not change their own identity, permissions, or autonomy.
