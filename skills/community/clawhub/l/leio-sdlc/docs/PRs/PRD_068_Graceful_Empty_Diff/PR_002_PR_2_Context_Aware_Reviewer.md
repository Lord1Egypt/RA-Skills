status: closed

---

---
# PR-068.2: Context-Aware Reviewer Playbook

## Context
Now that the orchestrator passes empty diffs and generates recent history, the Reviewer needs to know how to interpret this to avoid falsely rejecting PRs.

## Requirements
1. Update `playbooks/reviewer_playbook.md` (and the system prompt in `spawn_reviewer.py` if applicable) with the Exemption Clause: "If a requirement from the PR Contract is missing in `current_review.diff` (or if the diff is `[EMPTY DIFF]`), you MUST read `recent_history.diff`. If the requirement was implemented in a recent commit, mark it as SATISFIED and output `[LGTM]`. Do not reject for a missing diff if the feature exists in recent history."
2. Ensure `recent_history.diff` is injected into the Reviewer's workspace/context.
3. Extend `tests/test_068_empty_diff_graceful_skip.sh` to execute the Reviewer agent against the dummy workspace with an empty working tree and assert that it successfully outputs `[LGTM]` in `Review_Report.md`.
