## Description:

Autonomous e-commerce storefront operations, store inventory curation, collectible valuations, and order fulfillment via Stockpile MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casualbrooks](https://clawhub.ai/user/casualbrooks)

### License/Terms of Use:

MIT

## Use Case:

External merchants and agent developers use Stockpile to manage storefront inventory, route customer inquiries, maintain listings, fulfill orders, and review collectible appraisals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports that consequential store actions may bypass the documented approval boundary, with billing, appraisal, and message-routing capabilities also flagged.

Mitigation: Review the approval boundary and these behaviors before use; require explicit user confirmation for inventory changes, message routing, paid upgrades, and order fulfillment, and independently assess appraisal results.

Risk: ClawScan reports unpinned install sources and partial scan coverage.

Mitigation: Use a verified, pinned package or image release and check exact dependency versions against the reported advisories.

## Reference(s):

- [Stockpile Market](https://stockpile.market)
- [Stockpile agent documentation](https://stockpile.market/agents)
- [ClawHub release](https://clawhub.ai/casualbrooks/skills/mcp-stockpile)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON-formatted MCP tool responses and text results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool-dependent results covering stores, inventory, orders, routing, and appraisals.]

## Skill Version(s):

2.4.0 (source: SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
