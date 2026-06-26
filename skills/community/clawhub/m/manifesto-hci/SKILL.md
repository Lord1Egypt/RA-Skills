---
name: manifesto-hci
description: Implement "Explicit State & Continuous Consensus" HCI pattern (v3.0). Combat information entropy, prevent intent drift, and maintain a shared source of truth (Manifesto) across long-term interactions using Tri-Track Architecture and Git-backed state management. Use when starting or managing a project (coding, creative writing, complex planning) that requires high reliability and zero-drift execution. Triggers on phrases like "start project", "manage state", "explicit consensus", "manifesto", "/manifesto start", or when a `project_id` is provided.
---

# Manifesto HCI - Explicit State & Continuous Consensus (v3.0)

This skill enforces a rigorous state management and consensus-building workflow using Git-backed physical decoupling and asynchronous auditing.

## Core Interaction Logic

You MUST follow the "Tri-Track Architecture" and "Execution Hooks" defined in [specification.md](references/specification.md).

### 1. User Lifecycle Control (Slash Commands)
- **`/manifesto start [project_id]`**:
  - Run `python3 scripts/core.py start <project_id>`.
  - Perform `git init` and first `git commit` silently.
  - Output: `[System: Manifesto 已挂载。后台 Diff 守护进程已就绪，当前分支: master。]`
- **`/manifesto pause`**:
  - Pause the Diff Sub-Agent. Stop Manifesto updates.
  - Output: `[System: Manifesto 暂停更新。进入自由发散模式。]`
- **`/manifesto stop`**:
  - Final `git commit` and unmount.
  - Output: `[System: Manifesto 已解绑。共识状态已安全固化至本地硬盘。]`

### 2. Physical Decoupling (Tri-Track)
- All project data is stored in `projects/prj_[project_id]/`.
- **Track 1 (Raw Log)**: Append-only JSONL in `logs/`.
- **Track 2 (The State)**: YAML + Markdown Manifesto in `state/`. **Single Source of Truth.**
- **Track 3 (Working Memory)**: `workspace/` and LLM context.

### 3. Main Agent Protocol (Foreground)
Every foreground response MUST follow this rule:
- **Pre-hook (Intent Sync)**: Every turn starts with `[意图同步: -m "Short summary"]`.
- **Constraint**: The Main Agent MUST NOT output `[ACK]`, `[CONFLICT]`, or `[共识更新]` in its own text. It only handles the user's task.

### 4. Background Auditing (Diff Sub-Agent & Post-hook)
- On turn completion, a zero-temperature (T=0) Sub-Agent must audit history asynchronously using the [Diff Agent Prompt](references/diff_agent_prompt.md).
- **Stateful Write**: Update Manifesto following the [Manifesto Template](references/manifesto_template.md) structure and run `git commit`.
- **Ephemeral/Noise**: Discard.
- **Socket Push (Out-of-Band)**: The Sub-Agent pushes a *separate, standalone* UI message bubble:
  - `[共识更新] 已捕获新事实: ...`
  - `[逻辑冲突] 审计警报: ...`
  - `[ACK] 流程对齐中，无新共识产生。`

### 5. Automated History Logging
- After generating a response, log both the user input and your response.
- Execute: `python3 scripts/core.py log <project_id> user "<user_message>"` and `python3 scripts/core.py log <project_id> assistant "<assistant_response>"`.

## Manifesto Organization
Follow Topic-based Classification in [specification.md](references/specification.md):
1. **Core Anchors**
2. **Side-talk / Low Relevance**
3. **Multi-topic Parallelism**

## Constraints
- **Explicit Commits**: All changes must be visible via `commit -m`.
- **Zero Data Loss**: Never discard core arguments.
- **Physics Separation**: Manifesto vs History per project.
- **Agent Decoupling**: Main Agent (Interaction) vs Sub-Agent (Auditing).
