status: closed

# PR-002: Orchestrator Handoff Matrix & Exit Conditions

## 1. Objective
Implement the "Tool-as-Prompt" pattern by intercepting all major exit conditions and emitting standardized handoff instructions for the Manager Agent.

## 2. Scope (Functional & Implementation Freedom)
- Implement exit handlers for the 5 major conditions: Happy Path (Success), Dirty Workspace (Startup Fatal), Planner Failure (Startup Fatal), Git Checkout Error (Runtime Fatal), and Dead End/Escalation (Runtime Fatal).
- Ensure each condition prints the specific standardized action block (e.g., `[SUCCESS_HANDOFF]`, `[FATAL_STARTUP]`, `[FATAL_PLANNER]`, `[FATAL_GIT]`, `[FATAL_ESCALATION]`) to stdout before safely exiting.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. A test must validate that a clean exit (empty queue) outputs the exact `[SUCCESS_HANDOFF]` block.
2. A test simulating a dirty workspace at startup must output the exact `[FATAL_STARTUP]` block.
3. Tests for planner failure, git failure, and dead-end escalation must output their respective `[FATAL_*]` blocks.
4. All tests MUST run GREEN before submitting.