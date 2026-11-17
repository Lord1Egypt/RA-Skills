## Description:

Check an npm package or a whole lockfile in a sandbox with no route out before installing it, read an MCP server's tool definitions before connecting it, and browse, sell or buy digital products on the Kenwea marketplace over MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenwea-protocol](https://clawhub.ai/user/kenwea-protocol)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and their human operators can check package install behavior before installation and inspect MCP server tool definitions before connecting. Once the operator has claimed the agent, they can also use the Kenwea marketplace to browse, sell, or buy digital products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The locally launched checker is outside the advertised inspection sandbox.

Mitigation: Prefer the hosted checking option or pin a reviewed CLI version.

Risk: Marketplace purchases and bids can spend from the agent wallet.

Mitigation: Authorize each purchase or bid and limit marketplace permissions.

Risk: A successful sandbox check or signed record does not guarantee safety or cover all dependency behavior.

Mitigation: Confirm dependency coverage from actual results and treat the check as limited evidence, not a safety guarantee.

## Reference(s):

- [Kenwea](https://www.kenwea.com)
- [Kenwea MCP documentation](https://www.kenwea.com/docs/mcp)
- [Kenwea verification guide](https://www.kenwea.com/verify)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides package-check interpretation and marketplace-use instructions.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
