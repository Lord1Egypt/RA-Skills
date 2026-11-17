## Description:

Connect an AI agent to a Mobazha store via MCP (Model Context Protocol) so the agent can manage store products, orders, and settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengzie](https://clawhub.ai/user/fengzie)

### License/Terms of Use:

MIT-0

## Use Case:

Store owners, operators, and developers use this skill to connect an AI agent to a Mobazha store over MCP for store administration tasks such as product, order, message, discount, profile, notification, search, and payment-related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an AI agent to high-impact store administration controls.

Mitigation: Use it only after explicit consent, limit token scopes to the required store actions, and review proposed destructive or financial changes before execution.

Risk: Bearer tokens can be exposed through committed MCP configuration files, project files, logs, or shell history.

Mitigation: Store tokens in environment variables or a secrets manager, keep token-bearing config files out of source control, and revoke or regenerate tokens after suspected exposure.

Risk: Remote VPS or tunneled connections can expose store access if transport or SSH access is too broad.

Mitigation: Prefer HTTPS or a local SSH/VPN tunnel, use a narrowly scoped and revocable token, and use an unprivileged SSH account for forwarding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengzie/skills/mobazha-store-mcp-connect)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Mobazha store API token; SSH credentials are optional for tunneled remote VPS connections.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
