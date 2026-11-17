## Description:

Install and configure the AgentPMT MCP server so MCP-compatible AI agents can connect to the AgentPMT tool marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use this skill to connect MCP-compatible clients to AgentPMT through either a local STDIO connector or the remote HTTP endpoint. The setup covers credentials, client configuration, connection checks, and basic troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance uses unpinned package installation and @latest examples.

Mitigation: Pin an exact reviewed package version and avoid global installation unless the user has accepted that installation scope.

Risk: Bearer tokens combine an API key and budget key and may be stored in persistent agent configuration.

Mitigation: Keep tokens out of source control, logs, screenshots, and project files; prefer the narrowest budget key and rotate credentials immediately after exposure.

Risk: Connected agents may access paid tools through spending-authorized credentials.

Mitigation: Use budget limits, product approvals, spending caps, and dashboard audit logs to constrain and monitor tool usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/install-agentpmt-mcp)
- [AgentPMT website](https://www.agentpmt.com)
- [AgentPMT MCP endpoint](https://api.agentpmt.com/mcp)
- [AgentPMT dashboard](https://www.agentpmt.com/dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, client configuration snippets, authentication examples, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
