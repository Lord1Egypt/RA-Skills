## Description:

Guides agents through configuring Cloud Studio IoT's OpenClaw MCP gateway for IoT device commands, sensor reads, channel management, and agent task execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sobdev](https://clawhub.ai/user/sobdev)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to connect MCP clients to an OpenClaw gateway, verify gateway health, configure local or remote access, and troubleshoot IoT platform interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote OpenClaw MCP gateway access can expose IoT device controls, sensor data, channel messaging, and agent task execution.

Mitigation: Prefer loopback-only access or a private tailnet, and avoid public funnel mode unless strong authentication and network controls are in place.

Risk: High-impact OpenClaw tools can send device commands, publish channel messages, or run agent tasks through the gateway.

Mitigation: Disable or separately protect high-impact tools such as device commands, channel sending, and agent task execution when remote access is enabled.

## Reference(s):

- [OpenClaw Gateway Documentation](https://docs.openclaw.ai/gateway)
- [Cloud Studio IoT](https://cloudstudioiot.com/)
- [ClawHub Skill Page](https://clawhub.ai/sobdev/skills/iot-platform)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, YAML, and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configuration guidance for MCP clients and OpenClaw gateway access modes.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
