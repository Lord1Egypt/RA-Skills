status: blocked_fatal

# PR-002: Secure Prompt Injection and Global Directory Propagation

## 1. Objective
Refactor agent spawners to securely pass large prompts using atomic, permission-restricted temporary files, and propagate the absolute global workspace directory for reliable template resolution.

## 2. Scope (Functional & Implementation Freedom)
Update the execution layer (spawners) to use secure temporary files for prompt strings to prevent E2BIG errors and CWE-377 vulnerabilities. Ensure these files are strictly `0o600` permissions and are deleted automatically after execution via `try...finally`. Modify the orchestrator to resolve and pass the absolute global directory path down to all spawners.
*The Coder MUST search the workspace, understand the existing code structure, and autonomously decide which files to create or modify to implement this logic.*

## 3. TDD & Acceptance Criteria
1. Implement an integration test (`test_secure_prompt.sh`) that asserts spawners use a secure temporary file with `0o600` permissions and that the file is deleted immediately after the subprocess completes (no zombie files).
2. The orchestrator must successfully pass the absolute global directory down to the spawners.
3. The Coder MUST ensure all tests run GREEN before submitting. Test scripts and implementation must be delivered in this exact PR.