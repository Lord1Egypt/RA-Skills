---
name: shared-memory
description: Set up shared memory between multiple OpenClaw agents so they stay in sync without the user repeating context. Use when a user has 2+ agents (workspaces) and wants them to share knowledge, sync conversation summaries, and maintain a common long-term memory. Also use when user asks about multi-agent setup, agent sync, or says things like "stop repeating myself to different agents".
---

# Shared Memory for Multi-Agent OpenClaw

## What This Solves

When a user runs multiple OpenClaw agents, each agent has no idea what the other discussed with the user. The user becomes a "messenger" repeating the same context. This skill sets up automatic knowledge sharing between agents.

## Prerequisites

The user needs 2+ OpenClaw agent workspaces. If they only have one agent, explain:

> 要用共享记忆，你需要至少两个 Agent（两个 workspace）。在 OpenClaw 里，每个 Agent 是一个独立的 workspace 目录，有自己的 AGENTS.md、SOUL.md 和记忆文件。你可以通过 `openclaw` 配置多个 workspace，每个绑定不同的身份和职责。

If the user is unsure how to set up multiple agents, help them understand the concept first before proceeding.

## Setup Procedure

When the user asks to set up shared memory, follow these steps. **Do everything automatically** — only ask the user for information you cannot determine yourself.

### Step 1: Gather info (ask the user)

Ask these questions in one message:

1. How many agents do you have, and what are their names/emoji? (e.g. 小爪🦞, 小澜🌊)
2. Where are their workspace directories? (e.g. `~/.openclaw/workspace`, `~/.openclaw/workspace-sister`)
3. Which workspace should host the shared directory? (recommend the primary/main agent's workspace)

### Step 2: Create the shared directory structure

In the host workspace, create:

```
shared-knowledge/
├── SHARED-MEMORY.md
├── README.md
├── sync/
│   ├── <agent-a-id>-latest.md
│   └── <agent-b-id>-latest.md
└── projects/
```

Use short lowercase IDs for sync filenames (e.g. `xiaozhua`, `xiaolan`).

**SHARED-MEMORY.md** — Initialize with the user's basic info if you know it, otherwise create a skeleton:

```markdown
# SHARED-MEMORY.md - <Agent A Name> & <Agent B Name> 共享记忆

> 所有参与 Agent 的公共知识库，双方都可以读写。
> 私人人格、独立记忆不放这里，只放大家都需要知道的信息。

---

## 用户基本信息

(fill in what you know)

## 工作上下文

(fill in what you know)

## 重要决定

(leave empty for now)

## 家庭成员（AI Agent）

- <emoji> <name> — <role>
- <emoji> <name> — <role>
```

**Each sync file** — Initialize with:

```markdown
# <Agent Name> 最近对话摘要

> 由 <Agent Name> 自动更新，供其他 Agent 了解最新上下文

(暂无记录)
```

**README.md** — Write a brief usage guide covering: directory structure, what goes here / what doesn't, sync protocol.

### Step 3: Link the shared directory to other workspaces

For each non-host workspace, create a symlink so all agents access the same physical directory:

**Windows (PowerShell, run as admin):**
```powershell
New-Item -ItemType SymbolicLink -Path "<other-workspace>\shared-knowledge" -Target "<host-workspace>\shared-knowledge"
```

**macOS/Linux:**
```bash
ln -s <host-workspace>/shared-knowledge <other-workspace>/shared-knowledge
```

Verify the symlink works by reading a file through it.

### Step 4: Update each agent's AGENTS.md

Append the shared memory protocol block to each agent's `AGENTS.md`. Customize the names and paths for each agent's perspective.

The block to add (customize per agent):

```markdown
## 🤝 共享记忆协议（和 <Other Agent Name>）

你有个搭档叫 **<Other Agent Name>**，是用户的另一个 AI 助手。你们共享一个知识库，避免用户重复描述同样的事情。

### 目录：`shared-knowledge/`
- `SHARED-MEMORY.md` — 共享长期记忆（用户信息、项目、决策）
- `sync/<other-agent-id>-latest.md` — <Other Agent Name> 最近聊了什么
- `sync/<my-agent-id>-latest.md` — **你负责更新这个文件**
- `projects/` — 项目相关共享文档

### 你需要做的：
1. **每次对话开始**：读 `shared-knowledge/SHARED-MEMORY.md` 和 `sync/<other-agent-id>-latest.md`
2. **每次对话结束**：更新 `sync/<my-agent-id>-latest.md`（写你和用户聊了什么要点）
3. **有重要新信息时**：更新 `SHARED-MEMORY.md`（新的决策、项目进展等）

### 边界：
- ✅ 共享：工作上下文、项目进展、用户的偏好和决策、对话摘要
- ❌ 不共享：你的 SOUL.md、IDENTITY.md、私人想法和人格设定
```

Also add to the "Every Session" checklist in AGENTS.md:

```markdown
- **读共享记忆**：Read `shared-knowledge/SHARED-MEMORY.md`
- **读搭档动态**：Read `shared-knowledge/sync/<other-agent-id>-latest.md`
```

### Step 5: Verify

1. Read a file from `shared-knowledge/` in each workspace to confirm access works
2. Write a test line to one agent's sync file
3. Read it from the other workspace to confirm the symlink is working
4. Remove the test line

### Step 6: Tell the user it's done

Summarize what was set up and explain the behavior they should expect:

> 设置完成！从现在开始：
> - 每次我们聊完，我会自动更新我的同步文件
> - 下次你的另一个 Agent 上线时，它会先读我写的摘要，自动了解我们聊了什么
> - 重要决定会同步到共享记忆里，所有 Agent 都能看到
> - 你不用再重复告诉每个 Agent 同样的事情了

## Protocol Rules (for the agent using this skill)

After setup is complete, follow these rules in every session:

| Trigger | Action |
|---------|--------|
| Session start | Read `SHARED-MEMORY.md` + all other agents' sync files |
| Session end | Update own sync file with conversation highlights |
| Important new info | Update `SHARED-MEMORY.md` |

### What goes in shared memory
- ✅ User info, preferences, decisions
- ✅ Project context and progress
- ✅ Conversation summaries
- ✅ Shared reference documents

### What stays private
- ❌ Agent personality (SOUL.md, IDENTITY.md)
- ❌ Private memories and persona settings
- ❌ Credentials, tokens, passwords

## Scaling to 3+ Agents

For each additional agent:
1. Add a sync file: `sync/<new-agent-id>-latest.md`
2. Symlink `shared-knowledge/` into the new workspace
3. Add the protocol block to the new agent's AGENTS.md (listing ALL other agents)
4. Update existing agents' AGENTS.md to also read the new agent's sync file
