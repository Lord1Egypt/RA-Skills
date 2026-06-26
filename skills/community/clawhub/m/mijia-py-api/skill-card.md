## Description: <br>
Controls Xiaomi and Mijia smart-home devices through mijiaAPI, including device status checks, property updates, and scene execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xcchenx345](https://clawhub.ai/user/xcchenx345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect and control Xiaomi or Mijia smart-home devices from a local Python environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an existing Mijia login to reveal household details, device lists, scenes, and account identifiers. <br>
Mitigation: Avoid sharing setup or device-list logs, and review outputs before pasting them into external systems. <br>
Risk: The skill can change real smart-home device state or run automation scenes. <br>
Mitigation: Require explicit user confirmation before every state-changing command or scene run. <br>
Risk: Sensitive devices such as cameras or locks may create higher safety and privacy impact. <br>
Mitigation: Require a second confirmation for sensitive operations and prefer a version that enforces confirmation in code. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/xcchenx345/mijia-py-api) <br>
- [Device MIoT Property Catalog](reference/device_catalogs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and natural-language status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Python CLI commands that inspect homes, devices, scenes, and consumables or change device properties.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
