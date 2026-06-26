status: closed

# PR Contract: PR_01_Orchestrator_JSON_Parsing

## Context
The Orchestrator currently relies on naive string matching (`[LGTM]`) to approve PRs, which allows for security bypasses if a Reviewer rejects a PR but quotes the string. We need to deprecate text-based string matching and use strict JSON parsing for review status.

## Tasks for Coder
1. Refactor review validation logic in the orchestrator (e.g. `scripts/orchestrator.py`) to parse a structured JSON object (e.g., `{"status": "APPROVED", "comments": "..."}`) to determine review status deterministically.
2. Create unit tests for the Orchestrator Review Parsing logic. The tests must include an adversarial Reviewer output where the rejection reason contains the literal string `[LGTM]`, ensuring the JSON parser correctly interprets it as a rejection.

## Constraints
- Do not use string matching for approval status.
- Must include failing tests and their passing implementation in this single PR.
- CI pipeline must pass (100% green tests).