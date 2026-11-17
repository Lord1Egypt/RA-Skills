## Description:

Use when the user wants to connect to, test, or use the McDonalds service at mcp.mcd.cn, including checking authentication, probing MCP endpoints, listing tools, or calling McDonalds MCP tools through a reusable local CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1052666](https://clawhub.ai/user/1052666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to the McDonalds MCP service, verify credentials and endpoint health, list available tools, and invoke selected MCP tools through a local CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real McDonald's MCP token may authorize live account or ordering actions.

Mitigation: Use a token only after review, keep it in the environment or command line as intended, and run account-changing tools only when the user explicitly requests those changes.

Risk: A custom MCP URL could receive the bearer token.

Mitigation: Prefer the default https://mcp.mcd.cn endpoint and avoid overriding MCDONALDS_MCP_URL unless the endpoint is trusted.

Risk: Some available tools can create orders, create delivery addresses, or bind coupons.

Mitigation: Treat create-order, delivery-create-address, auto-bind-coupons, and mall-create-order as live-action tools requiring explicit confirmation before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1052666/skills/mcdonalds-skill)
- [McDonalds MCP service endpoint](https://mcp.mcd.cn)
- [McDonalds MCP credential portal](https://open.mcd.cn/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can print JSON responses and optionally write smoke-test reports to a JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
