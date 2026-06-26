---
Affected_Projects: [leio-sdlc, pm-skill]
Context_Workdir: /root/.openclaw/workspace/projects/leio-sdlc
---

# PRD: ISSUE-1081 Refine Actionable JIT Prompts and Execution Guardrails

## 1. Context & Problem (业务背景与核心痛点)
1. **Un-actionable JIT Prompts**: Currently, when the SDLC pipeline fails (e.g., parameter validation, invalid boundaries), the JIT prompts returned to the Agent are vague (e.g., "Correct your CLI command/parameters and retry."). This "riddle-like" feedback causes the Agent to hallucinate or guess the solution, wasting tokens and leading to infinite loops.
2. **Leaky Workspace Guardrails**: Previous efforts introduced a "Workspace Execution Guardrail" inside `orchestrator.py` to prevent the Agent from executing the pipeline directly from the target workspace (it must be executed from the installed `~/.openclaw/skills/...` directory). However, this guardrail was *only* added to `orchestrator.py`. Peripheral entry points like `spawn_auditor.py` and `pm-skill/scripts/init_prd.py` lack this protection, allowing the Agent to illegally bypass the runtime boundary.
3. **Auditor Channel Handshake & Formatting (ISSUE-1084)**: `spawn_auditor.py` does not strictly enforce an initial channel handshake like `orchestrator.py` does, and its error messages for missing channels are not standardized with the actionable JIT prompts format. Furthermore, its output formatting to the channel lacks consistency with the rest of the SDLC notifications.

## 2. Requirements & User Stories (需求定义)
1. **Actionable Exits**: Every `handoff_` string in `config/prompts.json` must be rewritten. They must explicitly state the problem AND provide the exact actionable command or clear next step the Agent should take.
2. **Universal Execution Boundary**: The workspace execution guardrail must be applied to `spawn_auditor.py` and `pm-skill/scripts/init_prd.py` to physically block execution from `/root/.openclaw/workspace/projects/*` unless bypassed via an explicit flag.
3. **No Mute Failures**: If the boundary check fails, it must print an *actionable* error message explaining exactly where to run the command from.
4. **Auditor Ignition Guardrail (ISSUE-1084)**: `spawn_auditor.py` MUST explicitly enforce the `--channel` parameter as required. Before launching the Auditor agent, it must perform a mandatory API handshake to the provided channel (similar to the orchestrator). If the handshake fails, it must exit immediately with an actionable JIT prompt.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- **`config/prompts.json`**: Update strings like `handoff_startup_validation_failed`, `handoff_missing_channel`, etc. Include explicit instructions. For example, instead of "Missing channel parameter", output "Missing channel parameter. You must append a valid OpenClaw channel string (e.g., `--channel slack:C0AML8LN91R`) to your command."
- **`scripts/spawn_auditor.py` & `skills/pm-skill/scripts/init_prd.py`**: Inject the standard `__file__` workspace path check at the top of the scripts (before executing core logic). If `__file__` contains `/root/.openclaw/workspace/projects/` and `--enable-exec-from-workspace` is not provided, immediately `sys.exit(1)` and print the explicit handoff prompt. Add the `--enable-exec-from-workspace` argument to `argparse` in both scripts to allow bypassing.
- **Auditor Handshake & Config Update**: In `spawn_auditor.py`, change `--channel` to `required=True` (or handle it with a strict actionable error if missing). Implement the `openclaw message send` subprocess handshake logic immediately after argument parsing. Update `config/prompts.json` to include a new `handoff_invalid_channel` message.

## 3.1 Blast Radius & Rollback Strategy (爆炸半径与回滚计划)
- **Blast Radius**: Modifying the English suggestions in `config/prompts.json` does not affect any existing state machines or logic loops. The execution guardrail added to `spawn_auditor.py` and `init_prd.py` will block illegitimate executions from the workspace. Enforcing the channel handshake in Auditor might break existing wrapper scripts that call it without a valid channel, but this is an intended security enforcement.
- **Rollback / Escape Hatch**: To prevent a complete system lock-out due to symlink/mount point drift in `__file__` matching, the new execution guardrails will explicitly support the existing `--enable-exec-from-workspace` bypass parameter. If a false positive blocks execution in production, the user/manager can append this flag to force-run the script as a manual override. For the channel handshake, if the OpenClaw API is down, users must fix the network or bypass the script entirely.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Actionable JIT Prompts in Logs**
  - **Given** The orchestrator is invoked without a `--channel`
  - **When** The validation fails
  - **Then** The printed JIT prompt explicitly contains an actionable command suggestion (e.g., "You must append `--channel ...`").
- **Scenario 2: Guardrail blocks execution in workspace**
  - **Given** The user/agent is in `/root/.openclaw/workspace/projects/leio-sdlc`
  - **When** They attempt to run `python3 scripts/spawn_auditor.py ...`
  - **Then** The script instantly exits with `code 1` and prints a "Security Violation" error.
- **Scenario 3: Guardrail allows execution from installed skill directory**
  - **Given** The user runs `python3 /root/.openclaw/skills/leio-sdlc/scripts/spawn_auditor.py ...`
  - **When** The script is invoked
  - **Then** It proceeds normally without security violations.
