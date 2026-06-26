---
name: hizal-end
description: Close the agent's context session and consolidate what was learned. Self-triggering — fires when the agent finishes a task, wraps up work, or is about to go idle. Handles the keep/promote/discard review of surfaced memory chunks. Triggers on phrases like "I'm done", "that's it for now", "wrapping up", "let me commit and close out", "finished this task", or any time the agent is ending a work session.
---

# Hizal End

Close your session. Review what surfaced. Let knowledge compound.

## End Session

```
hizal__end_session(session_id="<session-id>")
```

## Review SURFACE Chunks

The session end returns MEMORY chunks tagged for consolidation review. For each chunk, decide:

### Keep
Useful personal observation. Leave as AGENT memory. No action needed.

### Promote
Valuable for the team. Write it back as a PROJECT chunk:

```
# For architecture/design decisions
hizal__write_knowledge(project_id="<id>", query_key="<key>", title="<title>", content="<chunk-content>")

# For codebase conventions
hizal__write_convention(project_id="<id>", query_key="<key>", title="<title>", content="<chunk-content>")
```

Then optionally delete the original AGENT chunk:
```
hizal__delete_context(project_id="<id>", id="<chunk-id>")
```

### Discard
Noise or one-off observation. Ignore it.

## When to End

- At the end of a work session
- When switching to a completely different project/task (end old, start new)
- Before a long break

## Session Recovery After End

If you need to resume work later, call `hizal-start` — it will start a fresh session or resume an existing one.
