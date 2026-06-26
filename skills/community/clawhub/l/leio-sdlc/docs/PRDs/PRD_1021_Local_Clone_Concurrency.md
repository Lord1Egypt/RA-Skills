status: open

# PRD-1021: Implement Local Clone Sandbox Architecture for SDLC Concurrency (v3)

## 1. Problem Statement
The `leio-sdlc` orchestrator currently executes directly inside the monolithic global workspace (`/root/.openclaw/workspace`). This single-lane architecture relies on a global lock (`.sdlc_run.lock`) and strict dirty-workspace checks, preventing concurrent execution of multiple PRDs. Previous proposals (Git Worktree, Polyrepo) were rejected due to severe Git lock deadlocks and repository explosion risks. The Local Clone proposal (v1 & v2) iteratively solved pathing and push restrictions, but still suffered from hardcoded global locks and overzealous workspace purity checks. We need a robust, lock-free concurrency model that physically isolates executions without leaving the Monorepo.

## 2. Solution & Scope
Implement a "Local Clone Sandbox" architecture.
**Target Project Directory:** `/root/.openclaw/workspace/projects/leio-sdlc`

**Architectural Requirements (Guardrails):**
1. **Instant Sandbox Cloning:** Replace in-place branch checkouts with `git clone --local /root/.openclaw/workspace /root/.openclaw/workspace/.sandboxes/<PRD_NAME>`. The Orchestrator MUST execute all subsequent sub-agents inside this sandbox. Add `.sandboxes/` to the global `.gitignore`.
2. **Environment Hydration:** To prevent `preflight.sh` dependency vacuum, the Orchestrator MUST use `cp -al` to hardlink static dependency directories (e.g., `node_modules`, `venv`) from the main repo to the sandbox. It MUST strictly exclude or recursively delete dynamic caches (e.g., `__pycache__`) in the sandbox post-hydration.
3. **Absolute Path Enforcement:** The Orchestrator MUST pass absolute paths for all PR contracts (`--pr-file`) to the sub-agents. The `Review_Report.md` and `.coder_state.json` MUST be written directly to these absolute paths in the main repository.
4. **Non-Bare Repo Push & Merge Routing:** The sandbox MUST NOT push to the `master` branch of the origin. In State 6 (Merge):
    - The sandbox executes `git push origin <feature_branch>`.
    - The Orchestrator changes its working directory back to the main repository.
    - The Orchestrator executes `git merge <feature_branch>` in the main repository.
5. **Non-Interactive Rebase Sync:** Before pushing the feature branch, the Orchestrator MUST execute `git fetch origin && git rebase origin/master` in the sandbox. This MUST be non-interactive; if a conflict occurs, it MUST immediately `git rebase --abort` and trigger a `[FATAL_GIT]`.
6. **Session ID Rotation:** Upon a State 5 Tier 1 Reset (sandbox destruction), the Orchestrator MUST rotate the Coder's Session ID (e.g., appending `_retry_1`) to prevent LLM hallucinations.
7. **Delayed Granular Locking:** Remove the hardcoded `.sdlc_run.lock` at the start of `orchestrator.py`. The `fcntl` lock MUST be acquired *after* `argparse` parses the inputs, and the lock name MUST be dynamically bound to the PRD (e.g., `.sdlc_run_<PRD_FILENAME>.lock`).
8. **Remove Main Workspace Dirty Check:** Delete the early `git status --porcelain` check that aborts the Orchestrator if the global workspace is dirty. The main workspace acts as the host and may have uncommitted files; only the local clone sandbox needs to be clean.

## 3. Autonomous Test Strategy
- **Validation Script 1 (`scripts/test_local_clone_lifecycle.sh`):** Verify sandbox creation in `.sandboxes/`, hydration success, artifact writes to absolute paths, non-bare pushes, and secure deletion.
- **Validation Script 2 (`scripts/test_local_clone_concurrency.sh`):** Launch two background instances of `orchestrator.py` with different PRDs. Assert both bypass the dirty check, acquire independent PRD locks, operate in isolated clones, and merge back to the origin without global HEAD collisions.

## 4. TDD Guardrail
The implementation and its corresponding failing tests MUST be delivered in the same PR contract. No modifications to `orchestrator.py` are permitted without the automated test scripts passing.