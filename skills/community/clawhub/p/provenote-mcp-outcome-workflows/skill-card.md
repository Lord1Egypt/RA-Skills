## Description:

Teach an agent to install Provenote's first-party MCP server, connect it in a host, and run read-first outcome workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect a local Provenote MCP server in OpenHands, OpenClaw, or similar hosts, then run read-first note and research workflows before attempting narrow mutations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to install and run mutable external code locally.

Mitigation: Use a trusted Provenote repository checkout, pin a reviewed commit or release, install with locked dependencies, and run the server in a restricted workspace or account.

Risk: The MCP server exposes mutation-capable draft, research-thread, auditable-run, and settings tools.

Mitigation: Start with the documented list calls and require explicit user confirmation before any write or settings mutation.

Risk: Host configuration can point at the wrong local clone or workspace.

Mitigation: Verify the configured path and confirm successful draft, research-thread, and auditable-run list calls before attempting a mutation.

## Reference(s):

- [Install and Connect Provenote MCP](references/INSTALL.md)
- [Provenote MCP Capabilities](references/CAPABILITIES.md)
- [OpenHands / OpenClaw Demo Walkthrough](references/DEMO.md)
- [Provenote Troubleshooting](references/TROUBLESHOOTING.md)
- [OpenHands MCP configuration](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP configuration](references/OPENCLAW_MCP_CONFIG.json)
- [Provenote repository](https://github.com/xiaojiou176-open/provenote)
- [ClawHub skill listing](https://clawhub.ai/xiaojiou176/skills/provenote-mcp-outcome-workflows)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first workflow guidance for MCP list calls followed by a single narrow mutation.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
