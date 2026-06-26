# PRD-079: Universal Channel Notifications, Session Teardown Fix & Immutable PR Contracts

## 1. Problem Statement
1. The SDLC Orchestrator operates as a background process, forcing operators to poll logs for status. An automated, native push notification system is needed to broadcast progress to the originating chat channel (Slack, Discord, etc.) without human polling.
2. The current `teardown_coder_session` function attempts to call a non-existent CLI command `openclaw subagents kill`, causing errors.
3. The Orchestrator fails late in the process if the Git workspace is dirty at startup. A fail-fast mechanism is needed at startup.
4. The Orchestrator currently uses a "blind catch-all" `git add . && git commit` after the Coder finishes, polluting Git history with temporary files. 
5. The Orchestrator currently modifies the `PR_xxx.md` files to append context. This violates the core architectural rule: **PR files are immutable contracts.**
6. The state updater (`set_pr_status`) uses a dangerous `git add .` which risks committing unacknowledged dirty files.
7. Subagent prompt templates and playbooks blindly instruct agents to use `git add .`, which contradicts the new semantic commit rules.

## 2. Objective & Solution Synthesis
1. **Universal Channel Notifications**: Broadcast state transitions to the external channel (Slack, etc.) using `openclaw message send`.
2. **Session Teardown Fix**: Remove the invalid `subagents kill` CLI call.
3. **Fail-Fast Interceptor**: Detect a dirty Git workspace at startup and abort execution immediately.
4. **JSON-Based State Handoff**: Introduce a `.coder_state.json` file for the Coder to pass metadata.
5. **Direct Session Prompting**: The Orchestrator must pass Review Feedback and Alerts directly into the *existing* Coder session.
6. **Pre-Merge Final Cleanup**: Execute `git reset --hard HEAD && git clean -fd` before checkout master. 否则所有 dirty 文件都会被彻底删除.
7. **Precise State Commits**: Restrict the Orchestrator's state management commits to strictly target the exact PR file, never using `git add .`.
8. **Prompt Hygiene**: Remove all `git add .` instructions from all `spawn_*.py` files and the Coder playbook.

## 3. Scope Locking
**Target Project Directory:** `/root/.openclaw/workspace/projects/leio-sdlc`

## 4. Technical Requirements

### 4.1 Universal Channel Notifications
- **File**: `scripts/orchestrator.py`
- **Parameters**: Add `--notify-channel` and `--notify-target` to the CLI arguments.
- **Function**: Implement `notify_channel(args, msg)` using `subprocess.run(["openclaw", "message", "send", "--channel", args.notify_channel, "--target", args.notify_target, "-m", f"🤖 [SDLC Engine] {msg}"])`. Do not fail if the command errors (use `check=False`).
- **Integration Points**:
  1. *Ignition*: "🚀 引擎已启动，正在分析 PRD: {prd_name}" (State 0/1)
  2. *PR Switch*: "⏳ 正在处理 PR: {current_pr}" (State 2/3)
  3. *Dead End*: "🚨 警告：Coder 已经被退回 5 次且重置无效，任务进入死信队列，请人工介入！" (State 5 Arbitrator failure)
  4. *Success*: "✅ 恭喜 Boss！所有 PR 均已成功合并入 master，流水线安全退出。" (End of script)

### 4.2 Bug Fix: Session Teardown
- **Action**: In `teardown_coder_session`, remove the `subprocess.run(["openclaw", "subagents", ...])` block.

### 4.3 Dirty Workspace Interceptor (Fail-Fast)
- **Action**: Add an early check in `main()`. Execute `git status --porcelain`. If output exists, log `[FATAL] Dirty Git Workspace detected! ...` and exit.

### 4.4 Immutable PR Contracts & Precise Status Commits
- **Action 1**: Delete the `append_to_pr` function. 
- **Action 2**: In `set_pr_status`, change `subprocess.run(["git", "add", "."])` to `subprocess.run(["git", "add", pr_file])`.

