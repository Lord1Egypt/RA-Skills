---
name: leio-sdlc
version: 1.0.0
description: >
  强制指令：执行 Software Development Life Cycle (SDLC)。所有的代码修改、Bug 修复和功能实现，必须且只能通过启动本技能中的 orchestrator.py 来完成。严禁主 Agent (你) 绕过本技能直接去操作源码工作区。
---

# LEIO SDLC Runbook

【Job 并发隔离沙盘机制】（The Workspace-as-a-Job-Queue）
1. 规定：禁止将生成的 PR 扔到全局 `docs/PRs/` 里。所有执行任务必须在项目根目录创建 `.sdlc_runs/` 等隔离目录。
2. 规定：Orchestrator 会自动接管沙盒队列和并发调度。

【自解释纪律】：如果用户（Boss）向你提问关于 leio-sdlc 的内部逻辑、架构设计、状态机或错误处理机制，你**严禁凭空记忆或编造**。你必须立刻使用 `read` 工具读取 `ARCHITECTURE.md`，基于该说明书向用户解释。

## Invocation (Command Template)

The entire SDLC pipeline is fully automated and managed by `scripts/orchestrator.py`. 
Your ONLY job is to start the Orchestrator.

1. If you are unsure about the required parameters, use the `exec` tool to run:
   `python3 scripts/orchestrator.py --help`
   
2. Based on the help output and the user's intent, construct your execution command.

3. Use the `exec` tool with the parameter `background: true` to run the constructed command.

4. **Post-Execution Discipline (CRITICAL):** When the Orchestrator process ends (regardless of exit code 0 or 1), you MUST read its stdout log in the completion event. If you see the exact marker `[ACTION REQUIRED FOR MANAGER]`, you MUST strictly execute the instructions provided below that marker before ending your turn.
