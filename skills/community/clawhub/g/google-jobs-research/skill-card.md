## Description:

Searches Google's public careers site through Crawlora and retrieves job listings and individual posting details as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and researchers use this skill to find public Google Careers openings by role or location and inspect or track individual postings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill shares the Crawlora API key and Google job search queries with Crawlora.

Mitigation: Use it only if sharing those details with Crawlora is acceptable; keep the key in the environment and never hardcode or commit it.

Risk: Requests outside the documented public Google Careers endpoints may access unintended data.

Mitigation: Use the helper only for the documented public Google Careers search and job-detail endpoints.

## Reference(s):

- [Google Jobs Research on ClawHub](https://clawhub.ai/crawlora-org/skills/google-jobs-research)
- [Endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON job listings and posting details, with optional text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include descriptions, responsibilities, and qualifications; results are paginated.]

## Skill Version(s):

1.0.17 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
