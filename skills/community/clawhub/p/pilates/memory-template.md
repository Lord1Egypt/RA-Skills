# Memory Template - Pilates (Session Planner, Form Coach, Progress Tracker)

Create `~/pilates/memory.md` with this structure:

```markdown
# Pilates Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Practice Profile
experience_level: beginner | returning | regular | instructor_led
equipment_context:
primary_goal:
secondary_goal:
session_length_preference:

## Safety Context
joint_or_pain_notes:
pregnancy_or_postpartum_notes:
bone_health_or_surgery_notes:
red_flags_to_watch:
stop_if:

## Current Plan
active_mode:
weekly_target:
current_focus:
primary_correction:
next_session_goal:

## Tracking Signals
practice_days_this_week:
control_rating:
breathing_quality:
energy_after_practice:

## Notes
- confirmed useful cues
- recurring form patterns
- what increases or lowers adherence

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Active support | Continue coaching, logging, and review cycles |
| `complete` | Stable routine | Use lightweight maintenance and periodic review |
| `paused` | User paused practice | Keep context read-only until resumed |
| `never_ask` | No setup prompts wanted | Do not ask setup questions unless requested |

## File Templates

Create `~/pilates/sessions/log.md`:

```markdown
# Pilates Session Log

## YYYY-MM-DD HH:MM
- Mode: start | session | repair | build | recover
- Duration:
- Session focus:
- Main cue:
- Control today: 1_to_5
- Pain or symptoms:
- Win from session:
- Next target:
```

Create `~/pilates/plans/current-plan.md`:

```markdown
# Current Pilates Plan

## Active Week
- Primary goal:
- Days planned:
- Session lengths:
- Main exercise focus:
- Recovery option:
- Skip or modify if:
```

Create `~/pilates/form/checkpoints.md`:

```markdown
# Pilates Form Checkpoints

## Current Corrections
- Pattern:
- What it looks like:
- Single correction cue:
- Easier drill:
- Recheck on:
```

Create `~/pilates/summaries/weekly-review.md`:

```markdown
# Weekly Pilates Review

## Week Ending YYYY-MM-DD
- Sessions completed:
- Most controlled exercise:
- Most common breakdown:
- Breathing trend:
- Symptoms or caution notes:
- Next-week focus:
```

Create `~/pilates/safety/modifications.md`:

```markdown
# Pilates Safety Modifications

## Approved Adjustments
- Situation:
- Keep:
- Reduce:
- Avoid:
- Escalate if:
```

## Key Principles

- Track only the minimum signals that improve the next practice decision.
- Update `last` whenever goals, safety context, or cadence changes.
- Keep one main correction active at a time unless the user explicitly wants a deeper review.
- Record stop signals clearly enough that future sessions respect them automatically.
