status: closed

# PR-002: Orchestrator Post-Merge Sync Integration

## 1. Objective
Integrate the `leio-github-sync` utility into the main SDLC orchestration loop to automatically push code to GitHub after a successful PR merge.

## 2. Scope & Implementation Details
- Modify `scripts/orchestrator.py` to trigger the sync process immediately following a successful code merge (State 4 success or State 5 Arbitration override) and branch deletion.
- Execute `python3 ~/.openclaw/skills/leio-github-sync/scripts/sync.py --project-dir [WORKDIR]`.
- Implement robust error handling so that if the sync script fails or times out, the error is logged and a failure notification is sent, but the orchestrator does NOT crash or hang (the SDLC completion is not blocked).
- Utilize the new pulse messages created in PR-001.

## 3. TDD & Acceptance Criteria
- Add unit tests for `orchestrator.py` mocking the subprocess call to `sync.py`.
- Test the "happy path" where the sync succeeds.
- Test the "failure path" where the sync process raises an exception or returns a non-zero exit code, ensuring the orchestrator catches it and proceeds normally to completion.
- The PR must be fully self-contained with passing CI tests.