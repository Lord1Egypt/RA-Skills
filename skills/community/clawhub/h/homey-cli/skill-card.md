## Description:

Control Homey smart-home devices, zones, and automation flows through a CLI with capability-allowlisted write operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krausefx](https://clawhub.ai/user/krausefx)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent inspect Homey hub state, control allowlisted smart-home device capabilities, manage zones, and trigger Homey flows from CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect real smart-home devices through on/off, dimming, color, temperature, and flow-trigger commands.

Mitigation: Install only when an agent is intended to control Homey devices; review requested actions before execution and keep write capabilities allowlisted.

Risk: Homey OAuth credentials and token files grant access to the user's Homey account and devices.

Mitigation: Protect HOMEY_CLIENT_ID, HOMEY_CLIENT_SECRET, and files under ~/.config/homey-cli/; rotate credentials if exposed.

Risk: Triggered flows may perform broader home automations than a single device command.

Mitigation: Inspect flows before triggering them and restrict agent access to flows that are acceptable for automated operation.

## Reference(s):

- [Homey Developer App Tools](https://tools.developer.homey.app/tools/app)
- [ClawHub skill page](https://clawhub.ai/krausefx/skills/homey-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/krausefx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Homey CLI commands that read device state or change allowlisted device capabilities when the user directs it.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
