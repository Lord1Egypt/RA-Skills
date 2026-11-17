## Description:

Provides agent-facing guidance and shell commands for controlling JF/JieFeng PTZ camera devices, including status checks, directional movement, privacy mask, zoom and focus, presets, and tour management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure credentials and operate JF/JieFeng camera PTZ workflows through the Open Pro API. Typical tasks include checking device status, starting and stopping movement, managing privacy mask state, adjusting zoom or focus, and maintaining presets or patrol tours.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JF camera and API credentials can be sent to any endpoint configured through JF_ENDPOINT.

Mitigation: Set JF_ENDPOINT only to the intended official JF API host and run the skill in an environment where other software cannot alter JF_* variables.

Risk: Preset, tour, mask, and PTZ commands can change physical camera position, recording behavior, or device state.

Mitigation: Review the target device, command, direction, and start/stop behavior before execution, especially for unattended tour or movement commands.

## Reference(s):

- [JF Open Platform](https://open.jftech.com/)
- [JF API Documentation](https://docs.jftech.com/)
- [ClawHub Skill Page](https://clawhub.ai/jftech/skills/jftech-open-pro-ptz-control)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on JF_* environment variables and selected JF API endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
