# Capability Model

## Core Philosophy of This Skill

- Compress requests into structured inputs before deciding whether to enter the implementation phase.
- Build a minimal working map before making the smallest coherent change, instead of traversing the entire repository blindly.
- Tool capabilities take precedence over verbal promises: scriptable steps should be scripted; checkable rules should be policy-driven.
- Validation is part of the main workflow, not an afterthought following implementation.
- Delivery outputs reusable capabilities, validation evidence, and closure results, rather than a snapshot of the host implementation.

## Layered Capabilities

### tool layer

- Use `tool/tool-config.json` to constrain tool groupings, capabilities required per phase, and the boundaries of a single skill vs. standard libraries.
- The tool layer only expresses "what capabilities are needed to get things done", without mixing in state progression or delivery constraints.

### state layer

- Use `state/state-policy.json` to describe input shaping, mapping, implementation, validation, and delivery state sequences, along with minimum inputs.
- The state layer is solely responsible for the pace of progression and identifying gaps; it does not replace tool configurations or constraint judgments.

### policy layer

- Use `policy/constraint-policy.json` to define delivery boundaries, which are uniformly evaluated by `scripts/run_constraints.py` and `scripts/run_workflow.py`.
- The constraint layer determines whether hard boundaries—such as single skill limitation, standard library implementation only, and prohibiting host text copying—are still met.

### Implementation Principles

- First find the entry points, dependencies, state flows, and validation points before deciding on the impact area.
- Maintain the smallest coherent change. Avoid introducing unrelated refactoring, naming drift, or secondary mechanisms simultaneously.

### Validation and Closure Layer

- Every implementation must be matched with a corresponding validation entry point, rather than changing code first and guessing how to prove the result later.
- Only append artifact auditing and export preparation when publishing is actually required.

## Runtime Priorities

1. Structured requests and phase planning
2. Code discovery and impact assessment
3. Smallest coherent implementation
4. Validation and rollback assessment
5. Artifact auditing and export preparation

## Usage Guidelines

- When the task is still vague, fill in the required inputs first.
- When the task is clear, generate a phase plan before entering implementation.
- When publishable artifacts are needed, enter the export and audit actions last.
