## Description:

Place McDonald's China delivery orders through the official MCP server at https://mcp.mcd.cn using a Bearer MCP token over Streamable HTTP / JSON-RPC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielliao](https://clawhub.ai/user/danielliao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to browse McDonald's China delivery addresses, menus, meal details, coupons, price totals, and order status, then create delivery orders only after user confirmation. Developers can also use the included client and RPC helper when wiring the MCP service into agent clients.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Bearer MCP tokens could be sent to a non-McDonald's endpoint if MCD_MCP_URL or base_url is changed.

Mitigation: Use a dedicated, revocable McDonald's MCP token and verify the endpoint remains https://mcp.mcd.cn before use.

Risk: The skill can perform account-changing actions, including order creation, coupon or points actions, and cancellation.

Mitigation: Require explicit user confirmation before order creation, coupon or points actions, or cancellation.

Risk: Configuration output can reveal service configuration and a masked token prefix.

Mitigation: Avoid exposing mcdonalds_get_config output in user-visible contexts unless it is necessary for troubleshooting.

## Reference(s):

- [McDonald's MCP quick reference](artifact/references/api.md)
- [ClawHub skill release](https://clawhub.ai/danielliao/skills/mcdonalds-mcp-order-lite)
- [ClawHub publisher profile](https://clawhub.ai/user/danielliao)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, Python helper code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live MCP responses for account, address, menu, price, coupon, and order information.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
