---
name: openclaw-multi-agent-hq-builder
description: Build an OpenClaw multi-agent HQ system with a mother-bot plus sub-bots, including org design, role files, dispatcher, task state machine, blackboard protocol, and onboarding docs. Use this skill whenever the user wants to搭建多智能体组织、母bot/子bot体系、AI总部、调度系统、任务状态机、共享黑板、任务卡、或希望把一套多智能体工作流做成可安装、可复制、可教学的 OpenClaw skill/package.
---

# OpenClaw Multi-Agent HQ Builder

## Skill purpose
Use this skill to help a user build a **mother-bot + sub-bots** OpenClaw organization that is:
- structured
- installable
- teachable
- runnable
- upgradeable

When speed matters, optimize for a newcomer being able to finish the installation with a clear checklist, exact file list, and acceptance criteria before the stated deadline.

This skill is not for random prompt roleplay. It is for turning a multi-agent idea into a **working OpenClaw operating system skeleton**.

---

## What this skill builds
A standard delivery should include these layers:

### 1. Organization layer
Create or refine:
- org chart
- mother-bot / sub-bot division
- role boundaries
- reporting lines

### 2. Agent layer
For each core bot, create the four-file profile:
- `SOUL.md`
- `HEARTBEAT.md`
- `ROLE.md`
- `AGENT_PROFILE.md`

### 3. Protocol layer
Create or refine:
- work handbook
- task flow diagram
- input/output templates
- dispatcher rules

### 4. L5 operations layer
Create or refine:
- task state machine
- task card template
- blackboard protocol
- review mechanism
- system upgrade log

### 5. Onboarding layer
Create or refine:
- installation guide
- newcomer checklist
- first task demo card

---

## Default build order
Do not start by writing lots of personalities. Build in this order:

1. Confirm the mother-bot and core sub-bots
2. Confirm role boundaries and responsibilities
3. Build the HQ docs
4. Install each bot's four-file profile
5. Build dispatcher and workflow docs
6. Build task state machine and blackboard docs
7. Build onboarding docs for newcomers
8. Create a first live task card example

Reason: new users fail when they start with too many agents and too little structure.

---

## Recommended core architecture
Unless the user clearly wants a different structure, prefer this minimum HQ:

- `001` mother-bot / CEO / dispatcher / final decider
- `02` value and resource bot
- `03` problem definition and logic bot
- `04` long-term direction and principles bot
- `05` execution and delivery bot

Keep the HQ **small and hard**.
If the user mentions 06-10 or more specialized agents, default to an **outer specialist pool**, not permanent HQ members.

---

## Standard delivery files
When building from scratch, aim to produce these files or their equivalents:

### HQ docs
- `组织架构总表.md`
- `母bot与子bot工作手册.md`
- `001-05任务流转图.md`
- `001-05标准输入输出模板包.md`
- `001-dispatcher.md`
- `001-dispatcher-runbook.md`
- `多智能体技术路线图.md`

### L5 docs
- `任务状态机.md`
- `任务卡模板.md`
- `共享黑板协议.md`
- `复盘机制.md`
- `复盘模板.md`
- `系统升级日志.md`

### Task system
- `tasks/`
- `tasks/TASK-001-*.md`
- `tasks/TASK-002-*.md`

### Per-bot files
For `001` to `005`, create:
- `teammates/<id>/SOUL.md`
- `teammates/<id>/HEARTBEAT.md`
- `teammates/<id>/ROLE.md`
- `teammates/<id>/AGENT_PROFILE.md`

---

## Installation workflow for a newcomer
When the user wants a teachable installation package, produce an onboarding guide that walks them through:

### Step 1: Confirm structure
Have them decide:
- how many core bots
- what each bot is responsible for
- what stays in HQ vs outer specialist pool

### Step 2: Build HQ documents
Create the shared HQ governance files first.

### Step 3: Install the bot profiles
Create the four-file profile for each bot.

### Step 4: Install the dispatcher
Set up `001-dispatcher.md` and `001-dispatcher-runbook.md`.

### Step 5: Install L5 operations
Set up state machine, task cards, blackboard, review system, and upgrade log.

### Step 6: Run one real task
Create a first real `TASK-001` or `TASK-002` and run the full chain.

---

## Newcomer success checklist
A newcomer should be considered successful only if all of the following are true:

- HQ structure is clear
- each core bot has all 4 files
- dispatcher exists
- task state machine exists
- task card template exists
- blackboard protocol exists
- review mechanism exists
- upgrade log exists
- `tasks/` directory exists
- at least one real task card exists
- the user can explain the routing chain from 001 to sub-bots and back

---

## Output style
When using this skill, prefer outputs that are:
- concise
- structured
- installable
- easy to follow for a newcomer
- explicit about file paths and check steps

Do not give abstract theory without telling the user what files to create and in what order.

---

## Suggested report structure
For setup requests, use this structure:

1. Conclusion
2. What will be created
3. Exact file list
4. Recommended order
5. Key risks
6. Final acceptance checklist

---

## Anti-patterns
Avoid these mistakes:
- too many bots too early
- vague role descriptions with no file outputs
- no dispatcher
- no state machine
- no task cards
- no review loop
- no newcomer checklist
- relying only on chat history instead of files

---

## Bundled resources
Read these bundled resources when needed:
- `references/install-guide.md` for newcomer installation teaching
- `references/acceptance-checklist.md` for final quality checks
- `references/minimal-examples.md` for task card / blackboard / review minimal examples
- `references/test-prompts.md` for quick trigger and delivery checks and realistic request coverage
- `references/publish-checklist.md` for pre-release checks before declaring the skill ready to ship

---

## Core sentence
The goal is not to create more agents.
The goal is to create a **small, hard, teachable multi-agent HQ that can actually run.**
