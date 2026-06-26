# Memory Template - Groupon

Create `~/groupon/memory.md` with this structure:

```markdown
# Groupon Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Usual city or ZIP:
- Typical budget:
- Preferred categories:
- Travel radius:
- Timing constraints:
- Hard no rules:

## Notes
- Repeated merchant wins or misses:
- Booking friction patterns:
- Refund or support lessons:

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning practical deal preferences | Gather context when it changes the outcome |
| `complete` | Enough context for most Groupon tasks | Work normally and update only when patterns shift |
| `paused` | User does not want more setup for now | Use the current context and avoid extra setup questions |
| `never_ask` | User does not want proactive context gathering | Only use explicit instructions already provided |

## Optional Supporting Files

Create these only when they become useful:

```markdown
# ~/groupon/shortlists.md

## YYYY-MM-DD
- Deal:
  Verdict:
  Why:
  Caveats:
```

```markdown
# ~/groupon/purchases.md

## Active vouchers
- Deal:
  Status:
  Book by:
  Next step:
```

```markdown
# ~/groupon/incidents.md

## YYYY-MM-DD
- Merchant or deal:
  Issue:
  Support path:
  Outcome:
```

## Key Principles

- Store reusable context, not one-off chatter.
- Never store payment methods, login secrets, or full voucher codes.
- Keep notes short, concrete, and tied to better future decisions.
- Update `last` whenever the file changes.
