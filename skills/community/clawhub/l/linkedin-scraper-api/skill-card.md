## Description:

Looks up LinkedIn people and companies, their posts, job listings, and post comments through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for B2B prospecting, recruiting, and market research using public LinkedIn profiles, company information, posts, and job listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested LinkedIn identifiers and searches are sent to Scavio.

Mitigation: Use only for approved lookups and avoid inferring private details from public profiles.

Risk: The Scavio API key grants access to credit-billed calls.

Mitigation: Store SCAVIO_API_KEY in environment or secret storage and cap paginated calls before making requests.

## Reference(s):

- [Scavio LinkedIn API documentation](https://scavio.dev/docs/linkedin-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-scraper-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-scraper-api)
- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/linkedin-scraper-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API lookups return structured JSON; paginated results may require multiple credit-billed calls.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
