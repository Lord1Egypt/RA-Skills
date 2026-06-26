# Migration Guide - Productivity

## v1.0.4 Productivity Operating System Update

This update keeps the same home folder, `~/productivity/`, but changes the recommended structure from a light memory-only setup into a fuller operating system with named folders for inbox, goals, projects, tasks, habits, planning, reviews, commitments, focus, routines, and someday items.

### Before

- `~/productivity/memory.md`
- optional loose notes such as `~/productivity/<topic>.md`
- older installs may also have copied context guides in a flat layout

### After

- `~/productivity/memory.md`
- `~/productivity/inbox/`
- `~/productivity/dashboard.md`
- `~/productivity/goals/`
- `~/productivity/projects/`
- `~/productivity/tasks/`
- `~/productivity/habits/`
- `~/productivity/planning/`
- `~/productivity/reviews/`
- `~/productivity/commitments/`
- `~/productivity/focus/`
- `~/productivity/routines/`
- `~/productivity/someday/`
- any old loose notes preserved until the user chooses to merge or archive them

## Safe Migration

1. Check whether `~/productivity/` already exists.

2. If it exists, keep `memory.md` exactly as it is.

3. Create the new files without deleting the old ones:

```bash
mkdir -p ~/productivity/{inbox,goals,projects,tasks,habits,planning,reviews,commitments,focus,routines,someday}
touch ~/productivity/inbox/capture.md
touch ~/productivity/inbox/triage.md
touch ~/productivity/dashboard.md
touch ~/productivity/goals/active.md
touch ~/productivity/goals/someday.md
touch ~/productivity/projects/active.md
touch ~/productivity/projects/waiting.md
touch ~/productivity/tasks/next-actions.md
touch ~/productivity/tasks/this-week.md
touch ~/productivity/tasks/waiting.md
touch ~/productivity/tasks/done.md
touch ~/productivity/habits/active.md
touch ~/productivity/habits/friction.md
touch ~/productivity/planning/daily.md
touch ~/productivity/planning/weekly.md
touch ~/productivity/planning/focus-blocks.md
touch ~/productivity/reviews/weekly.md
touch ~/productivity/reviews/monthly.md
touch ~/productivity/commitments/promises.md
touch ~/productivity/commitments/delegated.md
touch ~/productivity/focus/sessions.md
touch ~/productivity/focus/distractions.md
touch ~/productivity/routines/morning.md
touch ~/productivity/routines/shutdown.md
touch ~/productivity/someday/ideas.md
```

4. If the user has older free-form topic files in `~/productivity/`, map them gradually:
   - current priorities -> `dashboard.md`
   - goals -> `goals/active.md`
   - projects -> `projects/active.md`
   - actionable work -> `tasks/next-actions.md`
   - habits and routines -> `habits/active.md`
   - focus notes -> `focus/sessions.md` or `focus/distractions.md`
   - weekly reset notes -> `reviews/weekly.md`
   - parked ideas -> `someday/ideas.md`

5. If older copied guide files exist in a flat layout, preserve them as legacy references. Do not delete or rename them automatically.

6. Only clean up legacy files after the user confirms the new structure is working.

## Post-Migration Check

- `memory.md` still contains the user's saved preferences
- active priorities are visible in `dashboard.md`
- next actions live in `tasks/next-actions.md`
- review cadence is captured in `reviews/weekly.md`
- no legacy file was deleted without explicit user approval
