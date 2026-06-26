# Multi-Agent Collaboration Claude Grade 2.0.0

## What changed

This upgrade keeps the original collaboration idea, but raises the package from a broad AI-collaboration toolkit to a more disciplined Claude-Code-style system.

## Major upgrades

1. Typed memory retrieval
- Added `ClaudeMemorySystem`
- Memory is now split into:
  - identity
  - correction
  - task
  - project
  - reference
- Added background extraction and Top-5 retrieval

2. Coordinator-led multi-agent workflow
- Added `ClaudeCoordinator`
- Fixed six-role operating model:
  - coordinator
  - explorer
  - planner
  - implementer
  - verifier
  - reviewer

3. Verification-first acceptance
- Added `VerificationAgent`
- Success now depends on evidence, not narrative confidence

4. Safety before execution
- Added `SafetyGatePipeline`
- Current implementation includes 14 pre-execution guards

5. Cost and cache observability
- Added `CostGovernor`
- Tracks 14 cache miss reason categories and invalid-call waste

## Why this is a big-version upgrade

The original package already had memory, routing, workflow, and goal systems.
This version adds the missing engineering controls that make a multi-agent system more trustworthy in real use:

- retrieval before reasoning
- role-bound coordination
- proof-based verification
- execution safety
- cost governance

## New files

- `dist/core/claude-memory.js`
- `dist/systems/claude-coordinator.js`
- `dist/systems/verification.js`
- `dist/systems/safety.js`
- `dist/systems/cost.js`
- `scripts/core/claude-memory.ts`
- `scripts/systems/claude-coordinator.ts`
- `scripts/systems/verification.ts`
- `scripts/systems/safety.ts`
- `scripts/systems/cost.ts`
- `claudegrade-demo.js`

## Validation

Validated by running:

```bash
node claudegrade-demo.js
```
