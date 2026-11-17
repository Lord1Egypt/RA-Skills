## Description:

Control and monitor Home Assistant smart devices using commands for lights, switches, covers, climate, scenes, scripts, and other entities through the Home Assistant API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue)

### License/Terms of Use:

MIT

## Use Case:

Developers and smart-home operators use this skill to configure and control Home Assistant entities from an agent-accessible command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Home Assistant long-lived access token can control every device allowed by the configured Home Assistant account.

Mitigation: Use a dedicated least-privilege Home Assistant account and rotate the token if it has been exposed in shell history, source control, or shared logs.

Risk: Commands can affect physical devices such as locks, covers, climate systems, scripts, and scenes.

Mitigation: Require explicit confirmation before running commands that unlock doors, move covers, change climate settings, or execute scripts and scenes.

Risk: Saved configuration can expose durable home-control credentials if it is committed or made readable to other users.

Mitigation: Keep the config file out of source control and restrict file permissions to the local user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris6970barbarian-hue/skills/glitch-homeassistant)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Home Assistant CLI setup and device-control guidance; actions depend on the configured Home Assistant account permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
