status: closed

# PR-002: Integrate Workspace Cleanup into State 5 Escalation

## 1. Objective
Integrate the Git cleanup utilities into the State 5 Escalation's Tier 1 reset logic to prevent `GitCheckoutError` when checking out the master branch.

## 2. Scope (Functional & Implementation Freedom)
- Locate the Tier 1 (Reset) logic within the orchestrator's state machine (specifically State 5 Escalation).
- Before the orchestrator attempts to check out the master branch during this reset phase, invoke the newly created Git hard reset and clean utilities.
- Ensure any errors during cleanup are caught and logged appropriately.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. Write or update an integration test that simulates a State 5 Escalation (Tier 1 reset) scenario.
2. In the test setup, purposely leave the workspace in a dirty state (modified and untracked files) to simulate a failed coder agent run.
3. Trigger the Tier 1 reset logic.
4. Assert that no `GitCheckoutError` is thrown and that the orchestrator successfully checks out the master branch.
5. The Coder MUST ensure all tests run GREEN before submitting.