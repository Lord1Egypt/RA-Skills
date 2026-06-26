# Review Operator Guide

## What is a Review?

A review is a structured reflection on what happened, what's next, and what matters.

## Review Cadence

| Type | Frequency | Purpose |
|------|-----------|---------|
| Session | After each work session | Capture decisions, record progress |
| Daily | End of day | Surface stale items, plan tomorrow |
| Weekly | End of week | Look at bigger patterns |
| Monthly | End of month | Strategic alignment check |

## Review Questions

### Daily Review
1. What did I move today?
2. What stalled?
3. What should I do tomorrow?
4. What needs updating in my system?

### Weekly Review
1. What patterns emerged this week?
2. What went well? What didn't?
3. Are my projects on track?
4. Do my decisions need revision?
5. What's the most important thing next week?

## Review Workflow

```
1. Gather inputs
   - Check STATE.md for project states
   - Check TODO.md for task statuses
   - Check DECISIONS.md for recent decisions
   - Check Inbox for unprocessed items

2. Generate draft
   - Write what moved
   - Write what stalled
   - Identify blockers
   - Surface stale items

3. Take actions
   - Update project states
   - Promote items that need promotion
   - Make decisions on pending items

4. Output
   - Write review to Chronicle/reviews/
   - Update STATE.md
   - Update TODO.md
```

## Review Outputs

A good review produces:
- Updated project states
- Cleaned TODO items
- Promoted decisions or knowledge
- Actionable next steps

## Staleness Rules

An item is stale if:
- Task hasn't changed in 7 days and is still open
- Project state hasn't been updated in 14 days
- Decision follow-up is overdue
- Waiting item has been waiting > 7 days

## Session Review Template

```markdown
# Session Review — YYYY-MM-DD HH:MM

## What happened


## Decisions made


## Progress made


## Next steps

-
```

## Daily Review Template

```markdown
# Daily Review — YYYY-MM-DD

## 1. What moved today


## 2. What stalled or felt heavy


## 3. Routing and promotion actions
- [ ] Route raw capture
- [ ] Promote any lesson
- [ ] Update STATE.md
- [ ] Prune stale items

## 4. Active project snapshot

| Project | Status | Next action | Risk |
|--------|--------|-------------|------|
| | | | |

## 5. Decisions captured today


## 6. Top 3 focuses for tomorrow


## 7. Review outputs completed
- [ ]
```

## Tips

- Don't skip review because you're busy. The review is what keeps the system useful.
- Be honest about what stalled. Don't paper over problems.
- Update actual files, not just the review document.
- The review is only as good as its outputs.
