## Description:

Retrieves read-only Nike product prices, listed sizes, release calendar details, and review data across Nike storefronts for agent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve storefront-specific Nike product prices, sizes Nike lists, launch calendar information, and review summaries for analysis. It also supports comparisons across Nike storefronts when each result is kept with its market and retrieval date.

### Deployment Geography for Use:

Global; 62 Nike storefronts across 42 countries.

## Known Risks and Mitigations:

Risk: Using the skill sends API requests through Scavio and requires providing a Scavio API key.

Mitigation: Use the key only if you trust Scavio to receive these requests, and keep it in a secure environment variable or secret store rather than prompts or logs.

Risk: Security analysis is incomplete because some local references could not be resolved.

Mitigation: Review the referenced materials and current Scavio API documentation before deployment.

## Reference(s):

- [Scavio Nike API overview](https://scavio.dev/nike-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api)
- [Scavio Nike product API documentation](https://scavio.dev/docs/nike-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api)
- [Scavio Nike launch calendar API documentation](https://scavio.dev/docs/nike-releases?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api)
- [Scavio Nike reviews API documentation](https://scavio.dev/docs/nike-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=nike-api)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON with concise Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market-specific results include retrieval dates; listing endpoints return the first 24 product groups.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
