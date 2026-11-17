## Description:

Multi-Protocol Bridge is an AgentPMT-hosted HTTP gateway that helps agents prepare FTP, FTPS, SSH, MQTT, and MQTTS tool calls for file transfer, remote command execution, and message publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and automation agents use this skill to call AgentPMT protocol-bridge actions for FTP file operations, SSH health checks or administration commands, and MQTT message publishing against explicitly authorized targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may route credentials, private keys, file contents, commands, and MQTT payloads through a third-party gateway.

Mitigation: Use only authorized targets, minimize submitted data, prefer least-privilege short-lived credentials, and avoid production SSH private keys in ordinary tool parameters.

Risk: FTP deletion, retained MQTT messages, and SSH commands can change or remove remote system state.

Mitigation: Require explicit approval before deletions, retained MQTT publishes, or SSH commands that modify systems.

Risk: Plain FTP or MQTT URLs can expose sensitive traffic when used without TLS.

Mitigation: Prefer FTPS and MQTTS whenever credentials, files, or operational messages are involved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/multi-protocol-bridge)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/multi-protocol-bridge)
- [Multi-Protocol Bridge Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, JSON parameters]

**Output Format:** [Markdown instructions with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents six AgentPMT actions; FTP transfers are capped at 100 MB, MQTT payloads at 1 MB, and SSH stdout/stderr at 10 MB each.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
