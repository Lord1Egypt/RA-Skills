## Description:

Resolve a company name to a Glassdoor employer ID, then retrieve its profile, ratings, up to three reviews, and salary percentiles by job title.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to research employers by retrieving company ratings, a limited set of employee reviews, and job-title salary estimates for compensation or employer-brand comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Scavio and API calls consume credits; company-search pricing may differ from the skill's stated cost.

Mitigation: Keep the API key out of source code, set a query budget, and check Scavio's current pricing documentation before use.

Risk: Employee reviews may contain identifying details, and a response includes at most three reviews.

Mitigation: Summarize reviews without identifying their authors, and use aggregate ratings rather than a few reviews to characterize employee sentiment.

## Reference(s):

- [Scavio Glassdoor API documentation](https://scavio.dev/docs/glassdoor-companies?utm_source=agent-skills&utm_medium=skill&utm_campaign=glassdoor-salary-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=glassdoor-salary-data)
- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/glassdoor-salary-data)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON data with employer profiles, ratings, reviews, and salary estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review results are limited to three per response; salary results are paginated by ten job titles.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
