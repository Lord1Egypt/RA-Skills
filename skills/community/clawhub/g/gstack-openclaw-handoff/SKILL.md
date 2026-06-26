---
name: gstack-openclaw-handoff
description: "Compact the current conversation into a handoff document for another agent or fresh session to continue the work. Captures decisions, open threads, artifacts, and suggests skills. Use when: ending a long session, switching agents, handing off to a teammate, or user says handoff, wrap up, save context."
---

# Handoff

Write a handoff document so a fresh agent can continue this work with zero ramp-up time.

## Process

1. **Synthesize** the current conversation into a structured handoff. Don't rehash — compress.
2. **Reference, don't duplicate.** If content already lives in a committed file, PR, issue, or plan — reference it by path or URL. Never copy large blocks.
3. **Redact** API keys, passwords, tokens, or PII. Replace with `[REDACTED]`.
4. **Save** to the OS temporary directory (not the workspace). Tell the user the absolute path so they can feed it to the next session.

## Handoff Template

```markdown
# Handoff: {task summary}
Date: {YYYY-MM-DD}
From: {session context — e.g. "OpenClaw session on branch feature/x"}

## Goal
{One sentence: what we're trying to accomplish}

## Current State
{What's done, what's in progress, what's blocked}
- Completed: ...
- In progress: ...
- Blocked on: ...

## Key Decisions Made
{Decisions that would be expensive to re-derive}
- Decision 1: chose X over Y because Z
- Decision 2: ...

## Open Threads
{Unresolved questions, known issues, things the next session should address}
1. ...
2. ...

## Artifacts
{Paths, URLs, branches — anything the next agent needs to find}
- Branch: ...
- Key files modified: ...
- Related PR/issue: ...

## Suggested Skills
{Skills the next session should invoke}
- /skill-name — reason

## Context the Next Agent Won't Have
{Anything learned during conversation that isn't captured in code/commits}
- ...
```

## Tailoring

If the user passed arguments (e.g. "handoff — next session will focus on the frontend"), tailor the Open Threads and Suggested Skills sections toward that focus. Deprioritize context irrelevant to the next session's scope.

## What NOT to include

- Full code listings (reference the file path instead)
- Conversation transcript or dialogue replay
- Debugging dead-ends that were fully resolved
- Anything already captured in git history
