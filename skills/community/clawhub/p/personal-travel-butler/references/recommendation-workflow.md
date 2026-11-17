# Recommendation Workflow

Use this process for questions, recommendations, and itinerary planning.

## Retrieval Order

1. Read `preferences/` for enduring user constraints and taste.
2. Search `places/`, `guides/`, and `trips/` for relevant local entries.
3. Use `indexes/` only as a shortcut; verify important details from atomic entries.
4. If freshness matters, actively check external information and report the verification date.
5. Separate confirmed local knowledge from inferred or newly fetched facts.

## Recommendation Rules

- Prefer entries with strong evidence, high priority, recent verification, and fit to the user's constraints.
- Mention uncertainty when an entry lacks city, hours, coordinates, or current status.
- Do not over-optimize for ratings if the user's own notes indicate strong interest.
- Preserve the user's travel style: pace, budget, food preferences, reservation tolerance, and companion constraints.

## Itinerary Rules

- Group places by city, neighborhood, transit feasibility, opening hours, and meal timing.
- Avoid impossible routes and note where timing needs live verification.
- Include backup options when a must-go place has uncertain hours or reservation risk.
- Keep the plan editable: candidate lists are often better than a rigid schedule during early planning.

## Answer Format

For short recommendations:

```markdown
## Best Picks

- Place - why it fits. Local evidence: ...

## Needs Checking

- Hours/reservation/current status for ...
```

For trip plans:

```markdown
## Plan

Day 1:
- Morning:
- Lunch:
- Afternoon:
- Dinner:

## Why These

- 

## To Verify

- 
```
