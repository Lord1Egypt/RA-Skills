# PRD_025: Yellow Path (Review-Correction Loop)

## 1. Context & Objective
The SDLC `v0.2` Architecture Blueprint defines a "Yellow Path" (局部自愈) for handling code review rejections (`[ACTION_REQUIRED]`). Currently, the pipeline is mostly linear ("Green Path"). We need to introduce a feedback loop mechanism allowing the Manager to pass the Reviewer's feedback back to the Coder for a revision, up to a threshold of MAX_REVISIONS (default 5) times.

## 2. Requirements & Implementation Scope

### Phase 1: Engine Support for Feedback (Coder's End)
The Coder must be able to read and understand the Reviewer's rejection reasons.
- **Modify `scripts/spawn_coder.py`**:
  - Add an optional argument `--feedback-file`.
  - If provided, the script should read the file's content and append a "Revision Feedback" section to the `task_string` given to the Coder agent.
  - The prompt should instruct the Coder to: "You are in a revision loop. Your previous attempt was rejected. Address the following feedback and modify the codebase accordingly."

### Phase 2: Manager Loop Logic (Playbook / Prompting)
The Manager must know how to route an `[ACTION_REQUIRED]` status back to the Coder.
- **Modify `SKILL.md` (leio-sdlc Runbook)**:
  - Add a new "Command Template 2b: Spawning a Coder for Revision (Correction Loop)".
  - Specify the exact command: `python3 {baseDir}/scripts/spawn_coder.py --pr-file <path_to_pr> --prd-file <path_to_prd> --feedback-file <path_to_review_report>`.
  - Add a directive to the Manager: "If the Reviewer generates a `Review_Report.md` containing `[ACTION_REQUIRED]`, do NOT merge. You must execute a Correction Loop: run the Coder Revision command, then run the Reviewer command again. Repeat this loop up to MAX_REVISIONS (default 5, but can be customized) times or until `[LGTM]` is given."

### Phase 3: Sandbox Sandbox Test (`scripts/test_e2e_yellow_path.sh`)
Create an E2E test to enforce the Manager's looping behavior.
- **Create `scripts/test_e2e_yellow_path.sh`**:
  - Initialize the sandbox similarly to `test_manager_e2e.sh`.
  - **Mocking the Reviewer**: In the sandbox, overwrite or wrap the `scripts/spawn_reviewer.py` with a deterministic mock script. 
    - The mock script will read a local file `.review_count` (starting at 0).
    - If count < 2: increment count, write a fake `Review_Report.md` starting with `[ACTION_REQUIRED]\nPlease add a docstring to hello.py`.
    - If count == 2: increment count, write a fake `Review_Report.md` starting with `[LGTM]\nGood job.`.
  - **Manager Prompt**: Instruct the Manager to execute the full pipeline and handle rejections according to the Yellow Path rules. "Do not stop until the final LGTM is given and code is merged."
  - **Assertions**: 
    - Assert that `.review_count` contains `3`.
    - Assert that `hello.py` exists and the final commit is merged.
    - Assert that the stdout log of the Manager contains evidence of executing `spawn_coder.py` with `--feedback-file` multiple times.

## 3. Acceptance Criteria
- [ ] `spawn_coder.py` accepts and processes `--feedback-file`.
- [ ] `SKILL.md` defines the Correction Loop command and instructions.
- [ ] `test_e2e_yellow_path.sh` successfully simulates 2 rejections and 1 acceptance.
- [ ] The Manager agent correctly parses the `Review_Report.md`, executes the feedback loop twice, and finally merges.
- [ ] The E2E test passes with return code 0.