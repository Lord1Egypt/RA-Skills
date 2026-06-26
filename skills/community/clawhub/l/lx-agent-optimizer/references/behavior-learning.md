# Behavior Learning

## Improvement Log Format

File: `~/.openclaw/workspace/improvement_log.md`

### Entry structure
```markdown
## YYYY-MM-DD (Week N)

**Review period:** YYYY-MM-DD to YYYY-MM-DD

### Problems (what went wrong)
1. **[Problem name]**: description of what happened and why it was bad
2. ...

### Lessons (what to do differently)
**Lesson 1: [Short title]**
Concrete behavior change, not vague intent.
Example: "Always check TOOLS.md before trying a tool command" not "be more careful"

**Lesson 2: ...**
```

## Weekly Cycle

Every Monday 9:00 AM:
1. Read improvement_log.md for history
2. Review last 7 days of conversations
3. Identify 2-3 concrete problems
4. Write specific, actionable lessons
5. Send brief report to user

## What counts as a problem
- User had to wait while agent fumbled
- Same mistake repeated from prior week
- User explicitly said "remember this" or "don't do that again"
- Task needed 3+ attempts before succeeding
- Agent asked user something that context already answered

## What counts as a good lesson
- Specific tool path or command to use
- Clear trigger: "when X happens, do Y"
- Verifiable: can check if followed next week
- NOT: "be more careful" / "think before acting"

## Promotion rules
- Lesson mentioned 3x in log → move to TOOLS.md or SOUL.md
- Verified repeatable workflow with easy-to-forget details → promote immediately to TOOLS.md
- If the user explicitly says "remember this" as a long-term preference → also record in MEMORY.md
- Lesson unused 60 days → archive or delete
- Lesson contradicted by new evidence → update immediately
