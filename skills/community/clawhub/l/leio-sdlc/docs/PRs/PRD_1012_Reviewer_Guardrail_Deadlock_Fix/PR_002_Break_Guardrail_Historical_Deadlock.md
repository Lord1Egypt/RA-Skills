status: completed

# PR-002: Break Guardrail Historical Deadlock

## 1. Objective
Prevent the security guardrail scanner from tripping on legitimate historical modifications by restricting its scan scope exclusively to the current PR's diff.

## 2. Scope (Functional & Implementation Freedom)
- Modify the guardrail scanning invocation so it only audits the current accumulative diff.
- Ensure historical diffs are removed from the security scanner's target list (but can still be provided to the LLM for context, if applicable outside the scanner).
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
- Implement a Historical Immunity Test: Modify a protected file on the main branch, commit it, then run the reviewer on a feature branch with benign changes. The guardrail MUST NOT fail.
- Implement an Active Tamper Test: Maliciously modify a protected file on a feature branch and commit it. The reviewer MUST successfully detect the tamper and fail.
- The Coder MUST ensure all tests run GREEN before submitting.