## Description:

This skill helps an agent control music hardware and software through osc-bridge, including hardware synthesizers over MIDI/SysEx, DAWs over OSC, and live-coding environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roomi-fields](https://clawhub.ai/user/roomi-fields)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and musicians use this skill to discover osc-bridge device routes, configure the MCP server and bridge process, and send OSC commands to supported MIDI hardware, DAWs, and live-coding environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can run an unpinned npm package automatically.

Mitigation: Pin @roomi-fields/osc-bridge to a reviewed version and avoid automatic unreviewed updates.

Risk: The bridge can control local MIDI devices, OSC ports, and DAW targets.

Mitigation: Run it only with the MIDI devices, local ports, and DAW targets the user intends to control.

Risk: OSC and UDP transport failures may be silent, so commands can appear successful without reaching a device.

Mitigation: Confirm the device catalogue path, bridge process, OSC client, MIDI output port, argument types, and target address before relying on results.

## Reference(s):

- [Devices: finding drivers and how addresses map to the wire](references/devices.md)
- [DAW and live-coding targets](references/software-targets.md)
- [When nothing happens](references/troubleshooting.md)
- [osc-bridge documentation site](https://roomi-fields.github.io/osc-bridge/)
- [vcv-osc plugin](https://github.com/roomi-fields/vcv-osc)
- [ClawHub skill page](https://clawhub.ai/roomi-fields/skills/osc-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is oriented around OSC route discovery, local bridge setup, MIDI port selection, and troubleshooting silent transport failures.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
