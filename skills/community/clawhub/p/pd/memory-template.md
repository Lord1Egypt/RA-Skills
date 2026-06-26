# Memory Template — Productivity

Create `~/productivity/memory.md` with this structure:

```markdown
# Productivity Memory

## Status
status: ongoing
version: 1.0.4
last: YYYY-MM-DD
integration: pending

## Constraints
<!-- Real-life constraints that shape planning -->
<!-- Example: "School pickup at 15:00", "Back-to-back meetings Tue/Thu" -->

## Work Style
<!-- How work goes best when it goes well -->
<!-- Example: "Needs one clear top priority", "Prefers batch communication" -->

## Energy Patterns
<!-- Repeating energy windows, not one-day moods -->
<!-- Example: "Best focus 8:30-11:30", "Post-lunch low energy" -->

## Planning Preferences
<!-- Format and rhythm preferences -->
<!-- Example: "Likes weekly planning on Sunday", "Hates giant task lists" -->

## Current Friction
<!-- Structural problems worth remembering -->
<!-- Example: "Too many parallel projects", "Avoids ambiguous tasks" -->

## Review Rhythm
<!-- How they want to review/reset -->
<!-- Example: "Weekly review Friday afternoon" -->

## Notes
<!-- Short internal observations with clear value -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning the user's system | Gather context naturally |
| `complete` | Local system is in active use | Work from the existing files |
| `paused` | User does not want more setup questions | Stop prompting, still help |
| `never_ask` | User said stop asking about setup/memory | Never prompt again |

## Principles

- Store stable patterns, not every temporary mood
- Save only what helps future prioritization or planning
- Prefer constraints and preferences over life-story detail
- If it belongs in the active system, put it in `~/productivity/` files instead of memory
