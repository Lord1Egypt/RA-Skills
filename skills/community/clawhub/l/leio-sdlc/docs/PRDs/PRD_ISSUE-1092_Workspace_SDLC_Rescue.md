---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1092_Workspace_SDLC_Rescue

## 1. Context & Problem (业务背景与核心痛点)
The SDLC Orchestrator currently suffers from two fatal architectural defects:
1. **Global-Dir Path Disconnection**: Introduced recently, a strict fail-fast check demands a `--global-dir` to isolate the sandbox. If omitted or misconfigured, it crashes with `RuntimeError` or causes downstream agents (`spawn_planner.py`) to write to inaccessible paths, silently breaking the pipeline.
2. **Ghost Commit Vulnerability**: The `coder_playbook.md` allows the Coder to bypass `git commit` by creating a `.coder_state.json` file with `{"dirty_acknowledged": true}`. The Reviewer is deceived by the staged files in `git diff --cached`, approves the PR, and the Orchestrator's `git reset --hard HEAD` cleans the uncommitted files, resulting in a merged empty branch.

## 2. Requirements & User Stories (需求定义)
- **Path Resilience**: If `--global-dir` is not provided or is empty, the Orchestrator and all sub-agents (`spawn_planner.py`, `spawn_coder.py`, etc.) must smoothly fallback to using `.sdlc_runs/` inside the local `workdir`.
- **Ghost Commit Prevention**: The Orchestrator MUST strictly block the Coder from progressing to Review if `git status` shows any uncommitted tracked or untracked changes.
- **Preflight Enforcer**: The Orchestrator MUST run `preflight.sh` (if it exists) after verifying the Git status is clean. If preflight fails, the Coder is bounced back.
- **Dual-Track Yellow Path**: The Orchestrator must track system-level failures (Git dirty, Preflight failed) using an `orch_yellow_counter`, strictly decoupled from the Reviewer's `review_yellow_counter`. Both counters trigger Red Path (PR Slicing) if they reach 3 consecutive failures, but they must reset independently upon success.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
> **[Instruction to Main Agent/Architect]**
1. **Global-Dir Fix**: In `orchestrator.py` and `spawn_planner.py`, remove the `raise RuntimeError` for missing global-dir. Set `global_dir = workdir` (or `sdlc_root` locally) if no external global path is defined.
2. **Prompts & Playbook Cleanup**: Remove all references to `.coder_state.json` and `dirty_acknowledged` from `.gitignore`, `coder_playbook.md`, and `prompts.json`.
3. **Orchestrator FSM Upgrade (State 3 -> State 4)**:
   - After the Coder process exits, the Orchestrator checks `git status --porcelain`.
   - If dirty: Increment `orch_yellow_counter`. Spawn Coder again with `coder_system_alert` prompt containing the git status output.
   - If clean: Check if `./preflight.sh` exists in `workdir`.
   - If it exists, run `./preflight.sh`. If it exits with a non-zero code, increment `orch_yellow_counter`. Spawn Coder again with `coder_system_alert` containing the combined stdout/stderr of the preflight failure.
   - If clean AND preflight passes (or does not exist): Reset `orch_yellow_counter = 0`, transition to State 4 (Reviewer).
4. **Red Path Trigger**: If `orch_yellow_counter >= yellow_retry_limit`, set `state_5_trigger = True` (same as Reviewer's Red Path trigger) to force a Micro-Slicing loop.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Global-Dir Fallback**
  - **Given** no `--global-dir` argument or config is provided
  - **When** `orchestrator.py` and `spawn_planner.py` execute
  - **Then** they successfully create and read from `<workdir>/.sdlc_runs/` without throwing a `RuntimeError`.

- **Scenario 2: Orchestrator Dirty Status Interception**
  - **Given** the Coder modifies a file, runs `git add`, but does NOT `git commit`
  - **When** the Coder finishes its turn
  - **Then** the Orchestrator detects the dirty status, increments `orch_yellow_counter`, does NOT call the Reviewer, and bounces the alert back to the Coder.

- **Scenario 3: Orchestrator Preflight Interception**
  - **Given** the Git status is clean but `./preflight.sh` exits with code 1
  - **When** the Orchestrator verifies the Coder's work
  - **Then** the Orchestrator captures the output, increments `orch_yellow_counter`, does NOT call the Reviewer, and bounces the alert back to the Coder.

- **Scenario 4: Dual-Track Exhaustion (Red Path Trigger)**
  - **Given** the Coder repeatedly fails the Preflight check 3 times
  - **When** `orch_yellow_counter` reaches 3
  - **Then** the Orchestrator immediately triggers State 5 / Micro-slicing (Red Path) without ever engaging the Reviewer.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Unit/E2E Test**: Create `scripts/e2e/e2e_test_1092_dual_yellow_path.sh` containing a mocked workflow.
  - Assert that a mocked Coder failing `git status` triggers the `coder_system_alert` loop.
  - Assert that a mocked `preflight.sh` failing triggers the `coder_system_alert` loop.
  - Assert that 3 consecutive `orch_yellow_counter` increments correctly trigger the Red Path (Slicing) without incrementing the Reviewer's yellow counter.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/orchestrator.py` (Add FSM check logic, dual-counters, fix global-dir)
- `scripts/spawn_planner.py` (Fix global-dir pathing)
- `playbooks/coder_playbook.md` (Update exit criteria, remove dirty_acknowledged)
- `config/prompts.json` (Update `coder_system_alert`)
- `.gitignore` (Remove `.coder_state.json`)

## 7. Hardcoded Content (硬编码内容)
### Exact Text Replacements:

**`playbooks/coder_playbook.md` (Update the 'Workflow' section exactly to this):**
```markdown
## Workflow (TDD & Pre-Push)
1. **Explore the Workspace**: Read the PR Contract. Before writing any code, search the repository to understand where this feature belongs.
2. **TDD Loop**: Write Test (Red) -> Write Code (Green) -> Run tests or `./preflight.sh` (if available) until everything passes. You MUST leave the workspace in a fully working state.
3. **Commit**:
   - **CRITICAL HYGIENE:** You are fully responsible for your Git state. You MUST NOT use `git add .` under any circumstances.
   - Explicitly use `git add <file>` to stage ONLY the specific files you modified or created for this PR.
   - **MANDATORY EXIT CRITERIA:** You MUST meet all three conditions before finishing your turn:
     a. You have completed the PR task requirements.
     b. `./preflight.sh` (if it exists) runs completely green.
     c. Your Git status is absolutely clean. You MUST explicitly execute `git commit -m "feat/fix: <description>"` to commit your staged files. Uncommitted changes will be rejected by the Orchestrator.
4. **Report HASH**: Execute `LATEST_HASH=$(git rev-parse HEAD)` and report to the Manager: "Tests green, ready for review. Latest commit hash is `$LATEST_HASH`."
```

**`config/prompts.json` (Update the `coder_system_alert` key exactly to this):**
```json
"coder_system_alert": "\n--- SYSTEM ALERT ---\nSystem Preflight or Git Workspace Check Failed!\n{system_alert}\n\nYou MUST fix the errors above. If it's a Git dirty status, use explicit `git add <file>` and `git commit -m \"...\"` to commit your work. If it's a preflight error, fix the code and ensure tests pass. The Orchestrator will not let you proceed to Code Review until the workspace is fully committed and preflight is green."
```
