# Background worker model

This document defines the next-step execution model for `local-coding-orchestrator`.

## Why background mode

Local coding CLIs can take a long time or block interactively.
Because of that, synchronous execution should not be the default orchestration path.

## Goal

Track background worker execution as a supervised handle, not as a blocking call.

## Minimum metadata to persist

Store background execution details in `workerRun`:
- `mode`: `background`
- `sessionId`: OpenClaw process session id
- `pid`: underlying process id when available
- `startedAt`
- `lastPolledAt`
- `finishedAt`
- `status`
- `exitCode`

## Expected flow

1. launch worker in background
2. persist session handle into the task record
3. mark worker run as `running`
4. let supervisor poll objective state later
5. on completion, write result/log metadata and update task record

## Important rule

Do not confuse:
- worker still running
- worker exited cleanly
- task completed

Worker completion is only one signal. The supervisor still owns task completion.
