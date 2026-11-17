## Description:

OpenClaw 沙盒测试系统 v2.0 helps users test OpenClaw configuration changes with layered isolation, validation, backups, rollback guidance, and Git-based version management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoopools](https://clawhub.ai/user/zoopools)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to test configuration changes in an isolated local sandbox, validate settings, back up production configuration, and apply changes with rollback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can affect live OpenClaw configuration and restart the Gateway.

Mitigation: Review configuration changes, verify backups, and manually confirm rollback steps before running production apply workflows.

Risk: The localhost sandbox Gateway can remain running after tests.

Mitigation: Add or run a reliable stop and cleanup path, then confirm the recorded process and port are closed.

Risk: The sandbox uses a static token and a predictable temporary directory.

Mitigation: Replace the static token and use a unique secure temporary directory before running the sandbox.

Risk: Third-party plugins can weaken sandbox isolation.

Mitigation: Disable third-party plugins by default and enable only the plugins required for a specific test.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoopools/skills/openclaw-sandbox)
- [Small Change Example](artifact/examples/小改动示例.md)
- [Large Change Example](artifact/examples/大改动示例.md)
- [Sandbox Contamination Cases](artifact/examples/污染问题案例.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local OpenClaw sandbox setup, backup, validation, Gateway restart, cleanup, and rollback instructions.]

## Skill Version(s):

2.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
