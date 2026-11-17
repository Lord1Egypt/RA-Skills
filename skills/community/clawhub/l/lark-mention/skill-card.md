## Description:

飞书 @ 提及专属技能。支持在群聊中向指定成员发送带真实 @ 提及的消息，解决飞书无法通过纯文本标签艾特成员的问题。触发场景：群里艾特成员、艾特全员、发送带 @ 的通知公告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[toto2016](https://clawhub.ai/user/toto2016)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send Lark or Feishu group messages that include real @ mentions for one member, multiple members, or all members. It helps prepare the correct text and mentions payloads when plain text tags would not trigger platform mentions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post live Lark or Feishu group notifications, including bulk mentions.

Mitigation: Review generated messages before sending, confirm the target chat and recipients, and avoid @all unless explicitly intended.

Risk: Unauthorized or misconfigured bridge usage could send messages through the wrong bot or chat context.

Mitigation: Use the skill only with an authorized local bridge and bot that have been approved for the target chat.

Risk: Unvalidated member IDs or display names could create malformed mention payloads.

Mitigation: Validate or escape member open IDs and names before passing them to the script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/toto2016/skills/lark-mention)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce message payloads that trigger live Lark or Feishu group notifications through an authorized local bridge.]

## Skill Version(s):

26.3.27 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
