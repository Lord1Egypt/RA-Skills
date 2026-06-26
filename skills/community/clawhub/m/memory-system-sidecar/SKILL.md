---
name: memory-system-sidecar
description: Operate, verify, rebuild, and debug the actual MemoryLab long-term memory sidecar that feeds `memory/ACTIVE_TASK_STATE.md` and `memory/LIVE_CONTEXT_PACKET.md`. Use when working on this repo’s implemented memory system: refreshing from session history, rebuilding indexes, running evals/tests, auditing milestone status, checking contamination boundaries, or inspecting memory artifacts under `memory-system/`, `memory/`, `history/`, and `scripts/context-refresh*`.
---

# Memory System Sidecar

Use this skill for the **implemented MemoryLab memory system**, not just abstract planning.

The system boundary is:
- **Context manager** = hot-path compactor
- **Memory sidecar** = long-term extraction, indexing, retrieval, consolidation
- **Bridge** = feeds retrieved memory back into `ACTIVE_TASK_STATE` / `LIVE_CONTEXT_PACKET` without treating them as source of truth

## Quick workflow

Choose the smallest workflow that matches the task.

### 1. Refresh live context + sidecar from a real session

Use when the user says things like:
- "refresh memory"
- "rebuild context from the laptop session"
- "update the live packet from the current session"

Run:

```bash
./skills/memory-system-sidecar/scripts/refresh_memory_system.sh
```

This wraps the repo’s standard end-to-end refresh path.

### 2. Verify the memory system still passes

Use when the user asks:
- "is the memory system working?"
- "does milestone 5 still hold?"
- "run the checks"

Run:

```bash
./skills/memory-system-sidecar/scripts/verify_memory_system.sh
```

This runs the main unit tests plus the eval harness.

### 3. Rebuild indexes only

Use when eval/retrieval drifts or docs mention stale-index behavior.

Run:

```bash
./skills/memory-system-sidecar/scripts/rebuild_memory_indexes.sh
```

Then rerun verify.

## Operating rules

- Treat raw history / transcripts as source of truth.
- Treat `memory/LIVE_CONTEXT_PACKET.md` as working memory, not durable storage.
- Do not treat retrieved-memory injection as new durable truth.
- Prefer repo wrappers (`scripts/context-refresh*`) over ad-hoc manual command chains.
- When status docs and runtime disagree, trust runtime checks after rebuild.

## Read these references when needed

- `references/commands.md` — exact command map for refresh / rebuild / verify / inspect
- `references/docs-map.md` — which doc is design vs status vs restore vs checklist

## Common files to inspect

- `memory-system/MILESTONE_STATUS.md`
- `docs/designs/MEMORYLAB_MEMORY_SYSTEM_MILESTONE_RESTORE.md`
- `docs/designs/MEMORYLAB_MEMORY_SYSTEM_BLUEPRINT.md`
- `memory/ACTIVE_TASK_STATE.md`
- `memory/LIVE_CONTEXT_PACKET.md`
- `memory/RETRIEVAL_CONTEXT_BUNDLE.json`
- `history/transcripts/*.md`

## Default debug order

When output looks wrong, inspect in this order:

1. `memory/ACTIVE_TASK_STATE.md`
2. `memory/LIVE_CONTEXT_PACKET.md`
3. `memory/RETRIEVAL_CONTEXT_BUNDLE.json`
4. `history/transcripts/*.md`
5. `memory-system/index/memory.db` freshness / rebuild state

## Compatibility rule

This skill operates the real sidecar already implemented in this repo. It should complement:
- `context-manager`
- `live-context-management`
- `long-term-memory`

Use this skill when the task is about **running or auditing the built system**, not just designing one.
