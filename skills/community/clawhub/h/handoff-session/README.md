# handoff-session

[English](#english) | [中文](#中文)

---

## English

A cross-session handoff protocol for Claude Code and other AI agents.

`handoff` is not a summarization tool. It's a protocol for **freezing your work context, packaging it, and resuming execution** — in any session, any agent, any device.

### The problem

When you use AI agents for long tasks, three things quietly go wrong:

1. **Context gets compressed silently.** The agent drops information without telling you. By the time you notice the task has gone off track, it's too late.
2. **Switching sessions or agents resets everything.** You have to re-explain the background, re-establish context, re-state constraints. Every switch leaks information.
3. **You have no pause button.** You wait until context is full to switch — the agent decides the timing, not you.

The root cause is the same: your work context is inside a black box you don't control.

### How it works

Three commands:

```
handoff out          # freeze current context into a handoff package
handoff in <id>      # resume a specific handoff
handoff in latest    # resume the most recent handoff
handoff list         # list recent handoffs
```

When you run `handoff out`, the agent packages the current state and prints a resume command:

```
Handoff saved.

  ID:   20260316-1430-a3f2
  File: ~/.agents/handoff_context/20260316-1430-a3f2/handoff.md

  Next session → handoff in 20260316-1430-a3f2
```

Copy the last line. Paste it into any new session — same agent or different one.

When you run `handoff in`, the agent shows a recovery preview first: what's being worked on, where it stopped, what the next step is. It only continues after you confirm.

### The handoff package

Each handoff is a plain Markdown file with 8 fixed slots:

1. **Current task** — what's being worked on
2. **Current status** — where it stopped, what's blocked
3. **Completed** — what's already done
4. **Key decisions** — conclusions already made
5. **Key constraints** — things that can't be broken
6. **Key files** — files the next session should open first
7. **Next step** — an immediately executable action
8. **Pending** — the one blocking question, if any

Target length: under 100 lines. The goal is not completeness — it's recoverability.

### Cross-agent handoff

The handoff package lives at a fixed local path. Any agent can read it.

For example: use Claude Code for architecture design → `handoff out` → switch to Codex for backend development → `handoff in` → switch to Gemini for review → `handoff in`. Three agents, one shared context, no information lost between switches.

For larger projects: Claude Code designs the architecture, multiple Codex instances develop different backend modules in parallel, multiple Gemini instances handle different frontend modules — all reading from the same handoff package with shared constraints and interface definitions.

The prerequisite is clean task decomposition. If module boundaries are clear, this lets multiple agents run truly in parallel instead of waiting for you to brief each one.

### Cross-device handoff

Point the storage path to a cloud drive:

```bash
export HANDOFF_ROOT="~/Library/Mobile Documents/com~apple~CloudDocs/handoff_context"
# or
export HANDOFF_ROOT="~/Dropbox/handoff_context"
```

Freeze at the office. Resume at home. The work context travels with you.

### Installation

Copy this folder into your project:

```
your-project/
  .claude/
    skills/
      handoff-session/
        SKILL.md
        scripts/
        references/
```

Claude Code will pick up `SKILL.md` automatically.

### Files

```
handoff-session/
  SKILL.md          # skill definition loaded by the agent
  使用文档.md        # Chinese usage documentation
  scripts/
    handoff_file.sh # helper script for managing handoff packages
  references/
    templates.md    # handoff package templates
```

---

## 中文

跨会话交接协议，适用于 Claude Code 及其他 AI agent。

`handoff` 不是总结工具，而是一套"冻结现场 → 封装状态 → 恢复执行"的协议。在任意会话、任意 agent、任意设备中恢复执行。

### 解决的问题

长任务里有三个无声的问题：

1. **上下文被悄悄压缩。** agent 丢了什么你不知道，等发现任务跑偏已经是半小时后的事。
2. **换会话、换 agent 就断线。** 背景得重新交代，约束得重新解释，每次切换都在漏东西。
3. **没有暂停键。** 只能等 context 满了才被迫换，不是你在掌控节奏。

根子是同一件事：工作现场不在你手里。

### 三条命令

```
handoff out          # 冻结当前现场
handoff in <id>      # 恢复指定交接包
handoff in latest    # 恢复最近一次
handoff list         # 查看最近记录
```

`handoff out` 执行后直接打印恢复命令，复制最后一行，新会话粘贴即可。

`handoff in` 先给恢复预览，你确认后才继续执行。

### 跨 agent 协作

交接包存在本地固定路径，任何 agent 都能读取。

Claude Code 做需求分析 → `handoff out` → Codex 跑代码 → `handoff in` → Gemini 做 review → `handoff in`。三个 agent，同一份上下文，切换中没有信息丢失。

更大的项目：Claude Code 做整体架构设计，多个 Codex 并行开发不同后端模块，多个 Gemini 并行开发不同前端模块，共享同一份架构约束和接口定义。前提是任务拆解要干净，模块边界得定清楚。拆解没问题的话，多个 agent 可以真正并行，而不是排队等你一个个交代背景。

### 跨设备使用

路径指向云盘：

```bash
export HANDOFF_ROOT="~/Library/Mobile Documents/com~apple~CloudDocs/handoff_context"
```

公司冻结，家里恢复，现场还在。

### 安装

把文件夹复制到项目的 skills 路径下，Claude Code 会自动加载 `SKILL.md`。
