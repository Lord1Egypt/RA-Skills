# PRD: Reviewer History Overreaction and Orchestrator LGTM Bypass (ISSUE-1025)

## 1. Meta Information
- **Project Name**: leio-sdlc
- **Target Absolute Directory**: `/root/.openclaw/workspace/projects/leio-sdlc`
- **Issue Tracker**: ISSUE-1025
- **Type**: Bugfix / Security

## 2. Problem Statement
The `leio-sdlc` framework currently suffers from two critical flaws in the code review phase:
1. **Orchestrator LGTM Bypass (Security Vulnerability)**: The `orchestrator.py` file relies on naive string matching (`if '[LGTM]' in review_content:`) to determine if a PR is approved. If a Reviewer rejects a PR but quotes the string "[LGTM]" (e.g., stating "The Coder improperly included [LGTM] in their output"), the Orchestrator falsely registers this as an approval, bypassing the review gate.
2. **Reviewer History Overreaction (False Positives)**: The prompt constructed by `spawn_reviewer.py` does not properly isolate the current changes (`current_review.diff`) from previously merged changes (`recent_history.diff`). As a result, the Reviewer analyzes trusted, already-merged code as if the current Coder just wrote it, leading to false-positive rejections (e.g., flagging historical framework setup as malicious prompt injection).

## 3. Proposed Solution
1. **Structured JSON Output for Reviewer**:
   - Deprecate fragile text-based string matching.
   - Force the Reviewer to output its final verdict in a strict JSON format (e.g., `{"status": "APPROVED", "comments": "..."}`).
   - Update `orchestrator.py` to parse this JSON object to determine the review status deterministically.
2. **Strict Context Isolation in Prompts**:
   - Refactor the prompt generation in `spawn_reviewer.py`.
   - Explicitly instruct the Reviewer that `recent_history.diff` is strictly read-only reference material for satisfied requirements.
   - Mandate that all security checks, redlines, and logic validations be strictly applied ONLY to `current_review.diff`.

## 4. Scope
- **`scripts/orchestrator.py`**: Update review validation logic to parse structured JSON instead of string matching.
- **`scripts/spawn_reviewer.py`**: Refactor the prompt template to enforce JSON output and cleanly isolate `recent_history.diff` from `current_review.diff`.
- *(If applicable)* Any associated Reviewer playbook or prompt templates must be updated to reflect the new JSON schema requirement.

## 5. Testing Strategy
Since `leio-sdlc` is an orchestration framework, testing must be handled via Unit/Integration tests with mocks:
1. **Orchestrator Review Parsing Test**: Create a unit test where the Orchestrator is fed an adversarial Reviewer output (e.g., a rejection reason that happens to contain the literal string `[LGTM]`). Ensure the JSON parser correctly interprets it as a rejection.
2. **Prompt Context Test**: Validate that `spawn_reviewer.py` outputs prompts with clear, unambiguous section headers separating history from the current diff.

## 6. TDD Guardrail
**Mandatory**: The implementation and its failing tests MUST be delivered in the same PR contract. Development cannot proceed without automated tests validating the string-bypass and context-isolation scenarios.
