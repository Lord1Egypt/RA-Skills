status: closed

# PR-002: Integrate Handoff Prompts into Orchestrator Exits

## 1. Objective
Integrate the `HandoffPrompter` utility into the Orchestrator's execution flow to ensure every exit path prints the required actionable next steps for the Manager Agent.

## 2. Scope (Functional & Implementation Freedom)
- Hook the `HandoffPrompter` into the Orchestrator's exit handlers (both successful completions and fatal errors).
- Ensure the 5 specific triggers (Queue Empty, Dirty Workspace, Planner Failure, Git Checkout Error, Dead End) correctly invoke the prompter and output to standard out.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. Write integration/behavioral tests that simulate the 5 exit conditions within the Orchestrator process.
2. Assert that the Orchestrator's standard output contains the exact `[ACTION REQUIRED FOR MANAGER]` strings for each respective trigger.
3. The Coder MUST ensure all tests run GREEN before submitting.