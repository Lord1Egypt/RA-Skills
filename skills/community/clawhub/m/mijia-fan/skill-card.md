## Description:

Xiaomi 米家风扇控制 Skill，支持开关、切换、状态查看、风速调节、摆风控制和米家设备列表查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[renjianboshi](https://clawhub.ai/user/renjianboshi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate a configured Xiaomi Mijia fan through shell commands, including power, speed, swing, status, and device discovery actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Xiaomi account-backed smart-home access to control a physical fan.

Mitigation: Install only after approving that access, configure MIJIA_FAN_DID for the intended device, and review agent-issued control commands before execution.

Risk: The installer may copy an existing Xiaomi authentication token from another local skill.

Mitigation: Remove or explicitly approve token-copy behavior before use, and manage Xiaomi tokens intentionally.

Risk: The list command can expose Mijia device names, IDs, and models in agent-visible output or logs.

Mitigation: Avoid running the list command unless device inventory disclosure is acceptable, and redact device identifiers when sharing logs.

Risk: The dependency is installed without a pinned version in the installer.

Mitigation: Pin and review dependency versions before deployment in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/renjianboshi/skills/mijia-fan)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the mijiaAPI package, and MIJIA_FAN_DID for device-specific actions.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, target metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
