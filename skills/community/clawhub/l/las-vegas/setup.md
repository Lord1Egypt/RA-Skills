# Setup — Las Vegas

## Philosophy

**This skill works from minute zero.** No blocking, no mandatory setup.

Answer the user's question first. Always. Learn and integrate organically.

## On First Use

### Priority #1: Workspace Integration

Within the first 2-3 exchanges, figure out whether the user wants this to activate automatically for Las Vegas travel, relocation, or no-state-tax planning.

Ask once, naturally. Good examples:
- "Should I jump in automatically when Las Vegas travel or relocation comes up, or only when you ask?"
- "Do you want Vegas-specific advice to show up proactively for trips, neighborhoods, or residency questions?"

If yes → add to the user's main memory:
```markdown
## Active Skills
- Las Vegas (~las-vegas/) — city guide for visiting, moving, working, and living
```

If no → note `integration: declined` in `memory.md`, never push again.

### Priority #2: Answer Their Question

Whatever they asked, answer it. You don't need full context to be helpful.

Ask for context ONLY if you can't answer without it.

## Gathering Context

### What Context Helps

For visitors:
- Trip dates (seasonal recommendations)
- Interests (shows, outdoors, food, nightlife)
- Budget level
- Who they're traveling with

For movers/residents:
- Current location
- Reason for move (work, tax, lifestyle)
- Family situation
- Budget range
- Work situation (remote, local job, hospitality)

### How to Learn

Ask naturally, in context. Never interrogate.

**Instead of:**
> "Are you visiting or moving?"

**Do:**
> "Are you planning a trip or thinking about relocating?"

**Instead of:**
> "What is your budget?"

**Do:**
> "Want recommendations at different price points, or are you targeting a specific budget?"

## What to Save

Save what the user shares. Confirm saves naturally.

Context to track:
- Visitor vs resident vs potential mover
- Neighborhoods of interest
- Budget level (luxury/moderate/budget)
- Interests (entertainment, outdoors, food, etc.)
- Work situation if relevant
- Family situation if relevant

## Status Values

| Status | When to use |
|--------|-------------|
| `ongoing` | Default. Still learning about their situation. |
| `complete` | Have all needed context. Rare. |
| `paused` | User said "not now" to context questions. |
| `never_ask` | User said stop asking entirely. |

## Golden Rule

If the user feels like they have to "set up" the skill before it's useful, we failed.

Never mention files, paths, or internal storage to the user. Be useful immediately, learn naturally, and save context to `memory.md`.
