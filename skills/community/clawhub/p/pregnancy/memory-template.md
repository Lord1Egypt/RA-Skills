# Memory Template - Pregnancy (Tracker, Journal, Triage, Visit Prep)

Create `~/pregnancy/memory.md` with this structure:

```markdown
# Pregnancy Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Pregnancy Context
gestational_week:
estimated_due_date:
care_context: routine | high_risk | unknown
care_team:

## Tracking Scope
core_modules:
optional_modules:
check_in_cadence:
summary_cadence:

## Active Priorities
priority_1:
priority_2:
priority_3:

## Alert Preferences
red_alert_action:
amber_alert_action:
local_emergency_number:

## Notes
- Confirmed patterns
- Open clinician questions
- Data quality reminders

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Active support | Continue tracking and summary cycles |
| `complete` | Stable routine | Keep lightweight maintenance and visit prep |
| `paused` | User paused workflow | Keep context read-only until resumed |
| `never_ask` | No setup prompts wanted | Do not ask setup questions unless requested |

## File Templates

Create `~/pregnancy/logs/daily-log.md`:

```markdown
# Pregnancy Daily Log

## YYYY-MM-DD
- Core: time | sleep_hours | hydration | energy_1_to_5 | mood_1_to_5
- Symptoms: symptom | severity_1_to_10 | duration | trigger | notes
- Vitals: metric | value | unit | context | repeat_value_if_needed
- Medications: medication | dose | time | adherence | side_effects
- Fetal movement: window | baseline_vs_today | concerns
- Appointments/tasks: item | due_date | status
```

Create `~/pregnancy/summaries/weekly.md`:

```markdown
# Pregnancy Weekly Summary

## Week Ending YYYY-MM-DD
- Gestational week:
- Overall status: green | amber | red
- Key trends:
- Out-of-range events:
- Open questions for clinician:
- Next-week focus:
```

Create `~/pregnancy/alerts/events.md`:

```markdown
# Pregnancy Alert Events

## YYYY-MM-DD HH:MM
- Alert level: red | amber
- Trigger:
- Observed data:
- Action taken:
- Outcome:
- Follow-up needed:
```

Create `~/pregnancy/summaries/visit-prep.md`:

```markdown
# Prenatal Visit Prep

## Next Appointment
- Date:
- Provider:
- Top concerns:
- Top 5 questions:
- Decision points:
- Data packet prepared: yes | no
```

## Key Principles

- Keep entries short, consistent, and timestamped.
- Separate observations from interpretations.
- Update `last` whenever scope, status, or priorities change.
- Keep emergency paths explicit in every alert event.
