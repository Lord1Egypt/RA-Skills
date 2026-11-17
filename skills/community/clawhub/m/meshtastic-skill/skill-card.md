## Description:

Send and receive messages via Meshtastic LoRa mesh network. Use for off-grid messaging, mesh network status, reading recent mesh messages, or sending texts via LoRa radio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukevr](https://clawhub.ai/user/lukevr)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to connect agents to Meshtastic LoRa mesh networks for off-grid messaging, mesh status checks, message monitoring, alerting, and digest generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish location and device metadata through map reporting.

Mitigation: Review configuration and code before running, keep map publishing disabled unless intentionally needed, and use fuzzy or approximate positions.

Risk: Mesh and MQTT traffic can be persisted locally and forwarded through alert or digest workflows.

Mitigation: Use a private log directory with restrictive permissions and avoid forwarding or acting on received mesh text until it has been reviewed as untrusted external content.

Risk: Broadcast mesh messages may expose sensitive information to unintended recipients.

Mitigation: Do not send secrets, precise locations, personal data, or operationally sensitive details over mesh channels.

Risk: Serial-device permission changes can overexpose the connected radio device.

Mitigation: Prefer group-based serial access over broad device permissions such as chmod 666.

## Reference(s):

- [Meshtastic Setup Guide](references/SETUP.md)
- [Claude Desktop MCP Configuration Example](references/claude_desktop_config.json)
- [Meshtastic Documentation](https://meshtastic.org/docs/)
- [Meshtastic MQTT Integration](https://meshtastic.org/docs/configuration/module/mqtt/)
- [Meshtastic Hardware Options](https://meshtastic.org/docs/hardware/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, JSON socket commands, MCP tool responses, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include mesh message text, node status, node lists, alert or digest summaries, and setup guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
