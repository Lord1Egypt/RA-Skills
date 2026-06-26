Status: Closed

status: completed

# PRD-1019: Clean Workspace During State 5 Escalation

## Target Project Scope
`/root/.openclaw/workspace/projects/leio-sdlc`

## 1. Problem Statement
The `orchestrator.py` script currently crashes with a `GitCheckoutError` during the "Tier 1 (Reset): Deleting branch and retrying" phase of State 5 Escalation. This crash occurs because the script attempts to checkout the `master` branch while the workspace is left in a dirty state by the coder agent, preventing the checkout.

## 2. Solution & Scope
To resolve the `GitCheckoutError` during the Tier 1 reset block:
*   **Action:** Add `git reset --hard` and `git clean -fd` commands immediately prior to invoking `safe_git_checkout("master")`.
*   **Scope:** Modify the Tier 1 reset logic in `orchestrator.py` to ensure the workspace is strictly clean before the branch checkout.
*   **Verification:** Add a test script to simulate the dirty workspace scenario and prove the reset logic successfully cleans the workspace and checks out the master branch without crashing.

## 3. Autonomous Test Strategy
*   **Strategy:** Integration/Script Testing.
*   **Approach:** Create a test script that sets up a test git repository, creates a dirty workspace (e.g., modified tracked files and new untracked files), and then invokes the modified Tier 1 reset block to verify that no `GitCheckoutError` is thrown and that the final state is a clean `master` branch.

## 4. TDD Guardrail
**CRITICAL:** The implementation of the workspace cleanup logic and its corresponding test script MUST be delivered together in the same PR contract. The test must fail before the fix is applied and pass afterward.