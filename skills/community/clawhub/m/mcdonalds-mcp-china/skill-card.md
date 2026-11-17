## Description:

Guides agents through McDonald's China MCP ordering workflows, including store and menu lookup, coupons, delivery and pickup orders, group meals, nutrition checks, and points redemption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meteorsliu](https://clawhub.ai/user/meteorsliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users in mainland China use this skill through an agent to browse McDonald's menus, apply coupons, calculate prices, place delivery or pickup orders, and redeem membership points. The skill also helps configure the McDonald's China MCP server with a user-provided token.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The MCP token is account-linked and could enable actions on the user's McDonald's account if exposed.

Mitigation: Treat the token like a password, keep it out of shared chats and logs, restrict configuration files that store it, and revoke or rotate it if exposed.

Risk: Paid orders or points-redemption orders could be created with incorrect items, prices, coupons, store details, or addresses.

Mitigation: Calculate the price and show order details for explicit user confirmation before creating paid or points-redemption orders.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/meteorsliu/skills/mcdonalds-mcp-china)
- [McDonald's China MCP Documentation](https://open.mcd.cn/mcp/doc)
- [McDonald's China MCP Portal](https://open.mcd.cn/mcp)
- [McDonald's China MCP Server](https://mcp.mcd.cn)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown guidance with command snippets, JSON configuration examples, and MCP tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided McDonald's China MCP token and user confirmation before paid or points-redemption orders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
