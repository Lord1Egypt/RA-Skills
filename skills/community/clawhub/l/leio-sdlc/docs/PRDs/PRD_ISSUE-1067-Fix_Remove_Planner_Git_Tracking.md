---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1067-Fix - Remove Planner Git Tracking

## 1. Context & Problem Definition (核心问题与前因后果)
In previous versions (ISSUE-1067), we attempted to remove the explicit `git add -f` tracking of generated PR contracts to prevent a fatal "Ghost PR Loop". However, the execution was incomplete: the Coder successfully removed the `git commit` logic from the Orchestrator but FAILED to remove the `subprocess.run(["git", "add", "-f", file_path], check=True)` command from `scripts/create_pr_contract.py`.

Because of this incomplete fix, newly generated PR contracts are placed in a "staged but uncommitted" ghost state. If the Orchestrator encounters a Coder failure and executes `git reset --hard` and `git clean -fd` in State 5, these staged-but-uncommitted files are completely physically wiped from the disk. This causes the immediate crash of the subsequent Coder retry (`[Pre-flight Failed] PR Contract not found`), resulting in a pipeline deadlock.

## 2. Requirements (需求说明)
1. **Remove Force Git Tracking**: Locate and completely remove the line `subprocess.run(["git", "add", "-f", file_path], check=True)` from `scripts/create_pr_contract.py`. The script must simply write the Markdown file and exit without interacting with Git.
2. **Add Strict Verification Test**: We MUST add a test (e.g., in `tests/test_create_pr_contract.sh` or a Python test) to strictly verify that `create_pr_contract.py` NO LONGER invokes any `git add` commands, and that generated files remain completely untracked by Git in the working directory.

## 3. Architecture (架构设计)
- **Stateless Artifact Generation:** The PR contract generator (`create_pr_contract.py`) acts purely as a stateless file writer. It is explicitly forbidden from interacting with the Git index.
- **Git Isolation:** The `.sdlc_runs/` directory remains untracked. Any state resets (`git reset --hard`) will strictly affect tracked codebase files and leave the PR lifecycle artifacts untouched.

## 4. Acceptance Criteria (验收标准)
- [ ] `scripts/create_pr_contract.py` does not contain any `git add` or `subprocess.run` calls related to Git.
- [ ] A dedicated test is created or updated to verify that executing `create_pr_contract.py` does not stage files in Git.
- [ ] The full test suite passes (GREEN).

## 5. Framework Modifications (框架修改声明)
- `scripts/create_pr_contract.py` (modified)
- `tests/test_create_pr_contract.sh` (modified)
