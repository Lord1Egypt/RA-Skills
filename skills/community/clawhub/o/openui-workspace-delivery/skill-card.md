## Description:

Teach an agent how to install OpenUI MCP Studio, connect it to a host, and use the core UI generation and review workflow without overclaiming a live marketplace listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and attach OpenUI MCP Studio as a local MCP server, then run a grounded UI generation and review proof loop for shadcn-style workspace delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable external OpenUI MCP Studio code.

Mitigation: Review or pin the external repository and dependencies before installing or running the local MCP server.

Risk: Host configuration examples require a Gemini API key.

Mitigation: Use a dedicated restricted key, avoid committing host config files, and prefer a secret store or inherited environment variable where supported.

Risk: The local MCP server may receive more workspace access than the UI task requires.

Mitigation: Run the server with only the workspace access needed for the specific generation or review task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaojiou176/skills/openui-workspace-delivery)
- [OpenUI MCP Studio Repository](https://github.com/xiaojiou176-open/openui-mcp-studio.git)
- [Install And Attach OpenUI MCP Studio](references/INSTALL.md)
- [OpenUI MCP Studio Capabilities](references/CAPABILITIES.md)
- [OpenUI MCP Studio First-Success Demo](references/DEMO.md)
- [OpenHands MCP Config](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP Config](references/OPENCLAW_MCP_CONFIG.json)
- [OpenUI MCP Studio Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup steps, host configuration guidance, proof-loop instructions, and review criteria for MCP-based UI delivery.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
