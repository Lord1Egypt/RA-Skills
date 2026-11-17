## Description:

Send text, image, interactive card, rich-text post, and shared-chat messages through a connected Feishu Custom Bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send messages through a Feishu Custom Bot connected to their OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run software whose behavior has not been verified and may add other agent skills.

Mitigation: Review and verify the installer release before running it, and inspect any skills it adds.

Risk: Messages are sent to Feishu recipients through write actions.

Mitigation: Keep confirmation enabled and review the recipients and message content before sending.

## Reference(s):

- [Feishu Custom Bot API documentation](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Feishu](https://www.feishu.cn)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON]

**Output Format:** [oo CLI commands with JSON payloads and structured connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends one message action per connector call.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
