## Description:

Control and monitor a Klipper 3D printer via the Moonraker API - print status, temps, pause, resume, cancel, emergency stop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogueecho](https://clawhub.ai/user/rogueecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, makers, and printer operators use this skill to monitor and control a Klipper 3D printer through Moonraker, including status checks, temperature review, file listing, and pause, resume, cancel, or emergency-stop actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MOONRAKER_HOST could target the wrong printer or a printer the user does not control.

Mitigation: Set MOONRAKER_HOST only to a trusted Moonraker instance for a printer the user controls before running commands.

Risk: Cancel and emergency-stop commands are disruptive physical-device actions.

Mitigation: Require explicit user confirmation before running cancel or emergency stop, and explain that emergency stop requires a firmware restart to recover.

Risk: Listing files exposes printer G-code filenames, sizes, and modified times.

Mitigation: Share file-list output only when needed for the user task and avoid exposing it outside the intended conversation or environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogueecho/skills/moonraker)
- [Publisher profile](https://clawhub.ai/user/rogueecho)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and Moonraker REST endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOONRAKER_HOST and curl; jq is optional for formatted JSON output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
