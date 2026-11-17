## Description:

Uses McDonald's MCP service to help users browse McDelivery menus, calculate prices, create and track orders, query nutrition information, and view promotional calendars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjn161](https://clawhub.ai/user/wjn161)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to place McDelivery orders, review saved addresses, configure default meals, receive nutrition-aware meal suggestions, and track order status. The workflow can create real orders and payment QR codes, so users should confirm sensitive actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a McDonald's token, saved addresses, local MCP configuration, and a real order/payment workflow.

Mitigation: Install only when the MCP endpoint is trusted, keep the token scoped and protected, and require explicit user confirmation before configuration changes, address creation, final order placement, and payment.

Risk: Command examples and helper flows pass user- or service-provided data through shell arguments.

Mitigation: Prefer structured argument passing that avoids shell interpolation, and review command examples before running them with real menu, address, order, or payment data.

Risk: Payment URLs are transformed into QR code targets.

Mitigation: Validate payment URLs against the expected McDonald's host before generating or scanning a QR code.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wjn161/skills/mcd-order-skill)
- [McDonald's MCP service endpoint](https://mcp.mcd.cn)
- [McDonald's developer portal](https://open.mcd.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown and text responses with JSON helper outputs, shell commands, configuration snippets, and optional payment QR image or ASCII output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and MCD_MCP_TOKEN; may read or update local skill and MCP configuration during setup.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
