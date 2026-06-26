---
name: hizal-start
description: Initialize the agent's context memory session. Self-triggering — fires whenever the agent begins work, picks up a task, or enters a coding session. Use before searching, writing, or building anything. Handles session start, resume, and recovery. Triggers on phrases like "let me start working", "begin this task", "pick up where I left off", "start coding", "let's get started", or any time the agent enters a new work context without an active session.
---

# Hizal Start

Begin every work session with Hizal. Search before you build; write as you build.

## Session Lifecycle

### 1. Check for Existing Session

Call `get_active_session()` first. If `status="active"`, use the returned `session_id` and call `resume_session` to extend TTL. If `status="none"`, proceed to start a new session.

### 2. Start Session

```
hizal__start_session(lifecycle_slug="<slug>")
```

Returns a `session_id`. Keep it visible — needed for `register_focus` and `end_session`.

The agent's project and lifecycle context is assumed known. If unsure, check AGENTS.md or ask the user.

### 3. Register Focus (Optional)

If the task is known, register it immediately:

```
hizal__register_focus(
  session_id="<session-id>",
  task="<task description>",
  tags=["<tag1>", "<tag2>"]
)
```

See the `hizal-register-focus` skill for details on focus registration.

## After Starting

1. **Search Hizal** for existing context on the task (see `hizal-search` skill)
2. Only then begin coding or building
3. **Write to Hizal** as you make decisions (see `hizal-write` skill)
4. **End your session** when done (see `hizal-end` skill)

## Session Recovery

If you lose your `session_id` (context reset, compaction), call `get_active_session()` again and follow the same check/resume flow above.
