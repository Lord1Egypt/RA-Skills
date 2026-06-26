status: closed

---
---

## Context
Merged branches are never cleaned up, leaving historical branches that guarantee naming collisions for future orchestrator runs.

## Requirements
1. **State 6 Teardown**: Modify `scripts/orchestrator.py` (or the relevant state 6 logic) so that after `merge_code.py` successfully executes and merges the branch, it executes `git branch -D <branch_name>` to physically delete the local temporary branch.
2. **Testing**: Update `tests/test_069_git_namespace_and_teardown.sh` to include the teardown assertions. After creating the branch, committing a dummy change, switching back to master, and merging, run the teardown logic and assert that `git branch --list <branch_name>` returns empty. Ensure the test passes 100%.
