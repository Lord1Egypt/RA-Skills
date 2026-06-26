---
name: invariance-battery
description: Runtime assertion system that continuously verifies AI agent invariants — properties that must ALWAYS hold. Use when building reliable autonomous agents, auditing agent behavior for drift, enforcing safety constraints, or building self-certifying AI systems. Covers invariant definition, runtime checking, drift detection, and falsification reporting.
version: 1.0.0
author: "@EvezArt"
tags: [evez, invariance, verification, safety, agent, assertion, drift, falsification]
---

# EVEZ Invariance Battery

Runtime assertion system for AI agents. Properties that must ALWAYS hold.

## When to Use

- Building autonomous agents that must maintain safety guarantees
- Auditing agent behavior for gradual drift from design intent
- Enforcing hard constraints that override any optimization objective
- Building self-certifying AI systems that can prove their own compliance
- Falsification testing — prove the agent VIOLATED an invariant, not just that it passed tests

## Architecture

The Invariance Battery runs as a continuous verification layer:

```
Agent Action → Invariance Check → PASS (proceed) / FAIL (halt + report)
                     ↓
              Append-Only Spine (audit trail)
```

## Invariant Types

1. **State Invariants** — Properties of the agent's internal state that must always hold
2. **Action Invariants** — Constraints on what actions the agent can take
3. **Temporal Invariants** — Properties over time (no oscillation, monotonic improvement)
4. **Boundary Invariants** — Hard limits the agent can never cross

## Key Concepts

- **Battery = Collection**: Multiple invariants checked in parallel, like electrical cells in series
- **Falsification > Verification**: A single violation PROVES the agent failed. No number of passes proves it works.
- **Drift Detection**: Gradual degradation of invariant scores over time
- **Spine Integration**: Every check is written to the append-only spine

## The Falsifier Gate

From EVEZ-OS: before any agent action is committed, it must pass through the falsifier gate.

```python
@invariant("action_cost < budget_threshold")
def check_budget(action):
    return action.estimated_cost < BUDGET_LIMIT

# If ANY invariant fails, the action is BLOCKED
# and the failure is written to the spine forever
```

## References

- EVEZ-OS: falsifier gate enforcement
- MAES: VERIFIED/PENDING/INVESTIGATING status model
- poly_c formula: τ × ω × topo / 2√N
