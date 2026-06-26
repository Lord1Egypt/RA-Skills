status: open

# ISSUE-1007: SDLC State Machine Robustness & Pause/Resume Resilience

## 1. Problem Statement
The SDLC Orchestrator relies strictly on filesystem artifacts (`docs/PRs/*.md` status fields) to maintain and synchronize its Finite State Machine (FSM). This architectural choice correctly assumes that LLM context is ephemeral and untrustworthy.

However, during emergency manual interventions (e.g., hard Git resets or workspace cleanups to resolve underlying infrastructure blockers), the physical code state can diverge from the persistent FSM state files. When the Orchestrator resumes, it reads the stale FSM files, causing fatal desynchronization:
- **Symptom 1**: The Orchestrator believes a PR is pending, but the underlying code is already merged. The Coder agent checks out the branch, sees no work needed, and submits an empty diff.
- **Symptom 2**: The Reviewer agent immediately rejects the empty diff. The Orchestrator loops infinitely, unable to reconcile the state.
- **Root Cause**: Manual or external interference destroys the parity between the FSM representation (markdown files) and the actual Git repository state.

## 2. Proposed Solution
The SDLC engine requires a hardened, self-healing state machine that guarantees robust pause/resume capabilities and absolute protection against state divergence.

### Implementation Goals:
1. **State Parity Verification on Boot**:
   - The Orchestrator MUST perform a "State Parity Check" upon initialization.
   - It must cross-reference the status in `docs/PRs/*.md` against the actual Git history (e.g., checking if the corresponding PR branch exists or if its commits are already in `master`).
   - If divergence is detected, the Orchestrator should trigger a safe auto-correction routine or halt with a clear "State Desync" error requiring manual resolution, rather than blindly trusting the text file.
2. **Atomic State Transitions**:
   - The FSM transitions (e.g., `in_progress` -> `review` -> `completed`) must be tightly coupled with Git operations. A state file update should only be committed in the exact same transaction as the code merge.
3. **Resilient Pause/Resume**:
   - Introduce a formal `sdlc pause` and `sdlc resume` mechanism.
   - A `STATE_LOCK` file or snapshot mechanism should capture the exact commit hash and FSM status to ensure that resumes are immune to intermediate tampering.

## 3. Acceptance Criteria
- A test case demonstrating that modifying the Git history externally (e.g., `git reset --hard`) while a PR is marked as `in_progress` does not cause an infinite loop upon resumption. The Orchestrator must detect the desync.
- The Orchestrator can be safely halted mid-PR, the workspace modified, and safely resumed without FSM corruption.
