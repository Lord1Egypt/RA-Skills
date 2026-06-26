# PRD-069: Git Namespace Refactoring & State Solidification

## 1. Problem Statement
The Orchestrator pipeline frequently crashes between Planner completion (State 0) and Coder initialization (State 1) due to Git state collisions. 
The crashes are caused by three interlinked flaws in `scripts/orchestrator.py`:
1. **Colliding Branch Names**: A crude regex (`r'(PR_\d+)'`) truncates rich PR filenames, forcing all branches to be named `feature/PR_001` regardless of the PRD context.
2. **Dirty Checkout**: Planner artifacts (PR contracts) are staged (`git add .`) but never committed. Orchestrator attempts `git checkout` with a dirty working tree, which Git aborts to prevent overwriting uncommitted files when a target branch already exists.
3. **Branch Leaks**: Merged branches are never cleaned up, leaving historical branches that guarantee naming collisions for future runs.

## 2. Solution
We must implement a strict Git State Machine within `orchestrator.py` to ensure robust isolation and cleanup.

### 2.1. Dynamic Git Namespace (Drop `feature/`)
- Remove the regex truncation in `orchestrator.py` that forces the `feature/` prefix.
- **New Branch Naming Rule**: `branch_name = f"{parent_dir_name}/{base_filename}"`.
- Example: If the PR file is `docs/PRs/PRD_069/PR_001_Git_Fix.md`, the branch name MUST be exactly `PRD_069/PR_001_Git_Fix`. Git will naturally treat `PRD_069` as a folder.

### 2.2. State 0 Solidification (Pre-Checkout Commit)
- Before the Orchestrator checks out a branch (transitioning from Planner to Coder), it must verify if there are uncommitted staged changes.
- If changes exist, execute: `git commit -m "docs(planner): auto-generated PR contracts"`. This ensures the working tree is completely clean before branching.

### 2.3. State 6 Teardown (Post-Merge Cleanup)
- In State 6 (Green Path), after `merge_code.py` successfully executes and merges the branch into `master`, the Orchestrator MUST execute `git branch -D <branch_name>` to physically delete the local temporary branch.

## 3. Testing Strategy (TDD)
A new integration test (`tests/test_069_git_namespace_and_teardown.sh`) MUST be created.

### 3.1. Test Setup
1. Initialize an isolated dummy Git workspace (`/tmp/test_069_workspace_$$`).
2. Simulate a Planner output by creating: `docs/PRs/PRD_069_Test/PR_001_Namespace_Fix.md` and running `git add .`.

### 3.2. Execution & Assertions
1. Run the modified branch extraction logic to assert the parsed branch name is exactly `PRD_069_Test/PR_001_Namespace_Fix`.
2. Run the State 0 Solidification logic and assert that `git status` is clean before proceeding.
3. Create the branch, switch to it, commit a dummy change, switch back to master, and merge it.
4. Run the State 6 Teardown logic and assert that `git branch --list PRD_069_Test/PR_001_Namespace_Fix` returns empty (branch is deleted).