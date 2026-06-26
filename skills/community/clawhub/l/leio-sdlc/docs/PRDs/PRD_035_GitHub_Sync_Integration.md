# PRD: GitHub Sync Integration for SDLC (PRD-035)

## Context
Now that we have a functional global `leio-github-sync` skill, we need to integrate it into the `leio-sdlc` orchestrator. This will ensure that every successful PR merge and deployment is automatically synchronized to the remote GitHub repository, achieving a seamless GitOps workflow.

## Requirements

### 1. Post-Merge Sync (orchestrator.py)
- After a successful merge to `master` (State 4 success or State 5 Arbitration override), the Orchestrator MUST invoke the `leio-github-sync` utility.
- **Execution Path**: Call `python3 ~/.openclaw/skills/leio-github-sync/scripts/sync.py --project-dir [WORKDIR]` where `[WORKDIR]` is the absolute path to the project being managed.
- **Error Handling**: Sync failures should be logged but should not block the overall SDLC completion (i.e., the PR is already merged and closed).

### 2. Integration Pulse
- Add a new intermediate pulse message via `notification_formatter.py` for sync events:
    - **Sync Started**: "Synchronizing code to GitHub..."
    - **Sync Result**: "GitHub sync complete."

### 3. Native release update
- Ensure `leio-sdlc`'s own `deploy.sh` (which we just bumped to v0.7.0) also includes a sync call at the very end of its build/deployment process to keep its own repo up to date.

## Architecture
- **Tool Mapping**: Add `leio-github-sync` to the orchestration loop in `scripts/orchestrator.py`.
- **Logic Insertion**: The sync call should occur immediately after `merge_code.py` returns success and the local branch is deleted.

## Acceptance Criteria
- [ ] Every time a PR is merged by the orchestrator, a `git push` to GitHub is automatically triggered.
- [ ] Slack notifications reflect the GitHub synchronization status.
- [ ] Sync failures do not cause the orchestrator to crash or hang.
