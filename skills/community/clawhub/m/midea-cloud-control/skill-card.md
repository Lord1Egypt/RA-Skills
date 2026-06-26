## Description: <br>
Connects a user's Midea cloud account, lists discovered Midea devices, and sends on/off commands to named Midea air conditioners through cloud APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fooklook](https://clawhub.ai/user/fooklook) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to connect a Midea account, cache discovered devices locally, list available devices, and send power on/off commands for named air conditioners. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Midea account credentials locally in plaintext at ~/.openclaw/midea-cloud-control/config.json. <br>
Mitigation: Warn before first-time credential storage, avoid echoing passwords, protect the local config file, and delete it when no longer needed. <br>
Risk: On/off commands can affect real appliances and cloud write calls may not prove the physical device changed state. <br>
Mitigation: Use exact device names, report only that the cloud command was sent, and rely on user confirmation or observed device behavior for physical success. <br>
Risk: The verified workflow is limited to account connection, cached device listing, and power toggling. <br>
Mitigation: Do not claim support for temperature control, mode switching, real-time state reads, or indoor temperature reads. <br>


## Reference(s): <br>
- [API Notes](references/api-notes.md) <br>
- [Generated Config Store](references/generated-config-store.md) <br>
- [Generated Midea Skill CLI](references/generated-midea-skill-cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output from generated Python helpers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local helper scripts and a local Midea account/device configuration cache when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