- **Scenario 4: Auditor Handshake Rejects Invalid Channel**
  - **Given** Auditor is called with `--channel invalid:format`
  - **When** The script attempts the handshake
  - **Then** It must immediately exit with `code 1` and print the actionable `[FATAL] Invalid notification channel format...` prompt.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Unit/Integration Testing**: Add/update unit tests for `spawn_auditor.py` and `init_prd.py` simulating the `__file__` path to ensure the `sys.exit(1)` behavior triggers correctly. 
- **Quality Goal**: Ensure 100% boundary coverage for all entrypoint scripts.

## 6. Framework Modifications (框架防篡改声明)
- `/root/.openclaw/workspace/projects/leio-sdlc/config/prompts.json`
- `/root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_auditor.py`
- `/root/.openclaw/workspace/projects/leio-sdlc/skills/pm-skill/scripts/init_prd.py`

---

## 7. HARDCODED CONTENT (CODER MUST COPY EXACTLY)

> **[CRITICAL INSTRUCTION TO CODER - ANTI-PITFALL GUIDE]**
> Before this fix is applied, YOU are currently vulnerable to the CWD drift bug. You MUST manually prepend the absolute workdir path (i.e., `/root/.openclaw/workspace/projects/leio-sdlc/`) to all relative file paths when using your `read`, `edit`, or `write` tools during this specific task. 
> To be absolutely clear, you will modify these specific files using these exact absolute paths:
> 1. `/root/.openclaw/workspace/projects/leio-sdlc/config/prompts.json`
> 2. `/root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_auditor.py`
> 3. `/root/.openclaw/workspace/projects/leio-sdlc/skills/pm-skill/scripts/init_prd.py`

**[REQUIRED EXACT STRINGS FOR config/prompts.json]**
You MUST replace the existing `handoff_` keys in `config/prompts.json` with the following EXACT strings to ensure they are actionable. DO NOT change the keys, only update the values:

```json
    "handoff_happy_path": "[SUCCESS_HANDOFF]\n[ACTION REQUIRED FOR MANAGER]\nThe pipeline has finished. You must now: 1. Update PRD status. 2. Close the Issue strictly using `python3 ~/.openclaw/skills/issue_tracker/scripts/issues.py update <ISSUE-ID> --status closed`. 3. Update STATE.md. 4. Wait and Report completion to the Boss.",
    "handoff_dirty_workspace": "[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nWorkspace is dirty. There are uncommitted files. NEVER blindly delete or commit them! You MUST use `git stash` to safely preserve the state, or abort and wait for human intervention.",
    "handoff_planner_failure": "[FATAL_PLANNER]\n[ACTION REQUIRED FOR MANAGER]\nPlanner failed. You MUST read planner logs in `.tmp/sdlc_logs/` and refine the PRD before retrying.",
    "handoff_git_checkout_error": "[FATAL_GIT]\n[ACTION REQUIRED FOR MANAGER]\nGit checkout failed. Workspace preserved. You MUST run: `python3 ~/.openclaw/skills/leio-sdlc/scripts/orchestrator.py --cleanup` to quarantine the branch.",
    "handoff_fatal_crash": "[FATAL_CRASH]\n[ACTION REQUIRED FOR MANAGER]\nOrchestrator crashed. Process groups reaped. Workspace preserved. You MUST read the traceback in logs and run: `python3 ~/.openclaw/skills/leio-sdlc/scripts/orchestrator.py --cleanup` to quarantine the branch.",
    "handoff_fatal_interrupt": "[FATAL_INTERRUPT]\n[ACTION REQUIRED FOR MANAGER]\nAborted via SIGINT/SIGTERM. Process groups reaped. Workspace preserved. No immediate action required unless retrying.",
    "handoff_missing_channel": "[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nMissing channel parameter. You MUST append a valid OpenClaw channel string (e.g., `--channel slack:CXXXXXX`) to your Orchestrator or Auditor command.",
    "handoff_invalid_channel": "[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nInvalid notification channel format or failed handshake. You MUST provide a valid OpenClaw channel string (e.g., `slack:CXXXXXX`) and ensure the gateway is running.",
    "handoff_dead_end": "[FATAL_ESCALATION]\n[ACTION REQUIRED FOR MANAGER]\nDead End reached. You MUST read `Review_Report.md` (located in the current job directory) and alert the Boss explicitly for instructions.",
    "handoff_startup_validation_failed": "[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nStartup validation failed (likely executing from the wrong directory). You MUST execute the script using its absolute installed path (e.g., `python3 ~/.openclaw/skills/leio-sdlc/scripts/orchestrator.py ...`) OR explicitly append the `--enable-exec-from-workspace` flag if testing locally.",
    "handoff_invalid_git_boundary": "[FATAL_STARTUP]\n[ACTION REQUIRED FOR MANAGER]\nInvalid Git boundary. You MUST `cd` to the root of a Git repository on the master/main branch before executing this pipeline.",
    "handoff_pipeline_locked": "[FATAL_LOCK]\n[ACTION REQUIRED FOR MANAGER]\nAnother SDLC pipeline is actively running in this workspace. You MUST wait for it to finish. DO NOT modify the workspace."
```
