# PRD_076: Defensive Pre-Review Force Commit (Anti-Ghost-Change)

## 1. Problem Statement
A critical vulnerability was identified in the SDLC pipeline: between State 3 (Coder) and State 4 (Reviewer), the Coder agent (or external factors) might leave uncommitted "dirty" files in the working tree (e.g., trailing dummy comments, un-added files). 
Because these files are uncommitted, they are invisible to the Reviewer's `git diff` audit. Worse, when the pipeline reaches State 6 (Merge) and attempts to `git checkout master`, Git strictly halts the process to prevent overwriting these dirty files, causing a system-level pipeline crash.

## 2. Solution (The "Collect All Drafts" Strategy)
Instead of silently wiping these dirty files (`git clean`), the system MUST forcibly commit them to the repository history just before the Reviewer steps in.
This "Fail-Fast" architectural decision achieves two goals:
1. **Evidence Fixation**: All modifications (intentional, hallucinatory, or malicious) are permanently logged in the git tree.
2. **Exposed to Audit**: The Reviewer will see these previously hidden changes in the diff and can logically reject the PR (`[ACTION_REQUIRED]`) if they are unauthorized, converting a physical Git crash into a graceful logical pipeline failure.

**Implementation Details:**
In `scripts/orchestrator.py`, immediately prior to transitioning to **State 4 (Spawning Reviewer)**, execute a mandatory catch-all commit:
```python
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "chore(auto): force commit uncommitted changes before review"], check=False)
```

## 3. Scope
- **Target Project:** `/root/.openclaw/workspace/projects/leio-sdlc`
- **Files to Modify:** `scripts/orchestrator.py`

## 4. Testing Strategy
- **Autonomous Test Strategy:** Write a unit/integration test (e.g., `tests/test_076_force_commit.sh`) that simulates a Coder leaving an untracked dirty file. Verify that the Orchestrator successfully commits it with the "chore(auto)" message before spawning the mock Reviewer.
- **TDD Guardrail:** The implementation and its failing test MUST be delivered in the same PR contract.
