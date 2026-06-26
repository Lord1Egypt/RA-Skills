---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1052 Enterprise SDLC Isolation: sdlc init and Runtime Run Directories

## 1. Context & Problem Definition
Currently, the Orchestrator scatters runtime artifacts (`Review_Report.md`, `.coder_session`, `current_review.diff`, `recent_history.diff`, `.coder_state.json`) directly into the project root. This inherently clashes with `git clean -fd` in virgin workspaces and causes cross-run state poisoning (retaining failed states).
We need an enterprise CI/CD model: all temporary runtime artifacts must be contained within their respective `.sdlc_runs/<PR_folder>/` directories, leaving the project root completely sterile.

## 2. Requirements
1. Modify `scripts/orchestrator.py`, `scripts/spawn_coder.py`, `scripts/spawn_reviewer.py`, and `scripts/merge_code.py` to ensure ALL runtime artifacts are written to and read from a specific `.sdlc_runs/<PR_Name>/` context instead of the project root.
2. The artifacts include, but are not limited to:
   - `Review_Report.md` -> `.sdlc_runs/<PR_Name>/Review_Report.md`
   - `current_review.diff` -> `.sdlc_runs/<PR_Name>/current_review.diff`
   - `recent_history.diff` -> `.sdlc_runs/<PR_Name>/recent_history.diff`
   - `current_arbitration.diff` -> `.sdlc_runs/<PR_Name>/current_arbitration.diff`
   - `.coder_session` -> `.sdlc_runs/<PR_Name>/.coder_session`
   - `build_preflight.log` -> `.sdlc_runs/<PR_Name>/build_preflight.log`
3. **Forensic Quarantine Tracking (CRITICAL FIX):** The `.sdlc_runs/` directory will be globally ignored (e.g., via `.git/info/exclude`) to protect it from `git clean -fd`. However, to prevent forensic data loss and state leakage across branches, `orchestrator.py` MUST be updated during a State 5 Escalation (`--cleanup` or Tier 1 Reset): it MUST execute `git add -f .sdlc_runs/<PR_Name>/` to forcefully track the ignored directory into the "WIP: FORENSIC CRASH STATE" quarantine commit. This physically binds the forensic logs to the toxic branch, ensuring they disappear from the workspace when switching back to `master`.
4. **Config/Prompts Updates:** Update `config/prompts.json` and `scripts/handoff_prompter.py` to ensure all references to `Review_Report.md` reflect its new dynamic, nested location.
5. **Guardrail Updates:** Update the `.sdlc_guardrail` file (and its generation in `patch_guardrails.sh` if applicable) to protect `.sdlc_runs/` from malicious Coder modifications instead of the root-level `Review_Report.md`.
6. **E2E Test Suite Alignment:** Update ALL associated E2E bash tests (`scripts/test_*.sh`) and python tests to mock and assert artifacts in their new `.sdlc_runs/` locations.

## 3. Architecture & Framework Modifications
- **Allowed Modifications:**
  - `scripts/orchestrator.py`
  - `scripts/spawn_coder.py`
  - `scripts/spawn_reviewer.py`
  - `scripts/merge_code.py`
  - `scripts/spawn_arbitrator.py`
  - `config/prompts.json`
  - `scripts/handoff_prompter.py`
  - `.sdlc_guardrail`
  - `scripts/test_*.sh` (Any test script relying on root artifacts)

## 4. Acceptance Criteria
- [ ] No runtime artifacts (`Review_Report.md`, `.coder_session`, diffs) are generated in the project root.
- [ ] `git clean -fd` can be safely executed without deleting the active `Review_Report.md` (since `.sdlc_runs/` is excluded from git).
- [ ] Forensic quarantine branch successfully tracks the ignored `.sdlc_runs/` via `git add -f`.
- [ ] The full E2E test suite (`bash scripts/test_sdlc_cujs.sh`) passes successfully.

---

## Appendix: Architecture Evolution Trace (架构演进与审查追踪)
> **[CRITICAL INSTRUCTION FOR PLANNER & CODER]** 
> IGNORING THIS SECTION IS MANDATORY. This section is strictly for historical tracking of the PM-Auditor-Boss discussion loop. Do NOT read, reference, or implement any logic from this appendix into the SDLC pipeline.

- **v1.0**: Attempted to add `.tmp/` and `.coder_state.json` to `.git/info/exclude`. Rejected by Auditor because `git clean -fd` wouldn't clean them, leading to State Poisoning across retries.
- **v2.0**: Proposed `Review_Report.md` backup/restore during `git clean`. Boss rejected it as a hacky patch and suggested an enterprise CI/CD isolation model (Workspace-as-a-Job-Queue) where all runs live in `.sdlc_runs/<run_id>/`.
- **v3.0**: Drafted ISSUE-1052 to move everything to `.sdlc_runs/`. Rejected by Auditor because it broke `config/prompts.json`, `test_*.sh` mock artifacts, and `.sdlc_guardrail`.
- **v4.0**: Added prompts, tests, and guardrail updates to the Allowed Modifications. Rejected by Auditor because putting forensic logs in a git-ignored `.sdlc_runs/` directory would strip them from the `--cleanup` forensic WIP commit, violating Section 4.2.
- **v5.0 (Current)**: Finalized architecture by introducing `git add -f .sdlc_runs/<PR_Name>/` during State 5 Escalation to explicitly bind the ignored forensic logs to the toxic branch.
