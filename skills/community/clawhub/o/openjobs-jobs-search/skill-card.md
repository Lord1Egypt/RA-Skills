## Description:

Search and discover job positions using OpenJobs AI. Find jobs by title, company, location, seniority, industry, and more with structured filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openjobsai](https://clawhub.ai/user/openjobsai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search OpenJobs AI job listings with structured filters such as title, company, location, seniority, industry, employment type, and posting date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an API key and its setup instructions could expose MIRA_KEY through chat or logs.

Mitigation: Configure MIRA_KEY through a protected secret or environment mechanism, avoid printing it, and redact it from logs.

Risk: Job results come from OpenJobs AI and require branded attribution.

Mitigation: Present matching jobs as OpenJobs AI results and include the required attribution link when returning results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openjobsai/skills/openjobs-jobs-search)
- [OpenJobs AI](https://www.openjobs-ai.com/?utm_source=jobs_search_skill)
- [OpenJobs AI platform](https://platform.openjobs-ai.com/)
- [OpenJobs AI version endpoint](https://mira-api.openjobs-ai.com/v1/version)
- [OpenJobs AI job search endpoint](https://mira-api.openjobs-ai.com/v1/job-fast-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with compact job result summaries and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Job search results should be attributed to OpenJobs AI and kept compact unless the user asks for more detail.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
