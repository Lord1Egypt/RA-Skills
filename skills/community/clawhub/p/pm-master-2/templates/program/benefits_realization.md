# Benefits Realization Plan · {{ project.name }}

> Tracks the definition, target, baseline, owner, and realization progress of the program's expected benefits, ensuring ROI is measurable and accountable.

## Benefits Register
| ID | Description | Metric | Target | Baseline | Realized | Owner | Planned Realization Date | Status |
|----|------|---------|------|------|--------|--------|------------|------|
{{#each benefits}}
| {{this.id}} | {{this.description}} | {{this.metric}} | {{this.target}} | {{this.baseline}} | {{this.realized}} | {{this.owner}} | {{this.realization_date}} | {{this.status}} |
{{/each}}

## Notes
- **Metric**: the specific indicator and definition for quantifying the benefit.
- **Baseline**: the starting measurement before benefit realization, used to compute net gain.
- **Realized**: the value achieved/confirmed to date.
- **Owner**: the specific role accountable for the benefit (required; enforced by consistency check).
- **Planned Realization Date**: the expected date the benefit lands.
- **Status**: Not Started / In Progress / Achieved / Closed.

> Tip: Each benefit must have a clear owner; once achieved, the governance role signs off to close the loop (see change_log).
