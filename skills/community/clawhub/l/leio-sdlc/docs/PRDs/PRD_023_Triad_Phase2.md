# PRD_023_Phase2: Triad Coherence Testing for Planner & Coder

## 1. Problem Statement
With the Reviewer's "Triad Coherence Test" (testing the `script + playbook + prompt` integration against LLM hallucinations) successfully implemented in Phase 1, we must extend this rigorous physical isolation testing to the Planner and Coder subagents. This guarantees that all three pillars of the Agentic SDLC remain stable across prompt or model updates.

## 2. Goals
- Create `scripts/test_triad_planner.sh`: A sandbox test verifying the Planner reads a PRD and produces a structured markdown PR Contract.
- Create `scripts/test_triad_coder.sh`: A sandbox test verifying the Coder reads a PR Contract and uses the `write` tool to actually generate code on disk.

## 3. Implementation Details

### 3.1 Planner Triad Test (`scripts/test_triad_planner.sh`)
- **Setup Sandbox**: Create `tests/dummy_triad_prd.md` containing a specific fake requirement (e.g., "Feature: Implement PL-999 auto-router").
- **Trigger**: Unset `SDLC_TEST_MODE`. Run `python3 scripts/spawn_planner.py --prd-file tests/dummy_triad_prd.md > tests/triad_planner.log 2>&1`.
- **Assertions**:
  - Positive Assertion: `grep` the log for the specific requirement keyword ("PL-999") to ensure it comprehended the PRD.
  - Positive Assertion: `grep` the log for markdown headings (e.g., `grep -E "^#.*"`) to ensure it outputs structured text, not just a conversational "OK".

### 3.2 Coder Triad Test (`scripts/test_triad_coder.sh`)
- **Setup Sandbox**: 
  - Create `tests/dummy_triad_prd_coder.md`.
  - Create `tests/dummy_triad_pr_coder.md`. The PR Contract must explicitly instruct the Coder to: "Use the write tool to create a file at `tests/dummy_generated_output.py` containing exactly `print('CODER_TRIAD_SUCCESS')`".
- **Trigger**: Unset `SDLC_TEST_MODE`. Run `python3 scripts/spawn_coder.py --pr-file tests/dummy_triad_pr_coder.md --prd-file tests/dummy_triad_prd_coder.md > tests/triad_coder.log 2>&1`.
- **Assertions (Behavioral Validation)**:
  - Check if the file `tests/dummy_generated_output.py` exists (e.g., `[ -f tests/dummy_generated_output.py ]`).
  - `grep` the contents of `tests/dummy_generated_output.py` to ensure it contains exactly `CODER_TRIAD_SUCCESS`.
- **Cleanup**: Remove all dummy files and the generated script.

## 4. Acceptance Criteria
- [ ] Both test scripts are implemented as executable bash scripts in `scripts/`.
- [ ] They unset `SDLC_TEST_MODE` to force real LLM calls via the newly refactored CLI spawns.
- [ ] The Coder test successfully validates physical file creation by the LLM tool call.