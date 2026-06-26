# PLAN-NNN: <Title>

Status:   draft | approved | in-progress | complete | cancelled
Created:  YYYY-MM-DD
Author:   planner_agent
Research: docs/status/RESEARCH-NNN.md
Priority: <impact x severity x frequency score>

Human approval required before implementation begins.
Approval timestamp: <pending>

---

## Objective

One paragraph. What will be true when this plan is complete?
Stated in terms of observable behavior, not implementation steps.

---

## Work Units and Execution Order

### Batch 1 (parallel-safe)

WU-01: <PIECE-01 name>
  Parallel-safe: yes
  Dependencies:  none

WU-02: <PIECE-02 name>
  Parallel-safe: yes
  Dependencies:  none

### Batch 2 (serial -- depends on Batch 1)

WU-03: <PIECE-03 name>
  Parallel-safe: no
  Dependencies:  WU-01 (consumes updated interface from PIECE-01)

---

## Piece Contracts

### WU-01 Piece Contract

Piece:         <PIECE-01 name from RESEARCH-NNN.md>
File(s):       <exact file paths>
Change:        <what changes -- function signatures, line ranges>

Pre-state:
  <exact current behavior or interface -- confirmed by researcher>

Post-state:
  <exact required behavior or interface after change>

Tests required:
  Unit:
    - assert <specific behavior> when <specific input>
    - assert <edge case> returns <specific output>
  Integration:
    - <specific scenario exercising PIECE-01 contract with PIECE-02>
  Edge cases:
    - <explicit list>

Done criteria:
  - [ ] All unit tests pass
  - [ ] All integration tests for this piece pass
  - [ ] Coverage >= 90% on changed files
  - [ ] Lint and pre-commit hooks pass
  - [ ] Reviewer Layer 1 approved (plan alignment)
  - [ ] Reviewer Layer 2 approved (correctness + security)
  - [ ] Reviewer Layer 3 approved (architecture coherence)

Rollback:
  <how to revert this piece without breaking other pieces>

### WU-02 Piece Contract
...

### WU-03 Piece Contract
...

---

## Integration Verification Steps

### After Batch 1 completes

Integration contracts to verify:
  - PIECE-01 => PIECE-02: <what to assert at the boundary>
  - PIECE-01 => PIECE-03: <what to assert>

Test scenarios:
  - <specific integration scenario>

### After All Batches Complete

Full integration test suite (run_integration_tests + run_e2e_tests)
E2e scenarios covering the complete task flow:
  - <scenario 1>
  - <scenario 2>

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| | | | |

---

## Rollback Plan

If the full plan must be reverted after all WUs are complete:
<steps to restore pre-plan state>
