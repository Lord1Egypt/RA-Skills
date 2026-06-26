# Memory Template - Mercado Libre

Create `~/mercado-libre/memory.md` with this structure:

```markdown
# Mercado Libre Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- User profile, goals, constraints, and preferred decision style -->

## Priority
<!-- Current focus: compare, buy, sell, automate, or dispute -->

## Watchlist
<!-- Tracked products, target prices, and urgency notes -->

## Comparisons
<!-- Product A vs B decisions, trade-offs, and final recommendation -->

## Purchase Decisions
<!-- Buy-now vs wait decisions and rationale -->

## Seller Operations
<!-- Listing, pricing, stock, and post-sale notes -->

## Automation Log
<!-- API or panel automation plan, runs, failures, and fixes -->

## Disputes
<!-- Claims, evidence timeline, and next steps -->

## Notes
<!-- Internal reminders that improve continuity and speed -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning context | Ask only when missing context changes outcomes |
| `complete` | Context is stable | Prioritize execution and measurable results |
| `paused` | User deferred setup | Use existing context without extra setup prompts |
| `never_ask` | User requested no setup prompts | Never ask setup questions again |

## Key Principles

- Keep memory in natural language, not configuration-style key lists.
- Store only information that improves future decisions.
- Update `last` after each meaningful working session.
- Preserve failed decisions and incidents to avoid repeating mistakes.
- Never persist credentials unless user explicitly asks.
