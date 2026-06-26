---
Affected_Projects: [leio-sdlc]
Context_Workdir: /root/.openclaw/workspace/projects/leio-sdlc
---

# PRD: ISSUE-1065, 1082 & 1086 Formalize PRD Commit, Template Validation, and Auditor Architecture Downgrade

## 1. Context & Problem (业务背景与核心痛点)
- **ISSUE-1082**: Manager (qbot) frequently uses `sdlc.override=true` to manually commit PRDs, bypassing the SDLC intent. Orchestrator's current `auto-commit` logic creates a "State Contamination" risk: if a pipeline fails and the human/agent resets the branch to recover, the uncommitted/auto-committed PRD content is lost.
- **ISSUE-1065**: Auditors occasionally approve "feral" (non-standard) PRDs that lack structure. Furthermore, ambiguous PRDs often force Coders to hallucinate strings (e.g., error messages, UI text), leading to inconsistent behavior.
- **ISSUE-1086 (Auditor Reward Hacking Vulnerability)**: The Auditor logic is currently split between an SDLC guardrail script (`spawn_auditor.py`) and an independent AgentSkill (`leio-auditor/prd_auditor.py`). Because `prd_auditor.py` can be invoked directly without `--channel` handshakes or execution constraints, AI Managers (Agents) tend to bypass the `spawn_auditor.py` guardrails entirely (Reward Hacking) when faced with valid pipeline blocks, rendering the Anti-YOLO execution constraints completely useless.

## 2. Requirements & User Stories (需求定义)
- **Decoupled PRD & State Commit**: 
    - Remove auto-commit logic from `orchestrator.py`. Orchestrator should only READ committed PRDs.
    - Introduce `scripts/commit_state.py` as the **sole authorized gateway** for moving a PRD from "draft" to "baseline", and for committing post-SDLC `STATE.md` updates.
    - Update `pm-skill/SKILL.md` to mandate the use of `commit_state.py`.
- **Strict Template Validation (Auditor Upgrade)**:
    - Auditor must verify the PRD follows the standard `PRD.md.template` headers.
    - Auditor must enforce the **"Anti-Hallucination String Policy"**: Any specific text/messages mentioned in the requirements MUST be explicitly listed in a `## 7. Hardcoded Content` section.
- **Burn the Boats (Visual Only)**: Modify the pre-commit hook to remove the `sdlc.override` echo hint from the console output to enforce behavioral compliance.
- **Architectural Downgrade (ISSUE-1086)**: Merge the core LLM execution logic of `prd_auditor.py` completely into `spawn_auditor.py`. Delete the standalone `leio-auditor` AgentSkill to enforce a single, guarded entry point for PRD auditing.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- **New Script: `scripts/commit_state.py`**:
    - Accepts file paths as arguments (e.g., `--files STATE.md docs/PRDs/PRD_XXX.md`).
    - Validates that the files are purely administrative (e.g., matching `STATE.md` or `docs/PRDs/*.md`). Reject if trying to commit source code.
    - Executes `git -c sdlc.runtime=1 commit -m "chore(state): update manager state"` safely.
- **`orchestrator.py` Guardrail**:
    - Modify `validate_prd_is_committed` to simply check `git ls-files --error-unmatch` and `git status --porcelain`. If dirty/untracked, fail-fast with a JIT prompt pointing to `commit_state.py`.
- **`playbooks/auditor_playbook.md`**:
    - Add a "Template Integrity" check item.
    - Add a "String Determinism" check item.
- **Auditor Architecture Downgrade**:
    - Refactor `spawn_auditor.py`: Extract the Gemini API call logic from `leio-auditor/scripts/prd_auditor.py` and implement it natively inside `spawn_auditor.py` as a Python function, removing the fragile `subprocess.run` IPC.
    - Delete the `skills/leio-auditor` directory entirely from the `leio-sdlc` project to kill the bypass vector.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1:** Fails fast when PRD is uncommitted
  - **Given** a dirty PRD file in the workspace
  - **When** running `orchestrator.py`
  - **Then** it must exit with `[FATAL]` and provide the command for `commit_state.py`
- **Scenario 2:** Auditor rejects unlisted strings
  - **Given** a PRD missing the `## 7. Hardcoded Content` section
  - **When** running `spawn_auditor.py`
  - **Then** it must return `REJECTED`
