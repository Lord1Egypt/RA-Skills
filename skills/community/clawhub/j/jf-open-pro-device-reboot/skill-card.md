## Description:

杰峰设备重启技能（开发版）。支持远程重启设备，部分设备支持关闭操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and device administrators use this skill to send remote reboot or shutdown commands to JFTech devices that are already bound to an Open Platform account and online.

### Deployment Geography for Use:

China, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: The skill can reboot or shut down devices without mandatory confirmation.

Mitigation: Require explicit human confirmation immediately before any reboot or shutdown action.

Risk: Device-control credentials may be sent to any endpoint configured through JF_ENDPOINT.

Mitigation: Set JF_ENDPOINT only to an official documented regional host and keep JF credentials and device tokens tightly scoped.

Risk: A reboot or shutdown can temporarily take the device offline and interrupt operations.

Mitigation: Use the skill only for devices the operator owns or administers, and confirm device availability and operational impact before sending the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-device-reboot)
- [JFTech Open Platform documentation](https://docs.jftech.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JF Open Platform credentials, a device token, and an online device before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
