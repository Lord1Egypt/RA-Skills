## Description:

Control Home Assistant devices, read sensors, and manage automations using the Python Bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mischa-petschenig](https://clawhub.ai/user/mischa-petschenig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use this skill to control Home Assistant devices, query entity states and history, search for entities, manage aliases, and trigger scenes through the Home Assistant REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow stores a long-lived Home Assistant token in a shell-sourced configuration file.

Mitigation: Use a least-privileged Home Assistant token, keep the file private, and avoid adding the token file to shell startup unless that exposure is acceptable.

Risk: The setup script can execute shell code from configuration inputs.

Mitigation: Do not run ha-setup.sh with untrusted HA_URL or token values; review inputs before saving or source configuration manually.

Risk: Commands can change lights, switches, climate devices, scenes, and other connected equipment.

Mitigation: Review proposed commands before execution and use verification only against the intended Home Assistant instance.

## Reference(s):

- [Home Assistant authentication documentation](https://www.home-assistant.io/docs/authentication/#your-account-profile)
- [Finding Home Assistant entity IDs](references/finding-entities.md)
- [ClawHub skill page](https://clawhub.ai/mischa-petschenig/skills/home-assistant-bridge-python)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python command examples, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can call the Home Assistant REST API and returns JSON for state, search, history, and service-listing commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
