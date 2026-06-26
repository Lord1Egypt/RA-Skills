---
name: lark-cli-devhub-taskflow
description: Use when turning development work into Feishu/Lark tasks through lark-cli or feishu-cli, including task lists, bug queues, status updates, blocked work, next actions, or task-linked Dev Hub records.
metadata:
  requires:
    bins: ["lark-cli"]
---

# Lark CLI Dev Hub Taskflow

Use Feishu Tasks for current work state. Use Base for durable bug evidence, decisions, and lessons learned.

Discovery aliases: `feishu-cli task`, `飞书任务`, `lark-cli task`, `Lark Tasks`, `bug queue`, `developer task list`.

## Task Lists

Recommended task lists:

- `Dev Hub Inbox`
- `Current Sprint`
- `Bug Queue`
- `Release Checklist`
- `Backlog`

## Status Discipline

Keep status small and explicit:

- `Inbox`: captured but not shaped.
- `Ready`: clear next action exists.
- `Doing`: actively being changed.
- `Blocked`: needs user, external system, or missing permission.
- `Review`: implementation done, needs review.
- `Verify`: needs test/manual verification.
- `Done`: verified enough for the agreed scope.

## Linkage

When a task results in a fix:

- Update the Feishu task status.
- Write a `Bugfix` record when code changed to fix a bug.
- Write an `AI Run` record when an AI agent did meaningful investigation or implementation.
- Store the Feishu task URL in the Base `Tasks` table or the related Bugfix field.

## Avoid

- Do not make every thought a task.
- Do not put root cause detail only in task comments.
- Do not close a bug task unless the verification result is recorded somewhere durable.

When official `lark-task` skill is installed, use it for exact CLI syntax and task GUID handling.
