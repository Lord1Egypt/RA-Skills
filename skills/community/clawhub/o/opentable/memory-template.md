# Memory Template - OpenTable

Create `~/opentable/memory.md` with this structure:

```markdown
# OpenTable Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Business Snapshot
venue_scope: single | multi
service_model: casual | upscale | mixed
primary_goal: occupancy | yield | no_show_reduction | guest_experience
planning_window: weekly

## Current Strategy
- Active availability strategy by daypart
- Pacing controls currently in place
- Cancellation and reminder policy currently used

## Metrics Baseline
- Covers seated
- No-show rate
- Average booking lead time
- Peak window conversion
- Waitlist conversion

## Open Risks
- Capacity risks for upcoming peaks
- Messaging or policy friction creating drop-off
- Data quality gaps that block decisions

## Notes
- Confirmed decisions
- Rejected experiments and why
- Follow-up actions with owner and due date

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Active optimization cycle | Keep gathering signals and iterating |
| `complete` | Current objective met | Shift to monitoring and next target |
| `paused` | User paused optimization | Keep context read-only until resumed |
| `never_ask` | User wants no setup prompts | Avoid setup questions unless user asks |

## File Templates

Create `~/opentable/reservation-log.md`:

```markdown
# OpenTable Reservation Log

## YYYY-MM-DD
- Goal:
- Change made:
- Time window:
- Result:
- Keep or rollback:
```

Create `~/opentable/incidents.md`:

```markdown
# OpenTable Incidents

## YYYY-MM-DD HH:MM
- Symptom:
- Guest impact:
- Root cause:
- Mitigation:
- Preventive action:
```

## Key Principles

- Keep notes concise and decision-oriented.
- Store trends and outcomes, not raw guest personal data.
- Update `last` whenever strategy or status changes.
