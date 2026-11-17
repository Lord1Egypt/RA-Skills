## Description:

Searches public Indeed job postings, suggests locations, and retrieves individual job details through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and recruiters use this skill to find Indeed postings by keyword and location, refine locations, and retrieve details for specific jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indeed search terms, locations, job keys, and the Crawlora API key are sent to Crawlora.

Mitigation: Use the skill only when this disclosure is acceptable; keep the API key in CRAWLORA_API_KEY and never hardcode or commit it.

## Reference(s):

- [Indeed endpoint reference](reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/indeed-research)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON job results and Markdown guidance with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are paginated; a job key retrieves an individual listing.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
