---
Affected_Projects: [leio-sdlc]
---

# PRD: 1041 JIT Prompt De-biasing (v6)

## 1. Context & Problem Definition (核心问题与前因后果)
V5 was rejected because instructing the Manager to run `git restore/clean` on a dirty workspace poses a catastrophic data loss risk to human uncommitted code. We must NEVER instruct destructive commands like `git clean` or `git restore` in JIT prompts. We must strictly preserve state using `git stash` or abort. Furthermore, the current JIT error messages contain suggestive phrasing that misdirects the LLM's attention (e.g., bypassing security by appending parameters), requiring a refactor to a Strong Block + Weak Disclaimer pattern. We also need to decouple specific handoff prompts in `orchestrator.py` to be more precise about the failure reason (e.g., git boundaries vs. locks vs. dirty workspaces).

## 2. Requirements (需求说明)
1. **Routing Tags Preservation**: Retain all required routing tags (`[SUCCESS_HANDOFF]`, `[ACTION REQUIRED FOR MANAGER]`, etc.) intact across all prompts.
2. **orchestrator.py Security Violation Rewrite**: Replace the `fatal_crash` handoff call with `startup_validation_failed`. Rewrite the `print` statement using the Strong Block + Weak Disclaimer pattern.
3. **Decouple Handoff Prompts in orchestrator.py**:
   - Replace the `dirty_workspace` fallback for the `.git` directory and master/main branch checks with a new `invalid_git_boundary` prompt.
   - Replace the `dirty_workspace` fallback for the `.sdlc_repo.lock` BlockingIOError check with a new `pipeline_locked` prompt.
4. **handoff_prompter.py New Prompts**: Add exactly the following prompts:
   - `startup_validation_failed`: `[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nStartup validation failed. No system state was modified. Correct your CLI command/parameters and retry.`
   - `invalid_git_boundary`: `[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nInvalid Git boundary. You must run this from the root of a Git repository on the master/main branch.`
   - `pipeline_locked`: `[FATAL_LOCK]\n[ACTION REQUIRED FOR MANAGER]\nAnother SDLC pipeline is actively running in this workspace. You must wait for it to finish. DO NOT modify the workspace.`
5. **handoff_prompter.py dirty_workspace Rewrite (V6 FIX)**: Update the instruction to: `[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nWorkspace is dirty. There are uncommitted files. NEVER blindly delete or commit them! You MUST use 'git stash' to safely preserve the state, or abort and wait for human intervention.`
6. **handoff_prompter.py happy_path Rewrite**: Update the instruction to: `[SUCCESS_HANDOFF]\n[ACTION REQUIRED FOR MANAGER]\nThe pipeline has finished. You must now: 1. Update PRD status. 2. Close the Issue strictly using the full path to the issue_tracker skill: python3 ~/.openclaw/skills/issue_tracker/scripts/issues.py. 3. Update STATE.md. 4. Wait and Report completion to the Boss.`

## 3. Architecture (架构设计)
The architecture refines the interaction model between the SDLC pipeline and the LLM Manager. By strictly enforcing non-destructive commands in JIT prompts, we secure the human workspace against autonomous agent data loss. The decoupling of prompts provides exact, contextual feedback that steers the LLM toward correct behavior without inducing loop-failures. We apply the "Strong Block + Weak Disclaimer" pattern to prevent bypass loops.

## 4. Acceptance Criteria (验收标准)
- [ ] `orchestrator.py` is updated to use `startup_validation_failed` for security violations, and `print` statements use the Strong Block pattern.
- [ ] `orchestrator.py` correctly uses `invalid_git_boundary` and `pipeline_locked` instead of overloaded `dirty_workspace` fallbacks.
- [ ] `handoff_prompter.py` contains the exact strings for `startup_validation_failed`, `invalid_git_boundary`, and `pipeline_locked`.
- [ ] `handoff_prompter.py` updates the `dirty_workspace` string exactly as specified, instructing `git stash` instead of destructive actions.
- [ ] `handoff_prompter.py` updates the `happy_path` string exactly as specified.
- [ ] All required routing tags (`[SUCCESS_HANDOFF]`, `[ACTION REQUIRED FOR MANAGER]`) are preserved in the text.

## 5. Framework Modifications (框架修改声明)
- `scripts/orchestrator.py`
- `scripts/handoff_prompter.py`

---

## Appendix: Architecture Evolution Trace (架构演进与审查追踪)
> **[CRITICAL INSTRUCTION FOR PLANNER & CODER]** 
> IGNORING THIS SECTION IS MANDATORY. This section is strictly for historical tracking of the PM-Auditor-Boss discussion loop. Do NOT read, reference, or implement any logic from this appendix into the SDLC pipeline.

- **v5.0**: [Rejected] Instructed Manager to use `git clean`/`git restore` on dirty workspace.
- **Audit Rejection (v5.0)**: Poses catastrophic data loss risk to uncommitted human code.
- **v6.0 Revision Rationale**: Replaced destructive git commands with `git stash` to preserve state, introduced specific decoupled error prompts for boundary and lock issues.