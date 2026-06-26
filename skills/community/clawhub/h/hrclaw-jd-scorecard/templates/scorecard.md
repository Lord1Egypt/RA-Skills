# {{role_title}} Scorecard

## Summary
{{summary}}

## Filters
- Location: {{filters.location}}
- Minimum years: {{filters.years_min}}
- Minimum education: {{filters.education_min}}

## Must Have
{{#each must_have}}
- {{this}}
{{/each}}

## Nice to Have
{{#each nice_to_have}}
- {{this}}
{{/each}}

## Exclude
{{#each exclude}}
- {{this}}
{{/each}}

## Weights
| Dimension | Weight |
| --- | ---: |
| Must have | {{weights.must_have}} |
| Nice to have | {{weights.nice_to_have}} |
| Title match | {{weights.title_match}} |
| Industry match | {{weights.industry_match}} |
| Experience | {{weights.experience}} |
| Education | {{weights.education}} |
| Location | {{weights.location}} |

## Thresholds
- Recommend: {{thresholds.recommend_min}}
- Review: {{thresholds.review_min}}

## Interview Questions
{{#each interview_questions}}
- {{this}}
{{/each}}

## Red Flags
{{#each red_flags}}
- {{this}}
{{/each}}

## Assumptions
{{#each assumptions}}
- {{this}}
{{/each}}

## Next Steps
{{#each next_steps}}
- {{this}}
{{/each}}
