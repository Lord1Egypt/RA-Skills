# PRD: Fix Planner PR Slicing Ordering (ISSUE-1029)

## Context
When a PR (e.g., PR_001) fails the SDLC pipeline, it is escalated (State 5) and sent to the Planner for re-slicing into smaller Micro-PRs. Currently, these new Micro-PRs are appended to the end of the job queue (e.g., PR_003, PR_004), causing them to execute AFTER PR_002, which breaks sequential dependencies. 

The fix is to ensure the Planner uses the `--insert-after` parameter when calling `create_pr_contract.py`, so the new PRs are named `PR_001_1_xxx`, `PR_001_2_xxx`, etc., ensuring they naturally execute before PR_002 using lexicographical sorting.

## Requirements
- The Planner script (`scripts/spawn_planner.py`) must extract the failed PR's index prefix (e.g., `001` from `PR_001_xxx.md` or `002_1` from `PR_002_1_xxx.md`) when `--slice-failed-pr` is provided.
- Use Python's `re` module with pattern `r"^PR_(\d+(?:_\d+)*)_"` to extract the index.
- Update the Planner's task instructions (`task_string`) to explicitly include `--insert-after {failed_pr_id}` in the `python3 create_pr_contract.py` command template.
- The prompt must state that `--insert-after {failed_pr_id}` is MANDATORY for sequential ordering.

## Framework Modifications
- `scripts/spawn_planner.py`

## Architecture
The update modifies the core `leio-sdlc` orchestrator logic in `scripts/spawn_planner.py` to correctly identify and pass parent PR context to the sub-agent for tool-call generation.

## Acceptance Criteria
- [ ] `scripts/spawn_planner.py` correctly extracts the parent PR ID.
- [ ] The `task_string` prompt sent to the Planner includes the correct `--insert-after` parameter.
- [ ] `test_planner_slice_failed_pr.sh` passes successfully.
- [ ] Generated Micro-PR files for a failed `PR_001` are named `PR_001_1_xxx.md`, `PR_001_2_xxx.md`, etc.
