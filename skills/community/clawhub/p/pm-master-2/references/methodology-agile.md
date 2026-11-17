# Methodology · Agile (Scrum / Kanban)

## Applicable Scenarios
Requirements uncertain, fast feedback needed, software products continuously evolving. Choose one framework: **Scrum** (time-boxed Sprints) or **Kanban** (flow first).

## A. Scrum Framework

### Ceremonies
| Ceremony | Frequency | Output |
|------|------|------|
| Sprint Planning | at the start of each Sprint | sprint_plan (committed backlog + goal) |
| Daily Standup | daily | blocker sync |
| Sprint Review | at the end of each Sprint | demonstrable increment, feedback |
| Sprint Retro | at the end of each Sprint | improvement items (retro template) |

### Core Artifacts (agile-specific templates)
- `templates/agile/product_backlog.md`: epics/features/user stories, priority, estimates
- `templates/agile/sprint_plan.md`: this Sprint's goal + committed items + task breakdown
- `templates/agile/definition_of_done.md`: Definition of Done (DoD) checklist
- `templates/agile/burndown.md`: burndown chart data + notes
- `templates/agile/retro.md`: retrospective template (went well / to improve / actions)

### Cadence
- Sprint length 1–4 weeks (default 2 weeks); fixed cadence, not arbitrarily extended.
- Kanban flow: WIP limited, Lead Time measured.

## B. Kanban Framework
- No fixed iterations; focus on **flow**: limit WIP, measure Lead Time / flow efficiency, class of service (CoS).
- Artifacts: Kanban board (can use `templates/agile/product_backlog.md` as the backlog pool) + `burndown.md` repurposed as a cumulative flow diagram.

## Key Metrics
- Velocity, Burn-down, Lead Time, WIP, flow efficiency (see `references/metrics.md`)

## Notes
- `framework` in `project.yaml` must be `scrum` or `kanban`, affecting template and ceremony selection.
- DoD is the quality red line; retrospective action items must be tracked to closure (into RAID issues).
- Agile does not mean no documentation: charter, RACI, and risks are still maintained per common/.
