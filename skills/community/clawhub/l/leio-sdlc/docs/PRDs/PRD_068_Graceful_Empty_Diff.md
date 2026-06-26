# PRD-068: Graceful Empty Diff Handling & Context-Aware Reviewer

## 1. Problem Statement
The SDLC orchestrator currently suffers from the "Coder's Dilemma" (Reward Hacking & Empty Diff Crashes). When a Coder "over-delivers" in an early PR (e.g., implements Feature A and B in PR_1), the subsequent PR_2 (requesting Feature B) becomes redundant.
Currently:
1. The Orchestrator crashes if a Coder submits an empty diff (`Git working tree is completely clean`).
2. The Reviewer evaluates exclusively on `current_review.diff`. If a required feature is missing from the diff (because it was already implemented in `master`), the Reviewer incorrectly rejects the PR.

## 2. Solution
We must implement a **Context-Aware Triad** with a parameterized history heuristic to gracefully handle already-completed work.

### 2.1. Parameterized History Depth
- Introduce a dynamic history extraction mechanism for the Reviewer.
- The number of commits to check should be defined as: `history_depth = max(5, number_of_preceding_prs_in_current_batch)`.
- Default to `5` if the preceding PR count is unknown or less than 5.
- The Orchestrator/Reviewer runner will execute `git log -n <history_depth> -p > recent_history.diff`.

### 2.2. Empty Diff Graceful Bypass
- Remove hard crash pre-flight checks (e.g., in `spawn_reviewer.py` or `orchestrator.py`) that fail when the working tree is clean.
- If the git status is clean, generate a synthetic `current_review.diff` containing exactly: `[EMPTY DIFF] The Coder made no changes in this PR.`

### 2.3. Context-Aware Reviewer Playbook
- Inject `recent_history.diff` into the Reviewer's workspace.
- Update `playbooks/reviewer_playbook.md` (and the system prompt in `spawn_reviewer.py`) with an Exemption Clause: 
  > "If a requirement from the PR Contract is missing in `current_review.diff` (or if the diff is `[EMPTY DIFF]`), you MUST read `recent_history.diff`. If the requirement was implemented in a recent commit, mark it as SATISFIED and output `[LGTM]`. Do not reject for a missing diff if the feature exists in recent history."

## 3. Testing Strategy (TDD)
A new integration test (`tests/test_068_empty_diff_graceful_skip.sh`) MUST be created to validate this flow.

### 3.1. Test Setup
1. Initialize a dummy Git workspace.
2. Commit a file `app.py` that implements BOTH "Feature A" and "Feature B". (Simulating over-delivery).
3. Create a PR Contract `PR_002.md` that explicitly requires ONLY "Feature B".

### 3.2. Execution & Assertions
1. Run the Reviewer agent against this workspace with an empty working tree (`git status` is clean).
2. **Assertion 1**: The Orchestrator/Reviewer runner does NOT crash with a `Pre-flight Failed: working tree clean` error.
3. **Assertion 2**: `recent_history.diff` is generated containing the commit for Feature B.
4. **Assertion 3**: The Reviewer successfully outputs `[LGTM]` in `Review_Report.md`, acknowledging that the feature is already present in the recent history.