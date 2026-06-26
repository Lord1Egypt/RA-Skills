status: closed

# PR-002: Update Planner Task Prompt

## 1. Objective
Update the Planner's task instructions to use the extracted failed PR ID for sequential ordering of new Micro-PRs.

## 2. Scope (Functional & Implementation Freedom)
- Modify the prompt/task instructions sent to the Planner to explicitly include the `--insert-after {failed_pr_id}` parameter in the `create_pr_contract.py` command template.
- State clearly in the instructions that `--insert-after` is MANDATORY for sequential ordering.
- *The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- The task instructions generated for the Planner include the correct `--insert-after {failed_pr_id}` argument when slicing a failed PR.
- Integration tests or relevant test cases (`test_planner_slice_failed_pr.sh` if applicable) pass successfully.
- The Coder MUST ensure all tests run GREEN before submitting.