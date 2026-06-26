# Setup — PD (Personal Development System)

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

**文件夹结构**：

```
~/productivity/
├── memory.md
├── dashboard.md
├── inbox/
│   ├── capture.md
│   └── triage.md
├── commitments/0_dream/
│   └── ideas.md              # 梦想/探索方向（不承诺）
├── commitments/1_intent/
│   └── active.md             # 90-Day Outcome Goals
├── commitments/2_queued/
│   └── active.md             # In-flight projects
├── commitments/3_committed/
│   ├── next-actions.md       # Concrete next steps
│   ├── this-week.md          # This week's commitments
│   └── waiting.md            # Waiting-for items
├── commitments/4_done/
│   └── achievements.md       # Completed items worth keeping
├── commitments/5_archived/
│   ├── waiting-projects.md   # Blocked/delegated projects
│   └── waiting-tasks.md      # Blocked tasks
├── habits/
│   ├── active.md
│   └── friction.md
├── reviews/                    ← 统一复盘容器
│   ├── daily/                 # 日复盘（YYYY-MM-DD.md）
│   ├── weekly/                # 周复盘（YYYY-Wnn.md）+ template.md
│   └── monthly/               # 月复盘（YYYY-MM.md）+ template.md
├── commitments/
│   ├── promises.md
│   └── delegated.md
├── focus/
│   ├── sessions.md
│   └── distractions.md
├── routines/
│   ├── morning.md
│   └── shutdown.md
└── someday/
    └── ideas.md
```

**注意**：`planning/`、`goals/someday.md`、`goals/`、`projects/`、`tasks/`、`someday/` 已废弃（v2.3.0 前旧版），不要创建。

Then create the baseline files from `system-template.md`:
- `~/productivity/memory.md`
- `~/productivity/inbox/capture.md`
- `~/productivity/inbox/triage.md`
- `~/productivity/dashboard.md`
- `~/productivity/commitments/0_dream/ideas.md`
- `~/productivity/commitments/1_intent/active.md`
- `~/productivity/commitments/2_queued/active.md`
- `~/productivity/commitments/3_committed/next-actions.md`
- `~/productivity/commitments/3_committed/this-week.md`
- `~/productivity/commitments/3_committed/waiting.md`
- `~/productivity/commitments/4_done/achievements.md`
- `~/productivity/commitments/5_archived/waiting-projects.md`
- `~/productivity/commitments/5_archived/waiting-tasks.md`
- `~/productivity/habits/active.md`
- `~/productivity/habits/friction.md`
- `~/productivity/reviews/daily/`（目录，日志文件名格式 YYYY-MM-DD.md）
- `~/productivity/reviews/weekly/template.md`
- `~/productivity/reviews/monthly/template.md`
- `~/productivity/commitments/promises.md`
- `~/productivity/commitments/delegated.md`
- `~/productivity/focus/sessions.md`
- `~/productivity/focus/distractions.md`
- `~/productivity/routines/morning.md`
- `~/productivity/routines/shutdown.md`
- `~/productivity/someday/ideas.md`

## AGENTS Routing Snippet

If the user wants stronger routing, suggest adding this to `~/workspace/AGENTS.md` or the equivalent workspace guidance:

```markdown
## Productivity Routing

Use `~/productivity/` as the source of truth for goals, projects, priorities, tasks, habits, focus, and reviews.
When the user asks to plan work, reprioritize, review commitments, reset routines, or turn goals into execution, consult the smallest relevant productivity folder first.
Prefer updating one trusted system over scattering tasks across ad-hoc notes.
```

## SOUL Steering Snippet

If the user uses `SOUL.md`, suggest adding:

```markdown
**Productivity**
When work touches priorities, commitments, planning, or review, route through `~/productivity/`.
Keep one coherent productivity system: intent hierarchy via 承诺阶梯（0_dream→1_intent→2_queued→3_committed→4_done→5_archived），habits in `habits/`，reviews in `reviews/daily/`/`reviews/weekly/`/`reviews/monthly/`，focus protection in `focus/`，routines in `routines/`。
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

| Status      | When to use                                        |
| ----------- | -------------------------------------------------- |
| `ongoing`   | Default. Still learning how the user works.        |
| `complete`  | System is installed and the user actively uses it. |
| `paused`    | User does not want more setup questions right now. |
| `never_ask` | User said stop prompting about setup or memory.    |
|             |                                                    |

## Golden Rule

If the skill becomes another productivity project instead of helping the user get clear and move, it failed.
