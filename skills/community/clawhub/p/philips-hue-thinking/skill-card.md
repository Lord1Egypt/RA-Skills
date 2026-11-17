## Description:

Visual AI activity indicator that uses Philips Hue lights to pulse red while an agent is thinking and turn green when it is done.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesserod329](https://clawhub.ai/user/jesserod329)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to give an AI assistant a physical activity indicator through a configured Philips Hue bridge and color bulb. It provides guidance and shell commands for setup, status changes, and workflow hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The assistant can control the configured Philips Hue light on the user's local network.

Mitigation: Install only when local Hue light control is intended, and configure it for a chosen light rather than broad unattended use.

Risk: The Hue username stored in the local configuration can control lights on the local network.

Mitigation: Protect the Hue configuration file and avoid exposing it in logs, shared shells, or copied troubleshooting output.

Risk: Shell hooks or automatic invocations may run light-control commands from a user profile.

Mitigation: Review hook scripts before adding them to a shell profile and prefer a user-owned PATH install over sudo where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesserod329/skills/philips-hue-thinking)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Philips Hue bridge, Hue color bulb, curl, Bash 4.0 or later, and a selected light ID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
