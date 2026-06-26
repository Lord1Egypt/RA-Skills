---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1051 Git Clean Artifact Destruction

## 1. Context & Problem Definition
In barebones user projects (like `target-demo`) that lack comprehensive `.gitignore` files, the Orchestrator's pre-merge cleanup step (`git clean -fd`) aggressively deletes dynamic runtime artifacts (such as `Review_Report.md`). This causes `merge_code.py` to fail its "Artifact-Driven Evidence Chain" physical file check, triggering a State 5 Escalation death-loop. 
The Orchestrator must dynamically append critical runtime artifacts to the target repository's `.git/info/exclude` during initialization to guarantee their survival across harsh workspace sanitation commands.

## 2. Requirements
1. Modify `scripts/orchestrator.py`.
2. In the sandbox initialization phase where `.sdlc_runs/` is currently added to `.git/info/exclude`, expand the logic to also append a list of critical SDLC runtime artifacts:
   - `Review_Report.md`
   - `current_review.diff`
   - `recent_history.diff`
   - `current_arbitration.diff`
   - `.coder_session`
   - `.coder_state.json`
   - `build_preflight.log`
   - `.tmp/`
3. Ensure that the logic checks if an artifact is already excluded before appending it to avoid duplicate entries in `.git/info/exclude`.
4. Ensure the output message `Initialized local sandbox: added .sdlc_runs/ to .git/info/exclude` is updated to reflect that multiple artifacts are now added (e.g. `added .sdlc_runs/ and runtime artifacts to .git/info/exclude`).

## 3. Architecture & Impact
- **File modified:** `scripts/orchestrator.py`
- This is a safe, backwards-compatible change that only enhances the robustness of the orchestrator in virgin workspaces.

## 4. Acceptance Criteria
- [ ] `orchestrator.py` correctly appends the list of artifacts to `.git/info/exclude` if they are not already present.
- [ ] No syntax errors introduced.
