# Setup — Productivity

## Philosophy

This skill should work from minute zero.

Do not make the user complete a productivity migration project before they can get help. Answer the immediate request first, then progressively turn repeated planning work into a trusted local system.

## On First Use

### Priority #1: Answer the Current Productivity Problem

If the user asks to plan, prioritize, review, or recover focus, help immediately.

Only propose setup when it will reduce future friction.

### Priority #2: Offer Lightweight Integration

Ask once, naturally:

> "Want me to set up a local productivity system so goals, projects, tasks, habits, and reviews stop living in random places?"

If yes, create `~/productivity/` and the baseline files.

If no, help anyway and mark integration as declined in `~/productivity/memory.md` only if the user wants memory enabled.

### Priority #3: Tune Activation Briefly

After wiring the default routing, ask one short follow-up:

> "I wired this to trigger for planning, prioritization, goals, projects, tasks, habits, reviews, and overload resets. Want to also trigger it for anything else?"

If the user names extra situations, update the routing snippet instead of inventing separate memory.

## Local Productivity Structure

When the user wants the system installed locally:

```bash
mkdir -p ~/productivity/{inbox,goals,projects,tasks,habits,planning,reviews,commitments,focus,routines,someday}
```

Then create:
- `~/productivity/memory.md` from `memory-template.md`
- `~/productivity/inbox/capture.md` from `system-template.md`
- `~/productivity/inbox/triage.md` from `system-template.md`
- `~/productivity/dashboard.md` from `system-template.md`
- `~/productivity/goals/active.md` from `system-template.md`
- `~/productivity/goals/someday.md` from `system-template.md`
- `~/productivity/projects/active.md` from `system-template.md`
- `~/productivity/projects/waiting.md` from `system-template.md`
- `~/productivity/tasks/next-actions.md` from `system-template.md`
- `~/productivity/tasks/this-week.md` from `system-template.md`
- `~/productivity/tasks/waiting.md` from `system-template.md`
- `~/productivity/tasks/done.md` from `system-template.md`
- `~/productivity/habits/active.md` from `system-template.md`
- `~/productivity/habits/friction.md` from `system-template.md`
- `~/productivity/planning/daily.md` from `system-template.md`
- `~/productivity/planning/weekly.md` from `system-template.md`
- `~/productivity/planning/focus-blocks.md` from `system-template.md`
- `~/productivity/reviews/weekly.md` from `system-template.md`
- `~/productivity/reviews/monthly.md` from `system-template.md`
- `~/productivity/commitments/promises.md` from `system-template.md`
- `~/productivity/commitments/delegated.md` from `system-template.md`
- `~/productivity/focus/sessions.md` from `system-template.md`
- `~/productivity/focus/distractions.md` from `system-template.md`
- `~/productivity/routines/morning.md` from `system-template.md`
- `~/productivity/routines/shutdown.md` from `system-template.md`
- `~/productivity/someday/ideas.md` from `system-template.md`

## AGENTS Routing Snippet

If the user wants stronger routing, suggest adding this to `~/workspace/AGENTS.md` or the equivalent workspace guidance:

```markdown
## Productivity Routing

Use `~/productivity/` as the source of truth for goals, projects, priorities, tasks, habits, focus, planning, reviews, and overload recovery.
When the user asks to plan work, reprioritize, review commitments, reset routines, or turn goals into execution, consult the smallest relevant productivity folder first.
Prefer updating one trusted system over scattering tasks across ad-hoc notes.
```

## SOUL Steering Snippet

If the user uses `SOUL.md`, suggest adding:

```markdown
**Productivity**
When work touches priorities, commitments, planning, or review, route through `~/productivity/`.
Keep one coherent productivity system: goals in `goals/`, projects in `projects/`, execution in `tasks/`, habits in `habits/`, planning in `planning/`, focus protection in `focus/`, resets in `reviews/`, routines in `routines/`, and parked ideas in `someday/`.
Use energy, constraints, and real context before prescribing routines.
```

## What to Save

Save to `~/productivity/memory.md` only with explicit approval:
- energy patterns that keep recurring
- stable planning preferences
- recurring constraints
- review cadence preferences
- system-level likes/dislikes

## Status Values

| Status | When to use |
|--------|-------------|
| `ongoing` | Default. Still learning how the user works. |
| `complete` | System is installed and the user actively uses it. |
| `paused` | User does not want more setup questions right now. |
| `never_ask` | User said stop prompting about setup or memory. |

## Golden Rule

If the skill becomes another productivity project instead of helping the user get clear and move, it failed.
