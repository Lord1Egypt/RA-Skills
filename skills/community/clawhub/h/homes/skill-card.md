## Description:

Look up real-estate listings, property details, price/tax history, market reports, saved homes, and photo galleries on homes.com via MCP. Triggers on phrases like "find homes on homes.com in", "homes.com property details for", "what does homes.com say about", "homes.com price history for", or any request involving homes.com properties, prices, history, or photos. Requires homes-mcp installed and the ContextMint Bridge extension active (see Setup below).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to search and compare homes.com listings, retrieve property details and price or tax histories, review saved homes and market reports, and calculate mortgage affordability or rent-versus-buy scenarios.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill uses third-party software through a signed-in homes.com browser session that may expose saved homes and searches.

Mitigation: Prefer a reviewed, pinned package version, verify the bridge extension release, approve only needed access, and revoke access when finished.

## Reference(s):

- [homes-mcp package](https://www.npmjs.com/package/homes-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge privacy documentation](https://github.com/nullnet-app/contextmint-bridge/blob/main/docs/PRIVACY.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Tables, URLs]

**Output Format:** [Structured property records, histories, comparisons, market summaries, photo links, and calculator breakdowns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compact responses omit image URLs where supported; saved homes and searches require a signed-in homes.com tab, and rent-versus-buy calculations require a supplied monthly rent.]

## Skill Version(s):

2.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
