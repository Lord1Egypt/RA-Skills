# Memory Template — Kimi

Create `~/kimi/memory.md` with this structure:

```markdown
# Kimi Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- What the user is trying to achieve with Kimi -->
<!-- Example: Use Kimi as the cheap long-context pass before a stricter local validator -->

## Routes
<!-- Primary and fallback route per workload in natural language -->
<!-- Example: Default to Kimi for document synthesis, but use another route for strict tool JSON if parse quality drops -->

## Approvals
<!-- What data may leave the machine and what must be redacted -->
<!-- Example: Internal incident notes allowed only after secrets and customer IDs are masked -->

## Constraints
<!-- Cost, privacy, latency, and deployment boundaries -->
<!-- Example: Keep batch spend capped, never send production tokens, prefer copy-paste curl checks -->

## Notes
<!-- Repeated failures, parser quirks, or migration gotchas -->
<!-- Example: Stale model IDs cause 404s; always refresh /models before changing prompts -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning routes | Keep refining workload defaults |
| `complete` | Stable Kimi workflow exists | Ask fewer setup questions |
| `paused` | User said not now | Avoid new setup prompts |
| `never_ask` | User rejected setup | Never request more setup details |

## Key Principles

- Store routes and approval boundaries, not secrets.
- Capture redaction rules before saving workflow defaults.
- Keep notes short enough to improve the next Kimi decision.
- Update `last` after meaningful Kimi work.