### 4.5 Semantic Git Status Enforcement (JSON State & Direct Prompting)
- **Action 1**: Delete `force_commit_untracked_changes`.
- **Action 2**: After the Coder session (State 3), run `git status --porcelain`. 
  - If clean: proceed to State 4.
  - If dirty: read `.coder_state.json`.
    - If `{"dirty_acknowledged": true}` exists: proceed to State 4.
    - If not: call `spawn_coder.py` with `--system-alert "<git status output>"`. 
- **Action 3**: Update `spawn_coder.py`. When receiving `--system-alert` or `--feedback-file`, inject a prompt directly into the *existing* Coder session.
  - **Prompt Template**: `[SYSTEM_ALERT] Uncommitted changes detected by Orchestrator:\n<git status output>\nYou must either 1) commit your intended changes, 2) update .gitignore to ignore test artifacts, OR 3) create a file named '.coder_state.json' with the exact content '{"dirty_acknowledged": true}' if you confirm the remaining untracked files are entirely irrelevant to your work. 否则所有 dirty 文件都会被彻底删除 (Otherwise all dirty files will be completely deleted in the final cleanup phase).`
- **Action 4**: Update `orchestrator.py` State 4 rejection loop. Pass Review Report path to `spawn_coder.py` (`--feedback-file`) to prompt existing Coder.

### 4.6 Fix Rogue Prompts (Remove Blind Commits)
- **Action 1**: In `scripts/spawn_planner.py`, `scripts/spawn_coder.py`, `scripts/spawn_reviewer.py`, and `scripts/spawn_arbitrator.py`, locate and REMOVE the string `Use 'git add .' to stage changes safely within your directory.` from all prompt templates.
- **Action 2**: In `playbooks/coder_playbook.md`, remove the old `git add . && git commit` instruction. Add explicit rules: "You are fully responsible for your Git state. Explicitly `git add <file>` only the files you intend to commit. If your tests generate temporary artifacts, you MUST either add them to `.gitignore` or create a file named `.coder_state.json` containing `{\"dirty_acknowledged\": true}`. The Orchestrator will reject your work if untracked files are left unacknowledged."

### 4.7 Pre-Merge Final Cleanup
- **Action**: In State 6 (Merge code) BEFORE executing `git checkout master`, run `git reset --hard HEAD` and `git clean -fd` within the branch.

## 5. Autonomous Test Strategy & TDD Guardrail
- **Guardrail**: The implementation and its failing test MUST be delivered in the same PR contract.
- **Strategy**: Unit and integration testing with mocks (`tests/`).

### 4.8 Planner Git Hygiene Loop
- **File**: `scripts/orchestrator.py`
- **Action**: Currently, State 0 has a primitive "Solidification" commit. Replace it with a robust `git status` check similar to the Coder's semantic enforcement.
- **Logic**: After `spawn_planner.py` finishes, the Orchestrator must check `git status --porcelain`.
  - If new PR files are untracked: 
    - The Orchestrator MUST re-spawn the Planner with a `--system-alert` instructing it to use the `create_pr_contract.py` tool correctly or manually `git add` its files.
    - Alternatively, since Planner is simpler, the Orchestrator should at least ensure that the newly created PR files in `docs/PRs/PRD_NAME/` are committed.
- **Decision**: To maintain symmetry with the Coder, the Planner should also be responsible for its own commits. Update `playbooks/planner_playbook.md` to require the Planner to commit its generated PR contracts. If it fails to do so, Orchestrator re-spawns it until the PR directory is clean.

### 4.8 Deterministic PR Contract Staging (Planner Fix)
- **File**: `scripts/create_pr_contract.py`
- **Action**: Currently, the Planner generates PR contract files using this script, but leaves them untracked. Update the script to automatically stage the generated files.
- **Function**: Import `subprocess` if not already imported. Immediately after successfully writing the new PR file to disk, execute `subprocess.run(["git", "add", file_path], check=True)`.
- **Reasoning**: This guarantees that every generated PR contract is precisely and deterministically staged in Git. This protects the PR files from being annihilated by the Pre-Merge Final Cleanup (`git clean -fd`) without requiring the Planner LLM to understand or execute Git commands.
