# AGENTS.md — Worker Operating Instructions

## Every Session

1. Read `SOUL.md` — your identity
2. Read the task brief you received — your mission
3. Check `tasks/` if brief references a task ID — for context

## How You Work

1. **Read the brief** — Understand exactly what's asked
2. **Check existing state** — Read relevant files before modifying
3. **Execute** — Do the work using your tools
4. **Verify** — Confirm the result matches acceptance criteria
5. **Callback** — Report back to Leader with results

## Memory

You share Leader's memory system (MEMORY.md, memory/, shared/).

- **DO NOT** update MEMORY.md or shared/ unless the brief explicitly asks you to
- If you're told to update memory/daily notes → write to `memory/YYYY-MM-DD.md`
- Task state files → update `tasks/T-{id}.md` as instructed

## Task Completion & Callback

After completing a task:

1. **Send callback to Leader:**
   ```
   sessions_send to {Callback to value from brief} with timeoutSeconds: 0
   Message:
   [TASK_CALLBACK:{Task ID}]
   agent: worker
   signal: [READY] | [BLOCKED] | [NEEDS_INFO]
   output: {concise result summary}
   files: {relevant file paths}
   ```

2. **Critical rules:**
   - Use the `Callback to` value from the brief as session key
   - **NEVER** use `"main"` — that resolves to your own session
   - Tag all deliverables `[PENDING APPROVAL]`
   - Keep output concise — full details stay in files

## Context Loss

If you can't recall the task context after compaction:

1. Read `tasks/` directory for active task files
2. Send `[CONTEXT_LOST]` to Leader with your agent name
3. Wait for re-briefing

## Communication Signals

See `shared/operations/communication-signals.md`.
