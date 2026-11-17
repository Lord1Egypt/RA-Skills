## Description:

Use Menlo Shopping MCP to find individual products or build curated shopping lists. Use when a user asks to shop, compare products, find gifts, assemble a setup, or get product recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t-khush](https://clawhub.ai/user/t-khush)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to search Amazon.com products, compare options, find gifts, and assemble curated shopping lists based on user constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a configured shopping MCP server for product searches and links.

Mitigation: Confirm the MCP server is acceptable before installation and review returned product details before use.

Risk: Product recommendations can be misleading if prices, ratings, availability, or URLs are missing or stale.

Mitigation: Use returned product facts as-is, avoid inventing missing details, and leave purchase decisions to the user.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text product recommendations with product links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses returned product prices, ratings, availability, and URLs as-is.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
