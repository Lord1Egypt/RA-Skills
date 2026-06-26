## Description: <br>
Control Xiaomi Mijia smart home devices, including turning lights on or off, adjusting brightness, setting color temperature, and switching lighting modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hqman](https://clawhub.ai/user/hqman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to let an AI coding agent control configured Xiaomi Mijia lamps or related smart-home devices through natural-language mappings and CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can immediately change the state of the configured Mijia device. <br>
Mitigation: Verify that MIJIA_LAMP_DID points to the intended device, review the Xiaomi QR login flow, and require confirmation before power or mode changes for devices with safety impact. <br>


## Reference(s): <br>
- [mijia-api library](https://github.com/Do1e/mijia-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands act on the device identified by MIJIA_LAMP_DID and report status or action confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
