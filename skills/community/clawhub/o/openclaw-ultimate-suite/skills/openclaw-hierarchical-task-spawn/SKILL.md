---
name: hierarchical-task-spawn
homepage: https://github.com/wd041216-bit/openclaw-hierarchical-task-spawn
description: Plan and execute spawned OpenClaw work as a task tree instead of a flat list. Use when a medium task should be split into fine sub-tasks, or a complex task should be split into medium workstreams that can further split into fine tasks.
---

# Hierarchical Task Spawn

Use this skill when one spawned task is still too big.

## Goal

Turn substantial work into a small task tree:

- simple work -> do it directly
- medium work -> split into a few fine tasks
- complex work -> split into medium workstreams, then split those into fine tasks if needed

## Complexity Ladder

### Simple

Do not spawn.

Use direct execution when the task can be finished in one short flow with little search, no meaningful branching, and no multiple deliverables.

### Medium

Split into fine tasks when the request has 2-4 meaningful steps or deliverables.

Examples:

- research + summary + table
- outline + draft + polish
- collect inputs + generate PPT + final QA

### Complex

Split into medium workstreams first when the request contains clearly different domains, multiple deliverables, or enough uncertainty that one child task would become bloated.

Examples:

- market scan + PM plan + PPT deck
- source collection + competitor analysis + executive summary + spreadsheet
- requirement clarification + implementation plan + artifact generation

## Tree Shape

Prefer a shallow tree with explicit ownership:

1. root request
2. medium workstreams
3. fine execution tasks

Default depth limit: 3 levels including the root.

## Workflow

### 1. Classify the task

Decide whether the request is simple, medium, or complex before spawning.

### 2. Split only where useful

- medium task -> 2-4 fine tasks
- complex task -> 2-5 medium workstreams
- each medium workstream may split into 2-4 fine tasks if needed

Do not create child tasks for cosmetic micro-steps.

### 3. Assign the right owner

Use the best specialist for each branch:

- `research` -> search, source review, verification, comparisons
- `office` -> team coordination, milestones, meeting outputs, shared execution
- `slides` -> personal planning, prioritization, private execution
- `council` -> multi-perspective debate
- current agent -> when the work still belongs here

Keep `family` and `kittypuppy` isolated to their own contexts unless the user is already in those agents.

### 4. Spawn by layer

- root spawns medium branches when the task is complex
- a medium branch may spawn fine tasks if it is still too broad
- leaf tasks should execute real work instead of just rephrasing the plan

## Leaf Task Standard

A leaf task should be concrete enough to finish without further decomposition.

Good leaf tasks:

- `搜索 2026 年 AI agent 框架并提取发布时间、价格、定位`
- `把研究结果整理成 6 页 PPT 初稿`
- `把会议纪要整理成 owner/deadline/action list`

Bad leaf tasks:

- `继续想一想`
- `处理这个项目`
- `完成所有内容`

## Reporting

Prefer progressive reporting:

- leaf tasks can report their own results when useful
- parent tasks should aggregate only related branches
- do not wait for unrelated branches if one finished result is already valuable

In Feishu, pair this skill with `feishu-parallel-dispatch` and `feishu-task-status`.

## Guardrails

- Do not recurse forever
- Prefer 3-8 active leaves, not a swarm
- Stop splitting once the next child would be a single-tool or single-deliverable action
- If the user clearly wants one synchronous answer, keep the tree internal and return one combined result
- If one branch stalls, do not block the whole tree from reporting other finished branches

## Example

User asks:
`帮我做一个行业调研、整理成对比表，再做一份给老板的 PPT`

Good split:

1. medium branch: `研究与证据`
2. medium branch: `表格整理`
3. medium branch: `PPT 生成`

Then:

- `研究与证据` may split into search / browse / verify
- `PPT 生成` may split into outline / slide draft / QA

This keeps each child narrow enough to finish well.
