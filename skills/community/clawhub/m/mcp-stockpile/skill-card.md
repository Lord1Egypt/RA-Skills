## Description:

Enables agents to manage Stockpile storefronts, inventory, appraisals, customer inquiries, and order fulfillment through MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casualbrooks](https://clawhub.ai/user/casualbrooks)

### License/Terms of Use:

MIT

## Use Case:

Store operators and developers use this skill to let agents search products, manage storefronts and inventory, appraise collectibles, and handle orders through Stockpile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent access to live storefront, inventory, checkout, fulfillment, and message-routing actions can change commerce operations without adequate scoping or confirmation.

Mitigation: Review before using a production account; use a least-privilege API key and trial the skill on a non-production or low-risk store.

Risk: Inventory deletion, batch listing, checkout creation, fulfillment, message routing, and automated sweeps can have consequential effects.

Mitigation: Require human approval for these actions and pin the package version when the runner supports it.

## Reference(s):

- [Stockpile Market](https://stockpile.market)
- [Stockpile Agent Hub and API keys](https://stockpile.market/agents?tab=api)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [Text, Guidance, API calls]

**Output Format:** [Text and structured MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require a Stockpile API key for authenticated account operations.]

## Skill Version(s):

2.0.1 (source: skill frontmatter, pyproject.toml, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
