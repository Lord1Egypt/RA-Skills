status: open

# PRD-1022: Refactor SDLC Orchestrator for Polyrepo Compatibility (v4)

## 1. Problem Statement
We are migrating to a "Hub & Spoke Polyrepo" architecture. The current `orchestrator.py` and its spawners assume execution within a single global repository. Previous iterations of this PRD identified critical flaws: concurrent checkout conflicts, dirty workspace loops, hardcoded template paths, and OS-level Argument list too long (`E2BIG`) errors. Audit v6 specifically highlighted vulnerabilities with `/tmp` file collisions, zombie files, and CWE-377 permissions risks. We need a secure, concurrency-safe, and OS-limit-safe refactoring before the physical directory split.

## 2. Solution & Scope
Refactor the SDLC orchestrator to be strictly bounded, "location-aware", concurrency-safe, and secure across independent sub-repos.

**Target Project Directory:** `/root/.openclaw/workspace/projects/leio-sdlc`

**Implementation Details:**
1. **Early Context Switching & Deferred Git Checks:** In `scripts/orchestrator.py`, `os.chdir(args.workdir)` MUST be executed immediately after `argparse` resolution. ALL git operations (`git branch`, `git status`) and file locks MUST happen *after* switching to the target `workdir`.
2. **Per-Repo Granular Locking:** Replace the hardcoded global `.sdlc_run.lock` with a strict per-repository lock file: `os.path.join(args.workdir, ".sdlc_repo.lock")`. This prevents multiple pipelines from corrupting the same Git working tree.
3. **Git Boundary Enforcement:** Add a validation check in `orchestrator.py`: if a `.git` directory does not exist inside the `workdir` (and `SDLC_BYPASS_BRANCH_CHECK` is not equal to `"1"`), it MUST `sys.exit` with a `[FATAL]` error.
4. **Secure Temporary Prompt Injection (Fix E2BIG & CWE-377):** The spawners (`spawn_coder.py`, `spawn_planner.py`, `spawn_reviewer.py`) MUST securely pass massive prompt strings (Playbooks + PRDs) to `openclaw agent -m` without overflowing `MAX_ARG_STRLEN` or leaving world-writable files.
   - **Generation:** MUST use Python's `tempfile.mkstemp(suffix=".txt", prefix="sdlc_prompt_", dir="/tmp", text=True)` to create an atomic, unpredictable file.
   - **Permissions:** The file descriptor MUST be explicitly constrained to `0o600` via `os.chmod` (readable/writable only by the owner).
   - **Cleanup:** The subprocess execution MUST be wrapped in a `try...finally` block. The `finally` block MUST call `os.remove()` on the temporary file to prevent zombie accumulation.
   - **Command:** The CLI `-m` argument will only contain: `"Read your complete task instructions from <temp_file_path>. Do not modify this file."`
5. **Global Directory Propagation:** `orchestrator.py` MUST resolve the global workspace directory (e.g., via `os.path.abspath`) and pass it down via a `--global-dir` argument to all spawner scripts. Spawners MUST use this absolute base path to securely locate `playbooks/` and `TEMPLATES/`, ignoring relative paths entirely.
6. **Main/Master Branch Compatibility:** Update the branch enforcement check in `orchestrator.py` to allow the orchestrator to start from either the `master` or `main` branch.

## 3. Autonomous Test Strategy
- **Testing Approach:** Shell script integration testing.
- **Unit Test 1 (`test_polyrepo_context.sh`):** Create a mock `workdir` with `git init`. Assert that `.sdlc_repo.lock` is created *inside* the mock workdir.
- **Unit Test 2 (`test_git_boundary.sh`):** Pass a `workdir` without a `.git` folder. Assert fatal exit.
- **Unit Test 3 (`test_secure_prompt.sh`):** Pass a mock PRD to the spawners. Assert they use a secure temporary file with `0o600` permissions and that the file is deleted immediately after the subprocess completes (no zombie files).

## 4. TDD Guardrail
The implementation and its failing tests MUST be delivered in the same PR contract. No modifications to `orchestrator.py` are permitted without the automated test scripts passing.