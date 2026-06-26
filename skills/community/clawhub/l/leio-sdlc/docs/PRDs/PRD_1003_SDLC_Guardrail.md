# PRD: Implement .sdlc_guardrail File for Strict Workspace Boundaries (ISSUE-1003)

## 1. Problem Statement
Currently, the Reviewer strictly rejects a Coder's PR if it modifies files not explicitly listed in the PR Contract (Anti-Reward Hacking Guardrail). However, this is too rigid for real-world development, as Coders often need to create legitimate auxiliary files (like `adapter.py` or `__init__.py`) to resolve dependencies or refactor code. Conversely, we must still prevent the Coder from maliciously modifying framework artifacts (e.g., `Review_Report.md`, `preflight.sh`, `.coder_session`, `TEMPLATES/`) to prevent reward hacking.

## 2. Goal & Solution
Introduce a declarative `.sdlc_guardrail` configuration file to define strict workspace boundaries. The Reviewer will use this file to distinguish between legitimate auxiliary file creation and malicious framework tampering, ensuring the "Fat Coder" has freedom elsewhere but cannot touch framework files.

## 3. Scope Locking
**Target Project Directory:** `/root/.openclaw/workspace/projects/leio-sdlc`

## 4. Action Items
1. **Implement `.sdlc_guardrail` File Standard:** Create a declarative `.sdlc_guardrail` file that explicitly lists off-limits files/directories (e.g., `.sdlc/`, `Review_Report.md`, `.coder_session`, `preflight.sh`, `run.sh`, `TEMPLATES/`) unless explicitly authorized by the PRD.
2. **Update Reviewer's Evaluation Logic:** Modify the Reviewer's Prompt Playbook to relax the strict 'PR scope' matching rule, allowing the Coder to create new auxiliary files, BUT strictly enforce a ban on modifying any file listed in the `.sdlc_guardrail`.
3. **Standardize Project Scaffolding:** Ensure every new project inherits a standard `.gitignore`, `.sdlc_guardrail`, and `.release_ignore`.

## 5. Autonomous Test Strategy
**Test Type:** Integration Testing & Reviewer Simulation
**Strategy:**
- Create a mock PR that attempts to modify a file listed in the `.sdlc_guardrail` (e.g., `Review_Report.md`) and verify the Reviewer rejects it.
- Create a mock PR that creates a benign auxiliary file (e.g., `adapter.py`) not listed in the `.sdlc_guardrail` and verify the Reviewer accepts it.
- Ensure the Reviewer logic correctly parses and applies the `.sdlc_guardrail` rules.

## 6. TDD Guardrail
The implementation and its failing test (e.g., test scripts simulating the Reviewer logic against a violation and a non-violation) MUST be delivered in the same PR contract.
