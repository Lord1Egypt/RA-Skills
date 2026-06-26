---
name: partial-implementation
description: Code returned as "done" is actually a stub — a placeholder body, a TODO comment, or a function that claims completion without real logic.
emoji: 🚧
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# partial-implementation

A function or module is declared complete, but the body is a stub. The most common form is a function with `pass`, `return None`, `throw NotImplementedError`, or a single `TODO:` comment in place of real logic.

## Symptoms

- Function signature exists but the body contains only a comment, `pass`, `return`, `throw new Error("not implemented")`, or similar.
- Placeholder values returned (`return 0`, `return {}`, `return null`) where real computation was requested.
- Tests pass only because the test is also a stub, or because the function always returns the fixture value.
- The agent claims a change is "complete" or "implemented" but no meaningful lines of logic were added.

## What to do

- Before declaring a task done, re-read every function you added or modified. If the body is a placeholder, the task is not done.
- Search the diff for `TODO`, `FIXME`, `XXX`, `NotImplementedError`, `unimplemented!`, `pass`, lone `return` or `return null`. Investigate each hit.
- Run the code end-to-end, not just the type-checker. A stub satisfies the type checker but fails at runtime.
- Compare the implementation against the task description: every bullet of the task should map to concrete lines of logic, not comments.
- If part of the task is genuinely out of scope, say so explicitly rather than stubbing silently.
