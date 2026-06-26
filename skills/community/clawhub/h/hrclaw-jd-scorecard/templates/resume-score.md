# Resume Score

## Mode
- Resume scoring against a scorecard

## Candidate Profile
- Name: {{candidate_profile.name}}
- Location: {{candidate_profile.location}}
- Years of Experience: {{candidate_profile.years_experience}}
- Education: {{candidate_profile.education_level}}
- Current Title: {{candidate_profile.current_title}}
- Current Company: {{candidate_profile.current_company}}

## Score
- Scorecard: {{scorecard_name}}
- Decision: {{decision}}
- Total Score: {{total_score}}
- Hard Filter Pass: {{hard_filter_pass}}

## Dimension Scores
{{#each dimension_scores}}
- {{@key}}: {{this}}
{{/each}}

## Reasons
### Hard Filter Fail Reasons
{{#each hard_filter_fail_reasons}}
- {{this}}
{{/each}}

### Review Reasons
{{#each review_reasons}}
- {{this}}
{{/each}}

## Signals
### Matched Terms
{{#each matched_terms}}
- {{this}}
{{/each}}

### Missing Terms
{{#each missing_terms}}
- {{this}}
{{/each}}

### Blocked Terms
{{#each blocked_terms}}
- {{this}}
{{/each}}

## Evidence
- Resume excerpt: {{evidence.resume_excerpt}}

## Summary
{{summary}}

## Next Steps
{{#each next_steps}}
- {{this}}
{{/each}}
