status: superseded

# PR Contract: PR_02_Reviewer_Prompt_Context_Isolation

## Context
The prompt generated for the Reviewer does not properly isolate current changes from previously merged changes, leading to false-positive rejections. It also needs to be updated to output the new JSON format expected by the Orchestrator.

## Tasks for Coder
1. Refactor the prompt generation logic (e.g. `scripts/spawn_reviewer.py`) to cleanly isolate `recent_history.diff` (read-only reference) from `current_review.diff` (target for security checks/redlines).
2. Update the prompt instructions to mandate that the final verdict is output in strict JSON format matching what the Orchestrator now expects.
3. Add unit tests validating that the generated prompts contain clear, unambiguous section headers separating history from the current diff.

## Constraints
- The reviewer must be strictly instructed to only apply validations to `current_review.diff`.
- Must include failing tests and their passing implementation in this single PR.
- CI pipeline must pass (100% green tests).