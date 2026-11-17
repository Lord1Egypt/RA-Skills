# Definition of Done (DoD) · {{ project.name }}

> Each area defines an acceptance checklist for "Done"; a work item must have all entries in its area checked off before it can be considered Done.

{{#each dod}}
## {{this.area}}

> Completion criteria for this area (all items must be checked before this dimension is considered Done):

{{#each this.checklist}}
- [ ] {{this}}
{{/each}}

{{/each}}

> Note: The DoD is a quality gate, not a workload metric; anything that does not meet it cannot be counted as a Sprint deliverable.
