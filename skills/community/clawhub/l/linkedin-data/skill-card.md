## Description:

LinkedIn API integration with a single superagnt API key (Bearer token). Fetch company profiles, jobs, people, posts, and professional network insights. Use this skill when users want LinkedIn data for sales, recruiting, or enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales and recruiting agents use this skill to retrieve LinkedIn company, job, profile, post, and professional network data for enrichment and research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send a superagnt API key to its external API.

Mitigation: Use the integration only if you trust superagnt with the key, and keep the key in the designated environment variable rather than exposing it in logs or responses.

## Reference(s):

- [LinkedIn Data documentation](https://superagnt.com/r/ch-linkedin-data-docs)
- [LinkedIn Data API](https://api.superagnt.com/v1/data/linkedin)
- [LinkedIn MCP server](https://mcp.superagnt.com/mcp/linkedin)
- [ClawHub listing](https://clawhub.ai/superagnt/skills/linkedin-data)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [Structured JSON data and concise research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested LinkedIn data and API endpoint.]

## Skill Version(s):

2.0.14 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
