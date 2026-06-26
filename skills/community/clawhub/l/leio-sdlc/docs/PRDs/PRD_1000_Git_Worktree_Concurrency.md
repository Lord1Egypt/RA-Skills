status: obsolete (Superseded by Polyrepo Migration - ISSUE-1020)

# PRD-1000: Implement Git Worktree for Concurrent Monorepo Development

## 1. Problem Statement
The current `leio-sdlc` orchestrator relies on a global lock (`.sdlc_run.lock`) and performs Git checkouts directly in the main workspace (`/root/.openclaw/workspace`). This turns the pipeline into a single-lane bridge, preventing concurrent execution of independent PRDs (e.g., AMS and ClawOS cannot be developed simultaneously). Simply removing the lock causes severe HEAD collisions, file overwrites, and state corruption. 

## 2. Solution & Scope
To achieve robust concurrency, we will migrate the Orchestrator to a `git worktree`-based architecture with strict environment and memory isolation.

**Target Project Directory:** `/root/.openclaw/workspace/projects/leio-sdlc`

**Architectural Requirements (The 9 Guardrails):**
1. **Granular Locking:** Replace the global `.sdlc_run.lock` with PRD-level locks (e.g., `.sdlc_run_<PRD_NAME>.lock`).
2. **Safe Workspace Location:** Worktrees MUST be created inside the main workspace to comply with OpenClaw sandbox boundaries (e.g., `/root/.openclaw/workspace/.worktrees/<PRD_NAME>/<PR_ID>`). Update `.gitignore` in the main repo to ignore `.worktrees/`.
3. **Environment Hydration:** Before yielding to the Coder, the Orchestrator MUST perform environment hydration by using hardlinks (`cp -al`) to copy heavy dependency folders (e.g., `node_modules`, `venv`, `__pycache__`) from the main repo to the new worktree. This prevents `preflight.sh` from re-downloading dependencies.
4. **Main Repo Merge Routing:** State 6 (Merge) MUST execute `git merge` in the *main repository*, not inside the worktree (to avoid `fatal: master is already checked out` errors).
5. **Robust Teardown & Zombie Prevention:** Wrap the Orchestrator's lifecycle in a robust `try...finally` block. Upon exit (success or fatal), it MUST execute `git worktree remove --force <path>` and `git worktree prune`.
6. **State 0 (Planner) Persistence:** The Planner MUST continue to execute in the *main repository* so that generated PR contracts (`docs/PRs/`) are durable and survive worktree destruction.
7. **Artifact Centralization:** Ephemeral artifacts (e.g., `Review_Report.md`, `.coder_state.json`) MUST be written to the main repository's PR directory (`docs/PRs/<PRD_NAME>/`), never inside the ephemeral worktree. This prevents "Feedback Amnesia" during Tier 1 resets.
8. **Session Memory Kill on Reset:** During State 5 Tier 1 Reset (Worktree destruction), the Orchestrator MUST forcibly kill the associated Gemini CLI Coder session to prevent the model from hallucinating that its reverted code still exists.
9. **Moving Master Sync:** Before State 4 (Review) or State 6 (Merge), the Orchestrator MUST execute `git rebase master` (or `git pull --rebase origin master`) inside the worktree to ensure the PR is reviewed and merged against the absolute latest trunk, preventing silent merge conflicts.

## 3. Autonomous Test Strategy
- **Testing Approach:** Shell script unit & integration testing.
- **Validation Script 1 (`scripts/test_worktree_lifecycle.sh`):** Verify that a worktree is created in `.worktrees/`, environment hydration (`cp -al`) works, artifacts are written to the main repo, and the worktree is cleanly pruned upon exit.
- **Validation Script 2 (`scripts/test_worktree_concurrency.sh`):** Launch two background instances of `orchestrator.py` with two different dummy PRDs. Assert that they both acquire their respective locks, operate in separate `.worktrees/` subdirectories, and successfully merge without HEAD collisions.

## 4. TDD Guardrail
The implementation and its corresponding failing tests MUST be delivered in the exact same PR contract. No code changes to `orchestrator.py` are permitted without the automated test scripts proving the Worktree isolation mechanisms first.
## 5. Auditor Security Patches (Added post-review)
To prevent critical failures identified during the architecture audit, the following must be implemented:
1. **Session ID Rotation:** Coder sessions must dynamically rotate IDs (e.g., append `_retry_X`) upon Tier 1 resets.
2. **Hydration Whitelist:** Environment hydration must strictly whitelist static dependencies (`node_modules`) and execute a recursive deletion of dynamic caches (`__pycache__`) post-hydration.
3. **Anti-Hang Rebase:** The pre-merge `git rebase master` must be non-interactive and immediately abort/throw `[FATAL_GIT]` upon detecting any conflict, preventing Orchestrator deadlocks.
