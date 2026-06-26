---
name: multi-step-workflow
version: 4.4.5
description: "Professional SOP with Machine-Gated Planning, Native-CLI Config, and Audit-Hardened Private Sandbox Storage."
homepage: "https://github.com/chyern/Agent-Skills"
repository: "https://github.com/chyern/Agent-Skills.git"
requires:
  bins:
    - node
    - openclaw
---
# Standard Task SOP (High-Trust Edition)

Follow this adaptive workflow to ensure task reliability and professional-grade execution.

## Phase 0: Triage & Analyze
1. **Analyze**: Assess task scope within the workspace.
2. **Threshold Check**:
   - **Simple Path**: < 3 steps. Direct execution.
   - **Standard Path**: >= 3 steps. Follow Path B.

---

## [Path A] Simple Path
1. **Confirm** intent -> **Execute** -> **Report**. DONE.

---

## [Path B] Standard Path (Machine-Gated)
For complex engineering, act as a **Manager** and ensure all workers are **Sandboxed**.

### Phase 1: Confirm
Summarize your understanding and align on the objective.

### Phase 2: Create Plan
1. **Decompose**: Register steps in `task-tracker.js`.
2. **Parallelize**: Identify independent sub-tasks for delegation.
3. **Draft Plan**: Create `implementation_plan.md`. Be explicit about worker scope.

### Phase 3: Obtain Approval (Planning Mode - THE GATE)
> [!IMPORTANT]
> **YOU ARE IN PLANNING MODE.**
> 1. Present plan. **MUST YIELD** and wait for user approval.
> 2. **GATING**: Once approved, YOU MUST RUN: `node scripts/approve.js "<task>"`
> 3. **DO NOT** modify any files until this symbolic gate script is run.

### Phase 4: Execute (Autonomous Loop)
> [!TIP]
> **YOU ARE IN AUTONOMOUS LOOP.**
> 1. **Sequential by Default**: Execute the plan steps sequentially yourself.
> 2. **Configurable Sub-agents**: BEFORE parallelizing work:
>    - **Check Configuration**: Run `openclaw config get skills.entries.multi-step-workflow.config`.
>    - **Initialization**: If config is empty or errors, run `openclaw config set skills.entries.multi-step-workflow.config '{"useSubAgents": false, "maxSubAgents": 3, "useSnapshots": false}' --strict-json`.
>    - **Modify Configuration** (if needed): Run `openclaw config set skills.entries.multi-step-workflow.config.<key> <value> --strict-json`.
>    - **Defaults** (if missing): `useSubAgents: false`, `maxSubAgents: 3`.
>    - If `useSubAgents` is `false`, **DO NOT use spawn**.
>    - If `useSubAgents` is `true`, you may use `spawn` (limit: `maxSubAgents`).
>    - **RESTRICTION**: Do NOT use `spawn` for arbitrary OS commands or network scanning.
> 3. **Progress**: Mark steps `done`. Report each step and IMMEDIATELY move to the next.
> 4. **Context Preservation (Anti-Amnesia)**: 
>    - **Check `useSnapshots`**: Run `openclaw config get skills.entries.multi-step-workflow.config` (Default: `false`).
>    - **Execute** (Only if `useSnapshots` is `true`): If you extract a crucial finding OR if the task is taking many turns:
>      `node scripts/context-snapshot.js save "<task>" "<findings>" "<pending>" ["<last_error_log>"]`
>    - **Self-Healing**: If you suspect context compaction, run `node scripts/context-snapshot.js load` to recover.

### Phase 5: Validate
Verify results (tests, results). If a worker fails, go back to Phase 4.

### Phase 6: Review
Evaluate the task and present a final Review summary directly in the chat. Highlight what was done well, what was problematic, and any critical lessons learned.
**DO NOT auto-write to any memory files.** 
Simply display your review and ask the user if they would like this experience saved to their long-term memory.

### Phase 7: Complete
Task finished. Clean up state if necessary.
