## Description:

Lofy Home helps an agent control smart-home scenes, devices, media, thermostat adjustments, and Wake-on-LAN through Home Assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrey401](https://clawhub.ai/user/harrey401)

### License/Terms of Use:


## Use Case:

External users and smart-home operators use this skill to activate home scenes, control configured Home Assistant devices, and receive brief status or failure messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous or casual commands can change physical home state.

Mitigation: Require explicit confirmation for thermostat changes, presence-based automations, broad scenes, and Wake-on-LAN before executing device actions.

Risk: The skill documents use of a Home Assistant bearer token over HTTP.

Mitigation: Use HTTPS or a tightly isolated local network, and create a least-privilege Home Assistant token for agent access.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and short natural-language confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured Home Assistant entities and credentials; broad physical-state changes should require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
