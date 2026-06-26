status: closed

---
---

## Context
The orchestrator currently crashes due to colliding branch names and dirty checkouts when transitioning from Planner to Coder.

## Requirements
1. **Dynamic Git Namespace**: Modify `scripts/orchestrator.py` to drop the regex `feature/PR_001` truncation. The new branch name must be parsed as `branch_name = f"{parent_dir_name}/{base_filename}"` (e.g. `PRD_069/PR_001_Namespace_Fix`).
2. **State 0 Solidification**: In `scripts/orchestrator.py`, before checking out a branch, check for uncommitted staged changes. If they exist, execute `git commit -m "docs(planner): auto-generated PR contracts"`.
3. **Testing**: Create `tests/test_069_git_namespace_and_teardown.sh`. Initialize a dummy git workspace (`/tmp/test_069_workspace_$$`), create a dummy PR file, and run the extraction and solidification logic. Assert that the branch name is correct and `git status` is clean before proceeding. Ensure the test passes 100%.
