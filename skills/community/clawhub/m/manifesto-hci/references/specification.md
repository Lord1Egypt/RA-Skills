# Manifesto HCI - System Architecture & Protocol (v3.0)

## Core Intent
- **Explicit State & Continuous Consensus:** To combat information entropy and ensure zero-drift AI execution intent.
- **Physical Decoupling:** Strictly follow the Tri-Track Architecture.

## Tri-Track Architecture (Physics Isolation)
All files are compartmentalized under `projects/prj_[project_id]/`:

1. **Track 1 | Raw Log:** `logs/history_[project_id].jsonl`
   - Append-only database. Lossless record of original context and divergent thinking.
2. **Track 2 | The State (Manifesto):** `state/manifesto_[project_id].md`
   - Single Source of Truth (SSOT). YAML + Markdown.
   - Contains: Conditions, constraints, goals, and validation logic.
3. **Track 3 | Working Memory:** `workspace/` directory and current context window.
   - Temporary sandbox. Core findings are extracted to Track 2.

## User Lifecycle Control (Slash Commands)
- `/manifesto start [project_id]`
  - Init physical project directory.
  - Silent `git init` and first commit: `git commit -m "Init: 系统冷启动，建立初始共识"`.
  - Output: `[System: Manifesto 已挂载。后台 Diff 守护进程已就绪，当前分支: master。]`
- `/manifesto pause`
  - Unmount hooks. Stop implicit updates.
  - Output: `[System: Manifesto 暂停更新。进入自由发散模式。]`
- `/manifesto stop`
  - Unmount and final `git commit`.
  - Output: `[System: Manifesto 已解绑。共识状态已安全固化至本地硬盘。]`

## Async Lifecycle & Execution Hooks
### 1. Main Agent (Foreground)
- **Pre-hook:** Scan history for `Conflict` or `ACK`.
- **Response:** TTFT-focused. Directly execute user instructions.
- **Conflict Handling:** If a `Conflict` exists, force user to adjudicate before any new task.

### 2. Diff Sub-Agent (Background/Async)
- Triggered on `on_turn_completed`.
- **Function:** Zero-temperature (T=0) objective auditing.
- **Logic:**
  - **Fact Extraction:** Distinguish between *Stateful* changes (Core Fact) and *Ephemeral* tasks (Noise).
  - **Commit:** For Stateful changes, update `manifesto_[project_id].md` and run `git commit`.
  - **Conflict Detection:** If New Intent vs Core Anchors, push `[逻辑冲突]` system message.

### 3. Socket Push (Post-hook Feedback)
- **[共识更新]:** `已捕获新事实: ${commit_msg}`.
- **[逻辑冲突]:** `审计警报: 新意图与核心锚点【${old_fact}】发生冲突`.
- **[ACK]:** `流程对齐中，无新共识产生。提示：当前路径高度明确。如需进行非共识发散可输入 /manifesto pause 挂起或 /manifesto stop 结束`。

## Formatting Standards & UI Feedback
- **Main Agent (Foreground Text):** MUST ONLY start with `[意图同步: -m "Summary"]`. It does NOT output ACK/Conflict tags.
- **Diff Sub-Agent (Standalone Socket Push):**
  - **Update:** `[共识更新]: 已捕获新事实: ${commit_msg}`.
  - **Conflict:** `[逻辑冲突]: 审计警报: 新意图与核心锚点【${old_fact}】发生冲突`.
  - **ACK:** `[ACK]: 流程对齐中，无新共识产生。提示：当前路径高度明确。如需进行非共识发散可输入 /manifesto pause 挂起或 /manifesto stop 结束`。

## Manifesto Organization (Topic-based)
1. **Core Anchors:** Main project pillars (High Priority).
2. **Side-talk / Low Relevance:** Isolated secondary discussions (Bottom of file).
3. **Multi-topic Parallelism:** Parallel `# Topic` modules for major shifts.
