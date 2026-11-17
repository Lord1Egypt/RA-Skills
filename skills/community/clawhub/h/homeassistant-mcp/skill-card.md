## Description:

Provides structured access to Home Assistant devices, sensors, and cameras via MCP, with handling for camera snapshots, garage doors, and device control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsnkzdeny](https://clawhub.ai/user/dsnkzdeny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use this skill to interact with Home Assistant entities through MCP, including status checks, device operations, camera snapshots, and garage-door workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived Home Assistant access token may be passed through shell commands to a fixed plaintext HTTP endpoint.

Mitigation: Use only with a trusted Home Assistant endpoint; prefer HTTPS, scoped credentials, and user-configured endpoints before deployment.

Risk: Camera snapshots and entity mappings can expose private smart-home data in the workspace.

Mitigation: Treat snapshots and entity lists as sensitive data, save them only when needed, and remove local copies after review.

Risk: The skill can guide device and garage-door operations that affect the physical environment.

Mitigation: Require explicit user intent before control actions and verify device state before and after any operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dsnkzdeny/skills/homeassistant-mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Home Assistant entity names, endpoint configuration, REST API fallback commands, and camera snapshot handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
