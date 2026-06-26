# PRD: Enforce SDLC via Git Pre-Commit Hook (ISSUE-1012)

## Context
As learned from recent failure incidents, soft constraints (prompt-level rules) are insufficient to prevent the main OpenClaw Agent (Manager) from bypassing the SDLC process and directly committing code to the `master` branch. To enforce the "Lobster Architecture" and strictly decouple roles, a hard physical isolation mechanism must be introduced at the Git engine level.

## Requirements

1. **Scope Protection & Opt-in Guardrail**:
   - The protection must strictly apply ONLY to the main branch (`master` or `main`).
   - Feature branches (e.g., `PRD_XXX`) used by sub-agents (Coder/Reviewer) must remain unrestricted.
   - **Opt-in Logic**: The hook must first check if a `.sdlc_guardrail` file exists in the repository root. If not found, it must `exit 0` implicitly, allowing standard commits on generic projects.

2. **Hook Redirection (core.hooksPath)**:
   - Instead of hiding the hook in the opaque `.git/hooks/` directory, create a version-controlled directory named `.sdlc_hooks/`.
   - Implement the `pre-commit` script inside `.sdlc_hooks/pre-commit`.
   - Update the deployment/installation scripts (`deploy.sh`, `preflight.sh`) to automatically run `git config core.hooksPath .sdlc_hooks` upon repository initialization.

3. **Authentication via Native Git Configuration (`git -c`)**:
   - Avoid brittle environment variables or stale file locks (Session Tokens).
   - The `pre-commit` hook must read a temporary, per-command Git config value (e.g., `git config sdlc.runtime`).
   - If `sdlc.runtime` is not equal to `"1"`, the commit must be intercepted and rejected.

4. **"Glass-Break" Emergency Override & JIT Prompt Enforcement**:
   - If a human administrator or the Main Agent attempts a direct `git commit` on the protected branch, the hook must exit non-zero and print a highly visible, self-explanatory error message.
   - **Role Awakening**: The error message MUST remind the Agent of its role: "As a Manager, you should NEVER commit directly! Run orchestrator.py instead."
   - The error message MUST explicitly provide the exact command required to bypass the hook in emergencies:
     `git -c sdlc.override=true commit -m "..."`
   - The hook script must check for `sdlc.override` and grant immediate bypass if set to `"true"`.

## Framework Modifications
- `scripts/orchestrator.py`: 
  - Any subprocess call that executes a `git commit` or `git merge` on the `master` branch must be updated to include `-c sdlc.runtime=1` (e.g., `git -c sdlc.runtime=1 commit ...`).
  - **Crucial Update**: Remove the `[FATAL]` error when an untracked PRD is passed. Instead, the Orchestrator should automatically run `git add <prd-file>` and `git -c sdlc.runtime=1 commit -m "docs(prd): auto-commit PRD"` to ingest it legally, preventing the Main Agent from being forced to perform an unauthorized manual commit.
- `scripts/merge_code.py`: Update the final merge commit logic to pass the runtime authentication flag (`git -c sdlc.runtime=1 merge <branch>`).
- `deploy.sh` \& `preflight.sh`: Add the `git config core.hooksPath .sdlc_hooks` initialization step.

## Architecture
By migrating from implicit hooks to a version-controlled `.sdlc_hooks/` directory mapped via `core.hooksPath`, the SDLC engine establishes a transparent, self-documenting boundary. Coupling this with stateless, per-command Git config (`git -c`) guarantees that authentication cannot leak across sessions or fail due to lingering file locks, while ensuring a deterministic escape hatch for human operators.

## Acceptance Criteria
- [ ] A `.sdlc_hooks/pre-commit` file is committed to the repository.
- [ ] The hook correctly ignores commits made on non-master branches.
- [ ] A raw `git commit` on `master` is rejected with an actionable error message containing the bypass instructions.
- [ ] Running `git -c sdlc.override=true commit -m "..."` successfully bypasses the lock on `master`.
- [ ] Running `git -c sdlc.runtime=1 commit -m "..."` successfully commits on `master`.
- [ ] `orchestrator.py` and `merge_code.py` successfully perform their automated merges without being blocked.