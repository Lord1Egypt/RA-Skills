status: closed

# PR-002: Enforce Guardrail in Reviewer Logic

## 1. Objective
Modify the Reviewer's evaluation logic to dynamically enforce the `.sdlc_guardrail` rules, allowing benign auxiliary file creation while strictly blocking framework tampering.

## 2. Scope (Functional & Implementation Freedom)
- Update the Reviewer agent or evaluation module to read and parse the `.sdlc_guardrail` file.
- Relax the strict "exact PR scope match" rule. The Reviewer should now allow the Coder to modify or create files NOT listed in the PR contract, PROVIDED they do not match any patterns in the `.sdlc_guardrail`.
- Implement strict rejection for any attempt to modify files protected by the guardrail unless explicitly authorized.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Integration Test 1: Simulate a PR that modifies a protected file defined in `.sdlc_guardrail` (e.g., a review report or template). Assert that the Reviewer correctly REJECTS the PR.
- Integration Test 2: Simulate a PR that creates a new, benign auxiliary file (e.g., an adapter script) not listed in the `.sdlc_guardrail`. Assert that the Reviewer correctly ACCEPTS the PR.
- The Coder MUST ensure all tests run GREEN before submitting.