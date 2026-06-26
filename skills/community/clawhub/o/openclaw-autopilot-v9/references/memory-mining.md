# Autopilot Memory Mining Reference v9.1

How to perform a real full-history recall instead of a shallow recent-context skim.

## Goal

Give Autopilot a complete historical picture before it acts independently.

That means:

- not stopping at today's or yesterday's notes
- not relying only on a semantic search hit list
- not ignoring reversals, stale plans, or old failures

## Full Historical Sweep Protocol

### Direct/Main Chats

Use this order:

1. Read `MEMORY.md`
2. Enumerate all `memory/*.md` files
3. Read every daily memory file
4. Build an internal historical timeline
5. Only then begin autonomous planning/execution

### Shared/Group Chats

Use this safer order:

1. Skip private `MEMORY.md`
2. Only read memory files that are appropriate for the context
3. Never expose private long-term memory in a shared room

## What to Extract During the Sweep

Track at least these categories:

- active and paused projects
- repeated user preferences
- standing bans / hard rules / safety constraints
- past reversals and rollbacks
- recurring failures and their fixes
- open loops and promised follow-ups
- named people, systems, devices, and repositories
- changes in workflow preference over time

## Conflict Resolution

If memory sources disagree:

1. Prefer the newer note
2. Check whether the older rule was explicitly superseded
3. If still ambiguous, surface the uncertainty instead of hallucinating certainty

## Large-Corpus Strategy

If there are many daily notes:

1. Enumerate files first
2. Read in chronological batches
3. Maintain a compact scratch summary while reading
4. Mark important transitions: installs, removals, policy changes, project pivots, failures, user corrections

Do not call the sweep complete until all memory files in scope have been covered.

## During Execution

After the full sweep:

- use targeted memory search for task-specific lookup
- re-open exact files when precision matters
- avoid re-reading the whole corpus unless the context changed materially

## Minimum Historical Summary

Before acting autonomously, be able to answer:

- What is ongoing?
- What was explicitly disabled or removed?
- What does the user consistently prefer?
- What mistakes already happened here?
- What older context is still relevant right now?
