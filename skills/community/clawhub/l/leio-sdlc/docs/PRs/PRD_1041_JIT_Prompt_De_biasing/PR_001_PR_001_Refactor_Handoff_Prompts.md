status: closed

# PR-1041-1: Refactor and Expand Handoff Prompts

## 1. Objective
Refactor existing JIT handoff prompts to prioritize safe state preservation and add specific prompts for granular error handling.

## 2. Scope (Functional & Implementation Freedom)
- Update existing dirty workspace prompts to explicitly instruct the use of state-preserving commands (like stash) and strictly forbid destructive commands.
- Update the happy path prompt to include explicit, multi-step instructions for closing the pipeline and updating tracking systems.
- Create new specific prompt definitions for startup validation failures, invalid repository boundaries, and active pipeline locks.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. The dirty workspace prompt must explicitly instruct the use of state preservation and not destructive commands.
2. The happy path prompt must include the required routing tags and the exact multi-step instructions for closure.
3. New prompts for validation failures, boundary issues, and locks must be defined with correct routing tags.
4. The Coder MUST write or update tests for these specific string generations/definitions. All tests MUST pass (GREEN) before submitting.
