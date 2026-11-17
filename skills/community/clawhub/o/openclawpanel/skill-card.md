## Description:

Control an OpenClaw LED panel (64x32 HUB75 on ESP32-S3) over HTTP to display text, graphics, shapes, play sounds, and read status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joaquinckronoset](https://clawhub.ai/user/joaquinckronoset)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an agent control a local OpenClaw LED panel, including drawing display content, playing sounds, checking status, and adjusting brightness or volume.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a physical display, play audible sounds, and persist brightness or volume settings on the configured panel.

Mitigation: Install only when agent control of the panel is intended, verify OPENCLAW_PANEL_IP points to the user's own local device, and review commands before execution.

Risk: Commands sent to an unintended or unreachable panel IP may affect the wrong local device or fail unexpectedly.

Mitigation: Check device status before use and keep the OpenClaw host and panel on the expected local network.

## Reference(s):

- [OpenClaw Panel ClawHub page](https://clawhub.ai/joaquinckronoset/skills/openclawpanel)
- [OpenClaw Panel project](https://github.com/joaquinckronoset/openclawpanel)
- [Skill API reference](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP API examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OPENCLAW_PANEL_IP and curl to issue local HTTP requests to the configured panel.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
