# PRD_031: Artifact-Driven Pre-flight Checks (Script-Level Guardrails)

## 1. Problem Statement
Despite implementing physical artifact checks in our E2E tests, the `leio-sdlc` Manager agent still has the technical freedom to execute workflow scripts (`spawn_*.py`, `merge_code.py`) out of order or before the necessary prerequisites exist. Relying purely on Prompt Engineering (`SKILL.md` instructions) to enforce this order is unreliable, as LLMs frequently suffer from "action hallucination" or skip steps. When a script is called out of order, the OpenClaw runtime blindly spawns the subagent, leading to wasted tokens, confused subagents, and corrupted Git states.

## 2. Solution: Hardcoded Pre-flight Guardrails
We will shift the enforcement of the SDLC state machine from "Soft Prompting" to "Hard Tool-Level Logic". All 4 core Python wrapper scripts will be refactored to perform physical artifact checks *before* making the expensive `subprocess.run(["openclaw", "agent", ...])` call. If a check fails, the script will instantly exit with `Code 1` and print an LLM-friendly, highly directive error message to snap the Manager back on track.

### Script Scope & Rules:
1. **`scripts/spawn_planner.py`**:
   - **Check**: The file specified by `--prd-file` must physically exist and must not be empty.
   - **LLM Correction Message**: `[Pre-flight Failed] Planner cannot start. PRD file not found at '{path}'. You must read or create the PRD first.`
2. **`scripts/spawn_coder.py`**:
   - **Check**: The file specified by `--pr-file` must physically exist.
   - **LLM Correction Message**: `[Pre-flight Failed] Coder cannot start. PR Contract not found at '{path}'. You must run spawn_planner.py first.`
3. **`scripts/spawn_reviewer.py`**:
   - **Check**: A `git diff HEAD` (or checking uncommitted/committed changes on the current branch) must not be empty. (If there is no code change, there is nothing to review).
   - **LLM Correction Message**: `[Pre-flight Failed] Reviewer cannot start. Git working tree is completely clean. The Coder did not write any code. You must spawn the Coder first.`
4. **`scripts/merge_code.py`**:
   - **Check**: Require a new argument `--review-file` and an optional flag `--force-lgtm`.
   - **Logic**: 
     - The file specified by `--review-file` MUST exist (proving a review occurred). If missing: `[Pre-flight Failed] Merge rejected. Review artifact '{path}' not found. You MUST run spawn_reviewer.py first.`
     - If `--force-lgtm` is NOT passed: The file content MUST contain the exact string `[LGTM]`. If missing: `[Pre-flight Failed] Merge rejected. The file '{path}' does not contain [LGTM]. You must fix the code and re-review, or use --force-lgtm to override a nitpicky Reviewer.`
     - If `--force-lgtm` IS passed: Skip the `[LGTM]` content check, allowing the Manager to override the Reviewer.

## 3. Testing Strategy
We will create a unit-test-style bash script to verify these guardrails without invoking the LLM.

**Test Script**: `scripts/test_preflight_guardrails.sh`
- **Setup**: Create an isolated Git sandbox.
- **Planner Test**: Call `spawn_planner.py` with a fake PRD path. Assert it exits with Code 1 and prints the `[Pre-flight Failed]` message.
- **Coder Test**: Call `spawn_coder.py` with a fake PR path. Assert it exits with Code 1.
- **Reviewer Test**: Call `spawn_reviewer.py` on a clean git directory. Assert it exits with Code 1.
- **Merge Test**: 
  - Call `merge_code.py` with a fake review file -> Assert Code 1.
  - Call `merge_code.py` with a review file containing `[ACTION_REQUIRED]` -> Assert Code 1.
  - Call `merge_code.py` with a review file containing `[ACTION_REQUIRED]` AND `--force-lgtm` -> Assert Code 0.
  - Call `merge_code.py` with a review file containing `[LGTM]` -> Assert Code 0 (or mock success).

## 4. Acceptance Criteria
- [ ] All 4 Python scripts have been updated with physical pre-flight assertions and LLM-friendly `[Pre-flight Failed]` stdout messages.
- [ ] `merge_code.py` accepts `--review-file` and `--force-lgtm` arguments.
- [ ] `SKILL.md` Runbook is updated to instruct the Manager on how to use `--force-lgtm` to override pedantic reviews.
- [ ] The `test_preflight_guardrails.sh` script is created and all negative/override assertions pass perfectly.