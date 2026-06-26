# Artifacts and log wiring

This document defines how `local-coding-orchestrator` should persist worker execution artifacts.

## Goal

Before attaching real worker execution, make sure every run has a predictable place for:
- prompt / brief
- raw log
- structured result
- short summary
- launch metadata

## Recommended directories

```text
local-orchestrator/
  tasks/
  prompts/
  logs/
  results/
  reviews/
  state/
```

## Task record responsibilities

The task record should carry two related but different concepts.

### 1. `artifacts`

Persistent file locations associated with the task:
- `promptPath`
- `logPath`
- `resultPath`
- `summaryPath`
- `reviewPath`
- `prUrl`

### 2. `workerRun`

The latest execution metadata for the currently active or most recent worker run:
- `tool`
- `role`
- `startedAt`
- `finishedAt`
- `exitCode`
- `status`
- `logPath`
- `resultPath`
- `summary`

## Why keep both

`artifacts` answers: where are the files?
`workerRun` answers: what happened during the last execution?

## Minimum statuses for workerRun

Suggested values:
- `planned`
- `running`
- `completed`
- `failed`
- `blocked`

## First safe step

Before running workers directly, the adapter should at least:
- allocate log and result paths
- write prompt path
- write workerRun metadata with `planned`
- update the task record

That makes the next step—real tool execution—much safer to wire up.
