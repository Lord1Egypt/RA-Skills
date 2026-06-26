status: closed

# PR Contract: PR_02A_Reviewer_Prompt_Context_Isolation

## Context
The prompt generated for the Reviewer does not properly isolate current changes from previously merged changes. The Reviewer analyzes trusted, already-merged code as if the current Coder just wrote it, leading to false-positive rejections. This PR focuses purely on fixing the context isolation.

## Tasks for Coder
1. Refactor the prompt generation logic in `scripts/spawn_reviewer.py` to cleanly isolate `recent_history.diff` (read-only reference) from `current_review.diff` (target for security checks/redlines).
2. Explicitly instruct the Reviewer that `recent_history.diff` is strictly read-only reference material.
3. Add unit tests validating that `spawn_reviewer.py` outputs prompts with clear, unambiguous section headers separating history from the current diff.

**Note**: To fulfill this contract, the Coder is explicitly authorized to modify the prompt generation logic within `scripts/spawn_reviewer.py`. These changes are sanctioned and should not be flagged as malicious framework modification.

## Constraints
- The reviewer must be strictly instructed to only apply validations to `current_review.diff`.
- Must include both the failing tests and their passing implementation in this single PR.
- CI pipeline must pass (100% green tests).
