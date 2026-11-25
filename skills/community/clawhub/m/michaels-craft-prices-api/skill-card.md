## Description:

Looks up Michaels product prices, details, and reported store stock in the United States and Canada through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping agents use the skill to retrieve Michaels catalog details, prices, promotions, product variants, online availability, nearby store stock, and store information. It supports shopping research for US and Canadian storefronts but does not place orders.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: Lookup requests and location details are sent to Scavio, and use requires a Scavio API key.

Mitigation: Provide only the ZIP or postal code needed for the lookup, consider whether Scavio's handling of the request is acceptable, and keep SCAVIO_API_KEY in an environment variable or secret store.

## Reference(s):

- [Scavio Michaels API overview](https://scavio.dev/michaels-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api)
- [Michaels API endpoint documentation](https://scavio.dev/docs/michaels-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=michaels-craft-prices-api)
- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/michaels-craft-prices-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON lookup results with concise human-readable summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live product and store lookup data; prices and reported availability may change between requests.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
