status: closed

# PR-1041-2: Orchestrator Prompt Decoupling and Security Refactor

## 1. Objective
Decouple overloaded error prompts in the orchestrator by wiring in the newly created specific prompts, and refactor security violation outputs.

## 2. Scope (Functional & Implementation Freedom)
- Replace generic or overloaded error prompt fallbacks in the orchestrator logic with the newly introduced specific prompts (for invalid boundaries, locks, and validation failures).
- Rewrite the output statements for security violations using a "Strong Block + Weak Disclaimer" pattern to prevent bypass loops.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. The orchestrator logic must trigger specific boundary, lock, and validation error prompts instead of a generic fallback.
2. Security violation outputs must be formatted using the Strong Block + Weak Disclaimer pattern.
3. The Coder MUST write or update tests to verify the correct prompts are triggered under the respective error conditions. All tests MUST pass (GREEN) before submitting.
