## Description:

引导用户安装、连接和配置领星（Lingxing）官方 MCP，并排查连接、鉴权、权限与客户端兼容性问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and configure the official Lingxing MCP connection in an MCP-capable client. It focuses on collecting the MCP Server URL and X-Mcp-Key securely, validating connection and authentication, and troubleshooting setup issues without accessing Lingxing business data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP Server URL and X-Mcp-Key are sensitive and could be exposed if pasted into ordinary chat, logs, shell commands, screenshots, or example files.

Mitigation: Use a secure credential input, secret store, or local MCP configuration, mask any displayed key value, and regenerate the key if it was exposed.

Risk: Connection validation could unintentionally access Lingxing business data if the agent uses business tools during setup.

Mitigation: Limit validation to server connectivity, authentication, and tool discovery; do not query inventory, orders, listings, sales, profit, advertising, or other business data.

Risk: Bundled screenshot assets referenced by the install guide are not present in the artifact.

Mitigation: Use the official Lingxing MCP help page when current screenshots or UI labels are needed.

## Reference(s):

- [Lingxing MCP official guide](https://www.lingxing.com/help/article/mcp)
- [领星官方 MCP 安装引导](artifact/references/install.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-lingxing-erp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not produce or store Lingxing credentials; validation is limited to connection, authentication, and tool discovery.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
