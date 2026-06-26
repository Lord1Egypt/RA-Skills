# PRD_030: Stateful Coder Sessions (Yellow Path Amnesia Fix)

## 1. Problem Statement
In the current implementation of the Yellow Path (Review-Correction Loop), when the Manager receives an `[ACTION_REQUIRED]` from the Reviewer, it calls `scripts/spawn_coder.py --feedback-file ...` to initiate a revision. 
However, the `spawn_coder.py` script hardcodes the agent session generation to use a random UUID (`session_id = f"subtask-{uuid.uuid4().hex[:8]}"`). 
This means the OpenClaw runtime instantiates a completely blank, new Coder agent for the revision. This new Coder lacks the critical **Internal Reasoning Context** (why it wrote the code the way it did in the previous attempt) and only has the diff and the feedback to guess what to fix. This "amnesia" drastically reduces the LLM's capability to resolve complex, multi-step bugs.

## 2. Solution: Deterministic Session Continuity
We must transition the Coder from a "Stateless One-Shot" execution to a "Stateful Thread-Bound" execution tied to the lifecycle of a specific PR Contract.

### 2.1 Refactor `scripts/spawn_coder.py`
- **Session ID Derivation**: Instead of a random UUID, the `session_id` MUST be deterministically derived from the PR Contract filename.
  - Example: If `--pr-file` is `.sdlc/jobs/Feature_X/PR_001_DB.md`, extract the base name (`PR_001_DB`) and generate `session_id = f"coder-{pr_base_name}"`.
- **Context Injection Handling**:
  - When `--feedback-file` is **NOT** provided (first attempt), the script sends the full initial context (`task_string` with PR and PRD).
  - When `--feedback-file` **IS** provided (revision loop), the script should **NOT** resend the massive PR/PRD prompt. The stateful session already knows the task. The script should only send the short, focused prompt:
    `"--- Revision Feedback ---\n{feedback_content}\n\nYou are in a revision loop. Your previous attempt was rejected. Address the feedback above and modify the codebase accordingly."`
- **Session Replay Flag**: Ensure the OpenClaw CLI call (`openclaw agent`) natively handles resuming the same session ID. (OpenClaw's SQLite backend automatically replays the conversation history if the ID matches).

## 3. Testing Strategy
To prove that the Coder retains its memory across calls, we must test its conversational continuity without writing real code.

### 3.1 E2E Sandbox Verification (`scripts/test_coder_memory.sh`)
Create a focused test script:
1. **Initial Run (State Creation)**:
   - Call `spawn_coder.py` with a dummy PR and PRD. 
   - Inject a secret into the initial prompt (e.g., "MANDATORY SECRET KEY: 42. Do not forget this.").
2. **Revision Run (State Retrieval)**:
   - Create a dummy `--feedback-file` that says: "You failed. What is the secret key I told you in the first prompt? Write it to `memory_proof.txt`."
   - Call `spawn_coder.py` with the feedback file.
3. **Assertion (Physical Artifact)**:
   - Assert that `memory_proof.txt` exists and contains `42`.
   - If it does, the Coder successfully accessed the conversation history of the previous session.

## 4. Acceptance Criteria
- [ ] `spawn_coder.py` generates deterministic `session_id`s based on the `--pr-file` name.
- [ ] `spawn_coder.py` sends a minimized prompt when `--feedback-file` is present, relying on session state.
- [ ] The `test_coder_memory.sh` script successfully asserts that the Coder remembers a secret injected in a previous call.