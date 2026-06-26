---
name: openclaw-rd-pipeline
description: Orchestrate OpenClaw end-to-end R&D delivery in Feishu from requirement intake to closure using PM, developer, reviewer, and tester subagents. Use when handling研发任务 that need structured requirement parsing, project-context enrichment from Feishu history/wiki, coding + PR flow, read-only review/testing gates, bug-loop rework, and final owner notification.
---

# OpenClaw R&D Pipeline

Execute a deterministic workflow for Feishu-driven R&D tasks with strict role boundaries, status transitions, and closure rules.

## Required Inputs

Collect or confirm these fields before starting:

- Feishu source context: group/chat ID, message URL, requirement text, requester
- Requirement metadata: priority, project tag, deadline
- Project configuration: repository URL, production branch, owner/team role mapping
- Task identifiers: requirement ID and Feishu task/doc IDs once created

If priority is missing, set it to medium.

## Role Boundaries

Apply these permissions strictly:

- Main agent: clone/update repository in read-only mode for context and handoff
- PM subagent: parse requirement, optimize prompt, coordinate confirmation, create Feishu task structure
- Developer subagent: create feature branch, implement code, push branch, open PR
- Reviewer subagent: read-only review, no code edits, no merge
- Tester subagent: read-only testing and CI verification, no code edits, no merge

Use an isolated git worktree and dedicated tmux session per subagent.

## Workflow

### 1) Intake and Context Build

Extract baseline fields from Feishu requirement.

Load project config and produce a shared `project_context` with:

- project name
- repository URL
- production branch
- owner/team mapping
- requirement metadata

Then deepen understanding through PM subagent:

- Query historical tasks in same Feishu group by project tag and requirement type.
- Load project Feishu wiki docs: product docs, API docs, prior decomposition cases, coding/UI/API/testing norms.
- Reuse prior parsing logic, edge cases, and acceptance criteria.

### 2) PM Structured Parsing Output

Generate:

- `structured_requirement`: business goal, inputs/outputs, boundaries, dependency modules/APIs, non-functional requirements
- `refined_prompt`: task prompt with historical references and explicit acceptance checks

For multi-module or multi-scenario tasks, call Superpowers skill for decomposition and acceptance criteria alignment. If unavailable, perform equivalent manual decomposition and mark it explicitly.

### 3) Prompt Confirmation and Task Creation

Send refined prompt to the responsible owner for confirmation.

If owner requests updates:

- propose changes with evidence from historical tasks and Feishu wiki
- iterate until approval

After approval:

- create Feishu master task/doc with status `待开始`
- create 3 first-level subtasks with status `待开始`: 编码, 评审, 测试
- attach relevant wiki norms in each subtask description

### 4) Development Stage

Set 编码 subtask to `进行中`, then execute:

- branch from production branch
- implement per project coding standards and historical patterns
- commit and push feature branch
- open PR to production branch
- include requirement ID, Feishu task ID, and knowledge-base links in PR title/description

Set 编码 subtask to `已完成` after PR is ready.

### 5) Review Stage

Set 评审 subtask to `进行中`, then perform read-only review for:

- logic correctness and edge cases
- exception handling
- security risks (injection, privilege issues, sensitive data)
- extensibility, reuse, performance
- UI/interaction conformance when frontend changes exist
- naming, structure, readability

Write findings in PR comments and cite historical review cases or wiki norms when relevant.

If pass, set 评审 subtask to `已完成`.
If fail, reject with actionable reasons linked to historical issue patterns.

### 6) Test Stage

Set 测试 subtask to `进行中`, then run:

- lint
- TypeScript type check
- unit tests
- Playwright E2E tests

Apply hard gate:

- if PR includes UI changes, require screenshot or recording in PR description
- if absent, fail CI and block merge

If pass, set 测试 subtask to `已完成`.
If fail, log defects using defect taxonomy norms.

### 7) Failure Loop and Bug Subtasks

When review or test fails:

- create BUG subtask under master task with status `待开始`
- include defect description, related norm, and similar historical bug case
- route back to developer subagent for fix and status progression `待开始 -> 进行中 -> 已完成`
- rerun review/test stages after fix

If repeated failures occur, re-open PM parsing to verify requirement interpretation.

### 8) Closure and Notification

Allow closure only when all are true:

- 编码 subtask completed
- 评审 subtask completed
- 测试 subtask completed
- all BUG subtasks completed

Then:

- set master task status to `已完成`
- notify owner in Feishu with summary package

Include in summary package:

- Feishu task card
- PM brief: parsing process, historical tasks/docs referenced
- Developer brief: branch, PR link, code delta
- Reviewer brief: decision, issue count, cited norms
- Tester brief: CI outcome, coverage/case count
- total cycle time
- optional comparison with similar historical tasks

## Output Templates

Load [references/templates.md](references/templates.md) and use those templates for:

- project context object
- refined prompt object
- PR description block
- review checklist
- test report
- final owner notification

Load [references/feishu-fields.md](references/feishu-fields.md) to map real Feishu fields into pipeline fields.

## Status Validation Script

Use [scripts/validate_status_flow.py](scripts/validate_status_flow.py) before state updates and before final closure.

Transition check:

```bash
scripts/validate_status_flow.py transition \
  --task-type subtask \
  --from-status 待开始 \
  --to-status 进行中
```

Snapshot check:

```bash
scripts/validate_status_flow.py snapshot --file status_snapshot.json
```

`status_snapshot.json` must include:

- `master`
- `coding`
- `review`
- `testing`
- `bug_subtasks` (list)
- `ui_changed` (bool)
- `ui_evidence_present` (bool)
