<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Template: templates/sprint-planning.md

```markdown
# Sprint Planning — Sprint {N}

**Dates:** {start} → {end}
**Capacity:** {team-size} × {days} = {total person-days} (minus {leave/ceremonies} = {available})

## Sprint Goal
{One sentence: what this sprint achieves}

## Committed Work

| # | Ticket | Title | Size | Module | Assignee |
|---|--------|-------|:----:|--------|----------|
| 1 | {id} | {title} | {S/M/L/XL} | {module} | {person} |
| 2 | {id} | {title} | {size} | {module} | {person} |
| ... | ... | ... | ... | ... | ... |

**Total committed:** {sum of sizes} / {capacity}

## Stretch Goals (If Capacity Allows)
| Ticket | Title | Size |
|--------|-------|:----:|
| {id} | {title} | {size} |

## Dependencies
| Task | Depends On | Status |
|------|-----------|:------:|
| {task} | {dependency} | {ready/blocked} |

## Risks
| Risk | Impact | Mitigation |
|------|--------|-----------|
| {risk} | {impact} | {plan} |

## Ceremonies
| Ceremony | Date | Time |
|----------|------|------|
| Planning | {date} | {time} |
| Daily standup | Mon-Fri | {time} |
| Review | {date} | {time} |
| Retro | {date} | {time} |
```
