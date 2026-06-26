status: open

# PR-003: Semantic Git Status Enforcement & Rogue Prompt Cleanup

## 1. Objective
Ensure semantic commits by cleaning up untracked artifacts and updating LLM playbooks to stop blindly calling `git add .`. Implement final Git hygiene practices.

## 2. Scope & Implementation Details
- `scripts/orchestrator.py`:
  - Delete `force_commit_untracked_changes`.
  - In State 3 (Post-Coder check), run `git status --porcelain`. If dirty:
    - Check for `.coder_state.json` with `{"dirty_acknowledged": true}`. If missing, spawn Coder with `--system-alert "<git status output>"`.
  - In State 4, pass the Review Report to `spawn_coder.py` with `--feedback-file`.
  - In State 6 (Merge code) BEFORE `git checkout master`, run `subprocess.run(["git", "reset", "--hard", "HEAD"])` and `subprocess.run(["git", "clean", "-fd"])`.
- `scripts/spawn_coder.py`:
  - Update to inject prompts directly into the existing Coder session when receiving `--system-alert` or `--feedback-file`.
- `playbooks/coder_playbook.md` & `scripts/spawn_*.py`:
  - Remove all instructions referencing `git add .`.
  - Update `coder_playbook.md` to require explicit `git add <file>` and managing untracked files with `.coder_state.json` or `.gitignore`.

## 3. TDD & Acceptance Criteria
- Validate `test_orchestrator.py` correctly asserts the orchestrator rejects a dirty git tree post-coder without a valid `.coder_state.json`.
- Ensure final cleanup logic cleanly resets the branch to HEAD and cleans untracked files before checking out master.