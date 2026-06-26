# Decision Log — Detailed Guide

## What is a Decision?

A decision is a judgment made with incomplete information, where the outcome matters.

Not every action is a decision. But when you choose one path over another, that is.

## Why Record Decisions?

1. **Preserve context**: Six months later, you won't remember why you chose X over Y.
2. **Learn from outcomes**: Good decisions + good outcomes = validate your reasoning. Bad outcomes + good reasoning = learn something.
3. **Enable continuity**: When someone else takes over, they can understand your thinking.

## Decision Log Template

```markdown
# Decision — YYYY-MM-DD

## Title
[Short description]

## Date
YYYY-MM-DD

## Decision
[What you decided]

## Rationale
[Why this choice over alternatives]

## Alternatives Considered
[What else was on the table]

## Consequences
[Expected outcomes]

## Follow-up Actions
- [ ] Action 1
- [ ] Action 2

## Status
[pending | completed | reversed]
```

## When to Log a Decision

Log when:
- You spent significant time evaluating options
- The choice affects multiple projects or teams
- The decision is hard to reverse
- You're uncertain about the outcome

## Don't Log When:
- Routine operational choices
- Easily reversible decisions
- No real deliberation happened

## Project Decisions vs System Decisions

**Project decisions**: Go in `Projects/<name>/DECISIONS.md`

**System decisions**: Go in `Chronicle/decisions/YYYY-MM-DD-slug.md`

System decisions affect the whole OS. Project decisions are local to one project.

## Reviewing Decisions

During weekly review:
- Check follow-up actions on recent decisions
- Mark reversed decisions with outcome notes
- Look for patterns in decision quality

## Example

```
# Decision — 2026-03-25

## Title
Adopt weekly review cadence

## Date
2026-03-25

## Decision
Switch from ad-hoc reviews to weekly rhythm

## Rationale
Ad-hoc reviews never happen. Weekly creates discipline.

## Alternatives Considered
- Monthly (too infrequent)
- Daily (too much overhead)

## Consequences
- Reviews happen consistently
- Accumulated items get smaller batches

## Follow-up Actions
- [x] Set calendar reminder
- [ ] Draft first weekly review

## Status
pending
```
