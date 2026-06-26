# Best Practices — Mjolnir Brain

## For Users

### 1. Bootstrap Right
Take time during the bootstrap conversation. The better your SOUL.md and USER.md are, the better the agent performs. Don't rush it.

### 2. Correct, Don't Repeat
When the agent makes a mistake, tell it *why* it was wrong, not just *what* to do instead. This helps it write better rules.

### 3. Review MEMORY.md Monthly
Skim through it. Remove outdated info. Add context the agent might have missed. It's a collaborative document.

### 4. Trust the System
Let the cron jobs run. Let the heartbeat work. Don't manually manage memory files unless something is clearly wrong.

## For Agent Developers

### 1. Keep MEMORY.md Under 20KB
This is a hard cap. Every token counts at session startup. If MEMORY.md grows beyond 20KB:
- Remove entries older than 90 days that haven't been referenced
- Merge similar entries
- Move detailed content to daily logs (link from MEMORY.md if needed)

### 2. Write Conclusions, Not Processes
```
❌ "We tried A, then B, then discussed C, and finally decided D because..."
✅ "Decision: D. Reason: X. Alternatives considered: A, B, C."
```

### 3. Tag Everything
Use `[universal]` and `[env-specific]` tags in Common Errors and Lessons sections. This makes it easy to extract transferable knowledge.

### 4. strategies.json is Your Most Valuable File
- Add new problem types as soon as they appear
- Always update success rates after trying a solution
- Keep solutions sorted by successRate (the update script does this automatically)
- Add environment tags when solutions are env-specific

### 5. Don't Over-Automate
The system works because it's simple. Resist the urge to add:
- Databases (grep is fast enough for <100 files)
- Complex scheduling (5 cron jobs is plenty)
- External services (zero deps is a feature)

### 6. Playbook Discipline
A good playbook has:
- Clear parameters (what changes each time)
- Pre-checks (don't start if prerequisites aren't met)
- Rollback steps (what to do when things go wrong)
- A creation date (for tracking staleness)

### 7. Heartbeat Hygiene
- Don't check everything every heartbeat — rotate checks
- Keep idle task queue short (≤5 items)
- Use heartbeats for maintenance, not for user-facing work

## Anti-Patterns

### ❌ Memory Hoarding
Don't save everything. If it won't matter in a week, don't write it to MEMORY.md.

### ❌ Strategy Sprawl
Don't create a strategy entry for every possible error. Focus on errors that:
- Happen more than once
- Have non-obvious solutions
- Cost significant time to debug

### ❌ Playbook Bloat
Not every operation needs a playbook. Only create them for operations that:
- Happen ≥3 times
- Have more than 3 steps
- Involve risk (deployment, data changes)

### ❌ Ignoring Consolidation
If the AI consolidation cron isn't running, daily logs pile up and MEMORY.md goes stale. Check `memory/memory-state.json` periodically.
