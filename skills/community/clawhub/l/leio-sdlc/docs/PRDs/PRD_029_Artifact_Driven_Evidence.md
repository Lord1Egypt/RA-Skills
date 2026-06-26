# PRD_029: Artifact-Driven Evidence Chain (物证驱动架构)

## 1. Problem Statement
The current E2E test suite (ISSUE-027) failed because the Manager agent bypassed the actual SDLC scripts and hallucinated a successful output (`[E2E_MANAGER_SUCCESS]`) to stdout. Our assertions were flawed because they relied on parsing LLM conversational output (`grep`) rather than validating physical artifacts. To achieve a deterministic pipeline, every agent role must leave an undeniable physical footprint (Artifact) on the filesystem, which the next stage (or the test runner) asserts.

## 2. Artifact Specifications
1. **Planner**: Must output `PR_xxx.md` files in `.sdlc/jobs/<PRD_NAME>/`. (Already functioning, needs assertion).
2. **Coder**: Must execute `write`/`edit` tools on the codebase AND perform a `git commit`. (Needs assertion).
3. **Reviewer**: Currently outputs `[LGTM]` to stdout. **CRITICAL FLAW**. The Reviewer MUST output a physical `Review_Report.md` file in `.sdlc/jobs/<PRD_NAME>/` containing the verdict (`[LGTM]` or `[ACTION_REQUIRED]`) and the review details.
4. **Manager / E2E Test**: Must assert the pipeline's success by checking for the physical existence of these files and git states, not by reading conversational logs.

## 3. Implementation Plan (Refactoring Scope)

### 3.1 Refactor Reviewer Output (`playbooks/reviewer_playbook.md` & `scripts/spawn_reviewer.py`)
- **playbooks/reviewer_playbook.md**: Change the final instruction. Instead of "Output [LGTM] or [ACTION_REQUIRED]", it must explicitly state: "You MUST use the `write` tool to create a file named `Review_Report.md` in the current job directory containing exactly `[LGTM]` or `[ACTION_REQUIRED]` on the first line, followed by your reasoning."
- **scripts/spawn_reviewer.py**: Pass the `job_dir` (e.g., `.sdlc/jobs/Feature_X/`) to the Reviewer's task string so it knows where to write the `Review_Report.md`.

### 3.2 Refactor E2E Sandbox Assertions (`scripts/test_manager_e2e.sh`)
- **Remove** the flawed stdout `grep` assertion (`grep -q "\[E2E_MANAGER_SUCCESS\]" manager_e2e.log`).
- **Add Physical Assertions**:
  1. **Planner Proof**: `[ -n "$(ls .sdlc/jobs/*/PR_*.md 2>/dev/null)" ]` (or similar glob match to prove a PR was created).
  2. **Coder Proof**: `[ -f hello.py ]` (The requested file exists) AND `git log -1 --oneline | grep -v init` (Proves a new commit was made).
  3. **Reviewer Proof**: `[ -n "$(ls .sdlc/jobs/*/Review_Report.md 2>/dev/null)" ]` AND `grep -q "\[LGTM\]" .sdlc/jobs/*/Review_Report.md` (Proves the reviewer physically stamped the approval).
- **Prompt Update**: Tell the Manager to execute the scripts and ensure the artifacts (PRs, Code, Review Report) are generated. It no longer needs to output a special string.

## 4. Acceptance Criteria
- [ ] Reviewer Agent uses the `write` tool to generate a physical `Review_Report.md` in the `.sdlc/jobs/` directory.
- [ ] `test_manager_e2e.sh` asserts physical artifacts (PRs, Code, Review_Report, Git Commits).
- [ ] The E2E test successfully runs the Manager, executing the pipeline and generating all required artifacts.
- [ ] Stdout string parsing is removed from E2E assertions.
