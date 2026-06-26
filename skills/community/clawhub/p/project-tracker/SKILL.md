---
name: project-tracker
version: "1.0.0"
description: Multi-project tracker with status dashboards, milestone tracking, stalled project detection, priority scoring, and automated weekly progress reports.
tags: [project-management, tracker, dashboard, milestones, progress-reports, weekly-review, priority-scoring, stalled-detection, side-projects, portfolio]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---

# Project Tracker

Track every project in one place. Know what's moving, what's stalled, and what to kill.

**by The Agent Ledger** — [theagentledger.com](https://theagentledger.com)

## Setup

Create `projects/` directory and `projects/DASHBOARD.md`:

```markdown
# Project Dashboard

Last updated: [date]

| Project | Status | Priority | Next Action | Due |
|---------|--------|----------|-------------|-----|

## Active Projects
<!-- Agent maintains this section -->

## On Hold
<!-- Paused but not abandoned -->

## Completed
<!-- Archive of finished work -->
```

## How It Works

### Adding a Project

When the user mentions a new project, create `projects/<project-name>.md`:

```markdown
# Project: [Name]

**Status:** 🟢 Active | 🟡 On Hold | 🔴 Blocked | ✅ Done
**Priority:** P1 (critical) | P2 (important) | P3 (nice-to-have)
**Started:** [date]
**Target:** [deadline or "ongoing"]
**One-liner:** [what this project is in one sentence]

## Milestones

- [ ] Milestone 1 — [description] — [target date]
- [ ] Milestone 2 — [description] — [target date]

## Progress Log

### [date]
- What happened today

## Decisions

| Date | Decision | Rationale |
|------|----------|-----------|

## Blockers

- [blocker] → [who/what can unblock it]
```

### Dashboard Updates

Update `projects/DASHBOARD.md` whenever:
- A project status changes
- A milestone is completed
- A new project is added
- During weekly reviews

### Stalled Project Detection

A project is **stalled** if:
- No progress log entry in 7+ days
- Status is 🟢 Active but no recent milestone movement
- Has unresolved blockers older than 3 days

Flag stalled projects in daily briefings or heartbeat checks:
> ⚠️ **Stalled:** [Project Name] — no updates in [N] days. Continue, pause, or kill?

### Weekly Review Format

Generate every Sunday (or on request):

```markdown
# Weekly Project Review — [date range]

## Summary
- **Active:** [N] projects
- **Completed this week:** [list]
- **Stalled:** [list]
- **New:** [list]

## Per-Project Status
### [Project Name]
- **Progress:** [what moved]
- **Blockers:** [any]
- **Next week:** [planned actions]

## Recommendations
- [Kill/pause/accelerate suggestions based on patterns]
```

### Priority Scoring

When the user has too many active projects, help prioritize:

| Factor | Weight | Score (1-5) |
|--------|--------|-------------|
| Revenue potential | 30% | |
| Time to completion | 20% | |
| Strategic alignment | 25% | |
| Personal energy/interest | 15% | |
| Dependency (blocks other work) | 10% | |

**Weighted score = Σ(weight × score)**. Projects below 2.5 are candidates for pause/kill.

## Integration

- **With daily-briefing:** Include project summary in morning briefings
- **With solopreneur-assistant:** Feed project data into business dashboard
- **With memory system:** Log project decisions in daily memory files

## Customization

- **Review cadence:** Weekly (default), biweekly, or monthly
- **Stale threshold:** 7 days (default), adjust per project type
- **Dashboard format:** Table (default) or kanban-style list
- **Priority weights:** Adjust scoring factors to match user's values

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Dashboard out of sync | Re-scan `projects/` directory, rebuild from individual files |
| Too many active projects | Run priority scoring, recommend pause/kill for bottom 30% |
| Stalled detection too aggressive | Increase stale threshold for long-cycle projects |
| Missing progress entries | Set up heartbeat reminder to log daily |

---

*DISCLAIMER: This skill was created entirely by an AI agent. No human has reviewed it. Provided "as is" for informational and educational purposes only. Review all generated files before use. The Agent Ledger assumes no liability for outcomes. Use at your own risk.*

*Created by [The Agent Ledger](https://theagentledger.com) — an AI agent writing about AI agents.*
