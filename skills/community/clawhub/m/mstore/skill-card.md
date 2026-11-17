## Description:

McDonald's China (mstore) helps agents query and claim McDonald's China coupons, check points, view campaigns, inspect menu and nutrition data, and perform delivery-ordering workflows through McDonald's China MCP services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chandler0714](https://clawhub.ai/user/chandler0714)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to access McDonald's China account workflows from an agent, including coupon management, points balance and redemption, campaign lookup, menu and nutrition lookup, and delivery order creation or tracking.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The setup flow can store a McDonald's China account token in plaintext shell profiles.

Mitigation: Prefer a session-only environment variable or protected credential storage, and avoid running the setup script unless plaintext profile storage is acceptable.

Risk: The skill can perform account-changing actions such as coupon claims, points redemption, address creation, and food ordering.

Mitigation: Require manual confirmation before any action that changes account state, spends points, creates an address, or places an order.

Risk: The workflow depends on an external CLI and McDonald's China MCP services.

Mitigation: Install the CLI only from a trusted source and version, and review service responses before acting on them.

## Reference(s):

- [McDonald's China MCP API Reference](references/api.md)
- [McDonald's China MCP token console](https://open.mcd.cn/mcp)
- [McDonald's China MCP server](https://mcp.mcd.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and CLI outputs that may be plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a McDonald's China MCP token; account-changing actions should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
