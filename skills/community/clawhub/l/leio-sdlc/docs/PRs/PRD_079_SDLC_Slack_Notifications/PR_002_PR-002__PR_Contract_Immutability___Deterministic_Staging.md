status: open

# PR-002: PR Contract Immutability & Deterministic Staging

## 1. Objective
Enforce the immutability of PR contract files by stopping the Orchestrator from appending context to them, and ensure generated PR contracts are deterministically staged in Git.

## 2. Scope & Implementation Details
- `scripts/orchestrator.py`:
  - Delete the `append_to_pr` function.
  - Modify `set_pr_status` to use `subprocess.run(["git", "add", pr_file])` instead of the dangerous catch-all `git add .`.
- `scripts/create_pr_contract.py`:
  - Import `subprocess` if not already imported.
  - Immediately after writing the PR file, execute `subprocess.run(["git", "add", file_path], check=True)` to deterministically stage the new contract.

## 3. TDD & Acceptance Criteria
- Ensure unit tests pass and cover:
  1. `append_to_pr` is no longer called in `orchestrator.py` during status updates.
  2. `set_pr_status` strictly stages only the modified PR file.
  3. `create_pr_contract.py` successfully calls `git add <file_path>` after writing the content.