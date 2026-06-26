# Memory Template - Google Pay

Create `~/google-pay/memory.md` with this structure:

```markdown
# Google Pay Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Project Snapshot
platform: web | android | hybrid
psp: unknown
environment: test | production
merchant_id: configured | missing
launch_state: planning | validating | ready | paused

## Current Scope
- Checkout flow currently in scope
- Recurring or one-time payment model
- In-scope countries and currencies

## Validation State
- Merchant readiness status
- Gateway tokenization validation status
- Real device and browser test status
- Fallback checkout status
- Idempotency validation status

## Risks
- High-impact open risks before release
- Monitoring or observability gaps
- Known incident patterns not yet fixed

## Notes
- Stable implementation choices
- Error signatures and proven fixes

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Integration in progress | Keep gathering context and validating changes |
| `complete` | Core flow validated | Focus on optimization and maintenance |
| `paused` | User paused work | Keep context read-only until resumed |
| `never_ask` | User wants no setup prompts | Do not request setup details unless user asks |

## File Templates

Create `~/google-pay/validation-log.md`:

```markdown
# Google Pay Validation Log

## YYYY-MM-DD
- Environment:
- Platform:
- Scenario:
- Result:
- Evidence:
- Follow-up:
```

Create `~/google-pay/incidents.md`:

```markdown
# Google Pay Incidents

## YYYY-MM-DD HH:MM
- Symptom:
- Scope:
- Root cause:
- Mitigation:
- Preventive action:
```

## Key Principles

- Keep persisted notes short and actionable.
- Store evidence links, not raw sensitive payloads.
- Update `last` whenever status changes.
