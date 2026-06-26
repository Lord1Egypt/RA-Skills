## Description: <br>
Control Meross cloud plugs via local CLI commands for discovery, state checks, and switch on/off actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[powtac](https://clawhub.ai/user/powtac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent discover Meross cloud plugs, read switch state, and perform explicitly confirmed on/off actions through a local CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Meross account credentials to access cloud devices. <br>
Mitigation: Set MEROSS_EMAIL and MEROSS_PASSWORD only in a trusted runtime, avoid writing credentials to project files, and protect the local environment. <br>
Risk: The skill can switch supported plugs on or off. <br>
Mitigation: Verify the exact deviceId, capability, and requested value before approving any set-device command. <br>
Risk: The local devices.json registry contains device identifiers and aliases. <br>
Mitigation: Keep devices.json access controlled and refresh it only from trusted runs of setup-once. <br>


## Reference(s): <br>
- [ClawHub Meross Smart skill page](https://clawhub.ai/powtac/meross) <br>
- [Skill README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI payloads or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Switch writes require an exact confirmation object; registry setup writes device identifiers and aliases to devices.json.] <br>

## Skill Version(s): <br>
1.0.27 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
