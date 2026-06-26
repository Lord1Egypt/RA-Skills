# Product Requirements Document (PRD)

## 1. Meta Information
- **Document Title**: PRD_ISSUE-1067_Remove_Planner_Git_Tracking
- **Target Audience**: Leio-SDLC Coder Agent, Reviewer Agent
- **Version**: 1.0.1
- **Status**: Draft

## 2. Executive Summary
This PRD completes the "Ghost PR Loop" critical bug (ISSUE-1067) fix in the SDLC framework. The root cause (`git add -f` in Planner) has already been physically removed via an emergency bypass. However, the orchestrator still contains obsolete logic that attempts to auto-commit PR contracts when checking out branches. This logic is no longer necessary since PR contracts are purely untracked local storage, and its presence risks accidentally committing unrelated staged files.

## 3. Detailed Requirements

### 3.1. Remove Obsolete Auto-Commit Logic in Orchestrator
- In `scripts/orchestrator.py`, near the beginning of `State 2` (around the `Checking out branch` print statements), locate the `git diff --cached` check and its subsequent commit command:
  `drun(["git", "-c", "sdlc.runtime=1", "commit", "-m", "docs(planner): auto-generated PR contracts"], check=True)`
- Since PR contracts are no longer forcibly added to the index, this auto-commit logic is obsolete and must be completely **REMOVED**.
- This prevents accidental commits of other staged files that might be caught in the `diff --cached` net.

## 4. Acceptance Criteria
1. The Orchestrator successfully runs the State Machine without attempting to commit "auto-generated PR contracts" during State 2.
2. PR status updates (`status: closed`) persist on the filesystem even after the orchestrator performs a `git reset --hard HEAD`.
3. All existing tests pass (`GREEN`).

## 5. Framework Modifications
- `scripts/orchestrator.py`
