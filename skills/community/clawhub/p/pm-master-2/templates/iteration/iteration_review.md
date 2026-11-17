# Iteration Review · {{ project.name }}

> At iteration end, demonstrate results to stakeholders, explain deviations, and pass inputs to the next iteration.

- **Iteration Number**: {{ iteration.num }}

## Completed
{{#each review.completed}}
- {{this}}
{{/each}}

## Deviation
{{ review.deviation }}

## Demo Conclusion
{{ review.demo }}

## Next Iteration Input
{{#each review.next_input}}
- {{this}}
{{/each}}

> Tip: The deviation explanation should relate to root cause, not just describe the symptom.
