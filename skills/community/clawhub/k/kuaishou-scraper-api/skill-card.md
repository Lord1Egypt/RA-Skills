## Description:

Guides agents in retrieving Kuaishou China profiles, posts, videos, comments, live status, hashtag feeds, leaderboards, and search results as structured data through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to guide Kuaishou China creator and trend research, including profile lookups, video and comment retrieval, and search through Scavio's API.

### Deployment Geography for Use:

Global; data coverage is limited to Kuaishou China, not Kwai international.

## Known Risks and Mitigations:

Risk: Exposing the Scavio API key in shared files or logs.

Mitigation: Store SCAVIO_API_KEY in an environment variable or secret store and keep it out of source control.

Risk: Repeated searches or batch calls can consume credits unexpectedly.

Mitigation: Review per-endpoint costs before calling, limit pagination and batch requests, and check reported credits used.

Risk: Lookup requests may disclose unnecessary identifiers to a third-party API provider.

Mitigation: Use Scavio only when its third-party data handling is acceptable and send only the identifiers needed for the lookup.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/kuaishou-scraper-api)
- [Scavio Kuaishou API documentation](https://scavio.dev/docs/kuaishou-profile?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=kuaishou-scraper-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance and examples; API results are structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API results can include pagination cursors and credits used; an SCAVIO_API_KEY is required for requests.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
