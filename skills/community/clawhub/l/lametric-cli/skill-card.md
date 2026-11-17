## Description:

Control LaMetric TIME/SKY smart displays from the command line for notifications, brightness and volume changes, timers, and device data display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dedene](https://clawhub.ai/user/dedene)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to generate LaMetric CLI commands and setup guidance for sending notifications, controlling display and audio settings, managing timers, and streaming content to LaMetric devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external LaMetric CLI installation.

Mitigation: Verify the CLI source before installing and use the install methods declared in the ClawHub metadata.

Risk: Notifications and streamed content may expose secrets or private operational details on a visible display.

Mitigation: Review messages and piped input before sending them to a device, especially when using logs, CI output, or shell pipelines.

Risk: Commands can change device state, including brightness, volume, timers, streaming sessions, Bluetooth, and app navigation.

Mitigation: Confirm state-changing commands before execution and target the intended device.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dedene/skills/lametric-cli)
- [LaMetric CLI repository](https://github.com/dedene/lametric-cli)
- [Publisher profile](https://clawhub.ai/user/dedene)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that may change device state or send visible notifications to LaMetric displays.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