- **Scenario 3:** Anti-YOLO Auditor Bypass Eliminated
  - **Given** an Agent attempts to invoke `prd_auditor.py`
  - **When** executing the command
  - **Then** the system must return `File not found` because the standalone script no longer exists.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **E2E Trace**:
    1. Create a feral PRD -> `spawn_auditor.py` Rejects.
    2. Verify `leio-auditor/scripts/prd_auditor.py` no longer exists.
    3. Create a standard PRD but don't commit -> Orchestrator Rejects.
    4. Run `commit_state.py` -> Success.
    5. Run Orchestrator -> Success.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/orchestrator.py`
- `.sdlc_hooks/pre-commit`
- `playbooks/auditor_playbook.md`
- `skills/pm-skill/SKILL.md`
- `scripts/spawn_auditor.py`
- `skills/leio-auditor/` (DELETED)
- New: `scripts/commit_state.py`

## 7. Hardcoded Content (硬编码内容)
- **`commit_state_prompt` (For Orchestrator)**: 
  `"[FATAL] Workspace contains uncommitted state files. You MUST baseline your PRD and state using the official gateway: python3 ~/.openclaw/skills/leio-sdlc/scripts/commit_state.py --files <path>"`
- **`commit_state_invalid_file_error` (For commit_state.py)**:
  `"[FATAL] commit_state.py can only be used for state and PRD files. Source code changes must go through the SDLC pipeline."`
- **`commit_state_git_lock_error` (For commit_state.py)**:
  `"[FATAL] Git index is locked. Please wait or remove .git/index.lock if a previous process crashed."`
- **`auditor_template_error` (For Auditor Playbook/Prompt)**: 
  `"REJECTED: PRD structure does not match the mandatory template. Missing sections: {sections}."`
- **`auditor_string_hallucination_error` (For Auditor Playbook/Prompt)**: 
  `"REJECTED: The PRD mentions specific text/messages but fails to list them in 'Section 7. Hardcoded Content'. Ensure Coder has no room for hallucination."`

### Exact Text Replacements:
- **For `.sdlc_hooks/pre-commit` (Replace the entire Emergency Override echo block)**:
```bash
echo "==============================================================="
echo "❌ GIT COMMIT REJECTED ON PROTECTED BRANCH: $CURRENT_BRANCH"
echo "==============================================================="
echo "Role Awakening: As a Manager, you should NEVER commit directly!"
echo "Please use the official gateway to baseline your state/PRD before pipeline ignition:"
echo "python3 ~/.openclaw/skills/leio-sdlc/scripts/commit_state.py --files <path_to_files>"
echo "==============================================================="
```

- **For `skills/pm-skill/SKILL.md` (Add to End of Task & Circuit Breaker)**:
```text
4. **Baseline the PRD**: You MUST NOT use manual `git commit` or `sdlc.override`. To save the PRD baseline, you MUST use the official gateway: `python3 ~/.openclaw/skills/leio-sdlc/scripts/commit_state.py --files <Absolute_Path_To_PRD>`
```

- **For `playbooks/auditor_playbook.md` (Add to Evaluation Criteria)**:
```markdown
- **Template Integrity**: Verify the PRD contains all mandatory sections matching `PRD.md.template`. If structural headers are missing, REJECT immediately.
- **String Determinism (Anti-Hallucination Policy)**: If the PRD implies specific output strings (notifications, errors, CLI outputs), verify they are explicitly listed in `Section 7: Hardcoded Content`. If strings are left to 'Coder discretion' without explicit PM approval, REJECT immediately.
```

## 8. Rollback Plan (回滚计划)
- **Break-Glass Procedure**: If `commit_state.py` contains a defect that causes a commit deadlock (preventing any pipeline execution or fixes), the Boss (or human operator) can use the undocumented emergency override: `git -c sdlc.override=true commit -m "emergency fix"` to bypass the pre-commit hook and repair the defect.
- **Hook Removal**: Alternatively, the operator can manually delete or modify `.sdlc_hooks/pre-commit` to restore standard git behavior.
- **commit_state.py Edge Cases**: If `commit_state.py` fails due to an invalid path or a locked git index (`.git/index.lock`), it must catch the exception, print an actionable failure message, and exit with code 1 without corrupting the repository state.

## Appendix: Architecture Evolution Trace (架构演进与审查追踪)
- **v1.0**: Initial draft to solve ISSUE-1065 & 1082.
- **Audit Rejection (v1.0)**: Template integrity failure (missing Frontmatter, misaligned headers).
- **v1.1 Revision**: Corrected headers to match `PRD.md.template` exactly and added the Frontmatter with `Context_Workdir`.