# Memory Template - Mindfulness (Tracker, Logger, Guided Practice)

Create `~/mindfulness/memory.md` with this structure:

```markdown
# Mindfulness Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Current Mode
mode: logger | guided | builder | reset
primary_goal:
secondary_goal:

## Practice Baseline
experience_level: beginner | intermediate | advanced
typical_session_length_min:
best_time_windows:
main_triggers_for_practice:

## Active Plan
plan_start:
weekly_target_sessions:
current_technique_focus:
next_check_in:

## Constraints and Preferences
hard_limits:
preferred_tone:
what_to_avoid:

## Notes
- Confirmed patterns
- Effective techniques
- Friction points and adjustments

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Active support | Keep improving routine fit and recommendations |
| `complete` | Stable routine | Maintain with lightweight check-ins |
| `paused` | User paused support | Keep context read-only until resumed |
| `never_ask` | No setup prompts wanted | Do not ask setup questions unless requested |

## File Templates

Create `~/mindfulness/logs/sessions.md`:

```markdown
# Mindfulness Session Log

## YYYY-MM-DD
- Session: HH:MM | mode | duration_min | technique | pre_state_1_to_10 | post_state_1_to_10 | note
- Session: HH:MM | mode | duration_min | technique | pre_state_1_to_10 | post_state_1_to_10 | note

### Daily Snapshot
- total_sessions:
- total_minutes:
- best_window:
- friction_point:
```

Create `~/mindfulness/plans/current.md`:

```markdown
# Mindfulness Current Plan

## Mode
- logger | guided | builder | reset

## Weekly Targets
- sessions_target:
- minutes_target:
- consistency_target:

## Focus
- Primary technique:
- Backup technique:
- Trigger-based quick reset:

## Review
- Next review date:
- Adjustment rule:
```

Create `~/mindfulness/check-ins/weekly.md`:

```markdown
# Mindfulness Weekly Check-Ins

## Week Ending YYYY-MM-DD
- Sessions completed:
- Minutes practiced:
- Average pre state:
- Average post state:
- Most effective technique:
- Main friction:
- Next-week single focus:
```

## Key Principles

- Keep logs short and consistent.
- Track behavior and outcomes, not personal judgments.
- Update `last` whenever mode, goals, or cadence changes.
