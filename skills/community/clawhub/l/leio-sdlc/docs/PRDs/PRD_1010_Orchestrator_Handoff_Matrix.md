# PRD 1010: Orchestrator Handoff Matrix (Tool-as-Prompt)

## 1. Problem Statement
Currently, `orchestrator.py` exits (both successful and fatal) do not provide the Manager (Main Agent) with actionable next steps. This leads to silent failures or incomplete post-flight operations (like closing issues or updating state). The goal is to make the Orchestrator completely self-explanatory and prompt-driven for the Manager Agent. Every exit path must print an explicit `[ACTION REQUIRED FOR MANAGER]` block.

## 2. Core Requirements: The 5 Exit Points (Handoff Matrix)
The Orchestrator must implement the following 5 core exit points, printing explicit instructions for the Manager Agent upon termination:

1. **Happy Path (Queue Empty)**
   - **Trigger**: All PRs completed successfully.
   - **Actionable Prompt for Manager**: "The pipeline has finished. You must now: 1. Close the PRD. 2. Close the Issue. 3. Update STATE.md."
2. **Dirty Workspace**
   - **Trigger**: Uncommitted changes detected before a git operation.
   - **Actionable Prompt for Manager**: "Workspace is dirty. You must run `git add/commit` or `git stash` to clean the workspace before proceeding."
3. **Planner Failure**
   - **Trigger**: The planning phase fails to generate a valid plan.
   - **Actionable Prompt for Manager**: "Planner failed. You must review and fix the PRD."
4. **Git Checkout Error**
   - **Trigger**: Conflicts or errors when checking out a branch.
   - **Actionable Prompt for Manager**: "Git checkout failed. You must run `git clean`, `git reset`, or `git branch -D` to resolve the state."
5. **Dead End (Tier 3)**
   - **Trigger**: Unrecoverable system or environment error.
   - **Actionable Prompt for Manager**: "Dead End reached. STOP and notify Boss immediately."

## 3. Autonomous Test Strategy
- Unit tests must mock the 5 exit conditions in `orchestrator.py` and assert that the standard output contains the exact `[ACTION REQUIRED FOR MANAGER]` strings.
- Integration tests should run a dummy orchestrator process that triggers each exit and verify the output is parsable by the Manager Agent prompt constraints.

## 4. TDD Guardrails
- **Red**: Write a test for an orchestrator exit condition that expects the specific handoff prompt block.
- **Green**: Implement the `print()` or logging statement in the specific exit handler.
- **Refactor**: Centralize the exit prompt generation into a reusable `HandoffPrompter` utility class to ensure consistent formatting across all exits. No logic should proceed without these tests passing first.
