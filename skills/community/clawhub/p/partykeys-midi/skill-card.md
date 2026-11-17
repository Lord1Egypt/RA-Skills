## Description:

Control PartyKeys MIDI keyboard via WebSocket - connect device, light up keys with 12 colors, listen to playing, play sequences, and follow mode for music teaching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allen4z](https://clawhub.ai/user/allen4z)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and music educators use this skill to let an agent connect to a PartyKeys MIDI keyboard, control its LEDs, query device state, play note sequences, and guide follow-along music teaching workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a local hardware-control bridge for a MIDI keyboard.

Mitigation: Run it only on a trusted network or behind firewall rules, and prefer a version that binds to localhost or uses an explicit pairing token.

Risk: Setup changes OpenClaw configuration files used to register the MCP server.

Mitigation: Back up ~/.openclaw/mcp.json and ~/.openclaw/openclaw.json before setup and review configuration changes before restarting OpenClaw.

Risk: Dependency versions are not pinned in the release artifact.

Mitigation: Use pinned dependency versions before deployment where reproducibility or supply-chain control is required.

## Reference(s):

- [Partykeys Midi ClawHub release](https://clawhub.ai/allen4z/skills/partykeys-midi)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands and MCP tool arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report hardware connection status and device-control results through MCP tool responses.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
