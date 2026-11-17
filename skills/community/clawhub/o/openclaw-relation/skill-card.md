## Description:

OpenClaw documentation knowledge base covering installation, configuration, Gateway management, channels, nodes, CLI commands, automation, security, and core functionality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aetik-yue](https://clawhub.ai/user/aetik-yue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and OpenClaw users use this skill as a reference for installing, configuring, operating, and troubleshooting OpenClaw gateways, channels, nodes, automation, and security controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example setup commands use a mutable global OpenClaw install and daemon installation.

Mitigation: Pin the OpenClaw package version, review daemon behavior and removal steps, and install only in an environment intended to run the service.

Risk: Gateway, webhook, and remote access guidance can expose agent access outside a local trusted context.

Mitigation: Restrict gateway and webhook access to trusted users and networks, prefer private tunnels, and verify allowlists before enabling remote access.

Risk: Mobile node features include camera, location, audio, and remote-control capabilities.

Mitigation: Enable sensitive device features only with explicit consent, least-privilege access, and logging appropriate for the deployment.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai/zh-CN)
- [OpenClaw documentation index](https://docs.openclaw.ai/llms.txt)
- [ClawHub skill page](https://clawhub.ai/aetik-yue/skills/openclaw-relation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw reference guidance and examples; review commands and configuration before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
