status: closed

# PR Contract: PR_02B_Orchestrator_JSON_Review_Parsing

## Context
The Orchestrator relies on naive string matching (`[LGTM]`) to determine PR approval, which can be bypassed if a rejection comment includes that string. This PR switches the review process to a strict JSON format.

## Tasks for Coder
1. Update `scripts/spawn_reviewer.py` prompt instructions to mandate that the final verdict is output in strict JSON format (e.g., `{"status": "APPROVED", "comments": "..."}`).
2. Update `scripts/orchestrator.py` review validation logic to parse structured JSON instead of string matching.
3. Add a unit test where the Orchestrator is fed an adversarial Reviewer output (e.g., a rejection reason containing the literal string `[LGTM]`). Ensure the JSON parser correctly interprets it as a rejection.

## Constraints
- Must include both the failing tests and their passing implementation in this single PR.
- CI pipeline must pass (100% green tests).
