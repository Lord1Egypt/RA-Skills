## Description:

Control Philips Hue lights and scenes via the OpenHue CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

People using Philips Hue lights can ask an agent to list Hue lights, rooms, and scenes, then adjust lights or activate scenes through the OpenHue CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI commands can change the state, brightness, or color of Hue lights and activate scenes.

Mitigation: Confirm the intended light, room, or scene and requested setting before executing a change.

Risk: Initial pairing requires pressing the Hue Bridge button.

Mitigation: Pair only with the intended Hue Bridge and perform the physical button press yourself.

## Reference(s):

- [OpenHue CLI documentation](https://www.openhue.io/cli)
- [Openhue on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-openhue)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the OpenHue CLI to list resources and control lights, rooms, or scenes.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
