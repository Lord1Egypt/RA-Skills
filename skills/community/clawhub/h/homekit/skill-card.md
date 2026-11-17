## Description:

Control Apple HomeKit smart home devices, including listing, discovering, pairing, and managing lights, switches, outlets, thermostats, and fans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manifoldor](https://clawhub.ai/user/manifoldor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use this skill to discover, pair, inspect, and control Apple HomeKit accessories from an agent-assisted command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls real smart-home devices, including device classes that may affect safety or property.

Mitigation: Review actions before execution and avoid using it for locks, garage doors, thermostats, or other safety-sensitive devices without explicit confirmation.

Risk: Pairing commands can include real HomeKit PINs and pairing data is stored locally.

Mitigation: Remove pairing commands containing real PINs from shell history and protect or delete ~/.config/homekit/pairings.json when the skill is no longer needed.

Risk: Device discovery and control depend on a trusted local network and paired HomeKit accessories.

Mitigation: Use the skill only on a trusted machine and network, and confirm the target alias before sending control commands.

## Reference(s):

- [HomeKit API Reference](references/api.md)
- [Apple HomeKit Documentation](https://developer.apple.com/homekit/)
- [homekit_python Library](https://github.com/jlusiardi/homekit_python)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may operate local HomeKit devices and store pairing data in ~/.config/homekit/pairings.json.]

## Skill Version(s):

1.0.6 (source: server release evidence, created 2026-03-21T04:54:21Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
