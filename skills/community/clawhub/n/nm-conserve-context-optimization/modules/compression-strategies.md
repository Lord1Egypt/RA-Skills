---
name: compression-strategies
description: |
  Pick one compression strategy for a bloated session: clear and catch up,
  a continuation agent, archive and summarize, or subagent delegation, with
  the savings and risk of each.
category: conservation
---

# Compression Strategies

Load this module when context feels sluggish, a task phase has just
ended, or quota burns faster than expected. Recommend one strategy,
with its reason and its estimated savings.

## Analyze First

Run `/context` for current usage, then estimate three things: how
much of the context is tool output rather than conversation, how many
turns have passed since the decisions still in force, and which files
are still active.

## The Four Strategies

**A. `/clear` and `/catchup`** fits a finished task phase, usage over
60%, and mostly stale content. Save critical state to
`.claude/session-state.md`, run `/clear`, then `/catchup` to reload
the active files.

**B. Continuation agent** fits usage over 80% with work in progress
that cannot stop. Run `Skill(conserve:clear-context)`, which hands the
saved state to an agent with a fresh context.

**C. Archive and summarize** fits usage of 40-60% with stale content
mixed into active content. Archive old decisions and errors to
`.claude/context-archive/`, summarize completed work, and continue.

**D. Delegate to a subagent** fits moderate pressure with independent
subtasks. Hand each subtask to an agent so the main context stays
lean.

## Savings and Risk

| Strategy | Typical Savings | Risk |
|----------|-----------------|------|
| /clear and /catchup | 70-90% | Low if state saved |
| Continuation agent | 80-95% | Low, state preserved |
| Archive and summarize | 20-40% | Very low |
| Delegate to subagent | 30-50% | Low, parallel work |
| Reversible compression (CCR) | 47-92% per archived output | Low, original cached |

The CCR row is per oversized tool output, not whole-context. Savings
depend on content type: logs compress hard, prose barely at all. See
`reversible-compression.md`. When the bloat is pasted log output,
filter before compressing, per `log-debugging-hygiene.md`.

## Context Archive

The `pre_compact_preserve` hook writes the context here before any
`/compact`:

```
.claude/context-archive/pre-compact-YYYYMMDD-HHMMSS-SESSIONID.md
```

## Exit Criteria

- [ ] Current usage and the tool-output share are stated
- [ ] One strategy is recommended, with the reason it fits
- [ ] Savings are estimated with the risk from the table above
- [ ] For a large tool output, the CCR handle and the
      `context_retrieve.py` command are given
- [ ] The recommendation is dropped when the bloat is dense prose,
      which compresses by roughly nothing
