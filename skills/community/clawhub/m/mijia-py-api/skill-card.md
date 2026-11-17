## Description:

mijia-py-api lets an agent query status, set properties, and run scenes for Xiaomi/Mijia smart-home devices through mijiaAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xcchenx345](https://clawhub.ai/user/xcchenx345)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent inspect and control their Xiaomi/Mijia smart-home devices, including device status, property changes, and automation scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control physical smart-home devices and run scenes through a local Mijia account.

Mitigation: Require explicit user confirmation before any scene execution or device state change, especially for cameras, locks, or other sensitive devices.

Risk: The skill depends on local Mijia account authentication and can expose account context through command execution or logs.

Mitigation: Use a trusted local environment, prefer a virtual environment with pinned dependencies, and avoid running setup or authentication checks in logged or shared terminals.

## Reference(s):

- [Standard Operating Procedure](instructions.md)
- [Device MIoT Property Catalog](reference/device_catalogs.md)
- [ClawHub Skill Page](https://clawhub.ai/xcchenx345/skills/mijia-py-api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown/text responses with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query local Mijia account state and propose or execute device and scene changes after confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
