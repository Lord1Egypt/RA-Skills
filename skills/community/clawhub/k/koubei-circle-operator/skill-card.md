## Description:

口碑圈商家运营自动化技能，用于口碑圈发帖、活动管理、数据监控、自动提醒和长连接推送，需要商户 Key 才能执行操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanceng666](https://clawhub.ai/user/quanceng666)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and operators use this skill to manage Koubei Circle community operations through OpenClaw, including publishing or editing posts, querying user and activity data, sending messages, managing labels, uploading media, and adjusting points. It is intended for merchant accounts that have already enabled Koubei Circle and obtained a merchant Key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A powerful merchant Key can query business or user data and perform remote actions such as publishing posts, editing content, sending bulk messages, changing labels, and increasing points.

Mitigation: Install only if the Koubei/OpenClaw service is trusted, use a least-privilege Key where available, rotate it when needed, and require human review before write operations.

Risk: The merchant Key is stored insecurely in local configuration.

Mitigation: Protect the local config file, avoid committing or sharing it, and rotate the Key if it may have been exposed.

Risk: SQL queries, uploads, message batches, points changes, and post edits can affect merchant data or users at scale.

Mitigation: Manually review query scope, target users, files, message content, point values, and post edits before allowing the agent to execute them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quanceng666/skills/koubei-circle-operator)
- [Publisher Profile](https://clawhub.ai/user/quanceng666)
- [Koubei Circle Official Site](https://dengluu.com)
- [OpenClaw CLI Command Reference](references/api.md)
- [Koubei Circle Feature Guide](references/features.md)
- [Koubei Circle Version Plans](references/versions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI inputs or outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a merchant Key and can trigger remote read and write operations against Koubei/OpenClaw services.]

## Skill Version(s):

1.4.1 (source: server release evidence and SKILL.md heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
