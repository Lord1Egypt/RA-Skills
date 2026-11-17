## Description:

Search Mercari US and Japan for live and sold listings, inspect item details and Japan seller profiles, and browse categories, brands, US deals, and trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and resale researchers use the skill to retrieve Mercari US and Japan listings and sold prices, compare asking and sale prices, and review item or Japan seller details.

### Deployment Geography for Use:

Global (Mercari data covers the US and Japan)

## Known Risks and Mitigations:

Risk: API requests use SCAVIO_API_KEY to access api.scavio.dev.

Mitigation: Keep the key in a secret store or private environment variable, and avoid exposing it in logs or shared configuration.

Risk: The security review was partial because several local references could not be resolved.

Mitigation: Review the skill and its setup instructions before enabling it.

## Reference(s):

- [Mercari API search documentation](https://scavio.dev/docs/mercari-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api)
- [Mercari API on ClawHub](https://clawhub.ai/scavio-ai/skills/mercari-api)
- [Scavio Mercari API overview](https://scavio.dev/mercari-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercari-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON API responses with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses use the source marketplace's language and currency.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
