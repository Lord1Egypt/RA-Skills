# OpenClaw Launcher Protocol

## Goal
Bridge durable run state to actual OpenClaw subagent launches.

## Input
Launch manifests generated in:
- `runs/<run-id>/launch/`

Each manifest points to:
- run id
- phase
- role/agent
- handoff path
- project/worktree context
- suggested label

## Launcher behavior
An OpenClaw orchestrator session should:
1. run `python3 scripts/orchestration/launcher_preflight.py`
2. list pending launch manifests (`scripts/orchestration/list_pending_launches.py`)
3. read the referenced handoff markdown
4. call `sessions_spawn` with that handoff as the task prompt
5. only record a launch receipt via `scripts/orchestration/mark_launch.py` when the spawn is confirmed healthy

## Current blocker, clarified
The failure observed on 2026-04-20 and reproduced on 2026-04-21 is **not well explained by “hard-coded logic” or by heartbeat `999d` alone**.

What we can actually support with evidence is:
- `sessions_spawn` still times out even after heartbeat returned to `1d`
- similar spawn failures were already visible before the `999d` change
- the gateway log now shows repeated `active-memory timeout after 8000ms`, `lane wait exceeded`, and then gateway/tool timeouts

So the current best explanation is **gateway responsiveness / main-lane congestion**, not the orchestration design itself.

## Receipt rule
A `childSessionKey` returned alongside `status: error` is **not** a trustworthy launch receipt.

Treat a launch as real only when one of these is true:
- `sessions_spawn` returns success
- the child session becomes observable from the session tree
- an internal completion/update event proves the spawned child exists

Until then, do not mark the manifest as launched.

## Why manifests exist
Local scripts do not own OpenClaw tool access. The manifest is the durable bridge between file-native orchestration state and tool-native subagent spawning.

## Minimal contract
- handoff markdown remains the canonical task packet
- launch manifest is the canonical spawn request
- launch receipt is the canonical proof that an OpenClaw child session was spawned
- the orchestrator session remains the authority that actually launches agents
