## Description:

Openclaw Push Doctor is a self-diagnostic skill that checks OpenClaw communication channels and scheduled tasks, then guides targeted repairs for Feishu, Telegram, WeChat, and cron failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose broken OpenClaw push channels, expired Feishu or Telegram authentication, WeChat bridge disconnects, and failed or duplicated cron jobs. It provides shell-command guidance and repair steps for restoring message delivery and scheduled pushes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair instructions can expose messaging credentials or configuration values in logs or chat.

Mitigation: Review commands before execution, avoid printing raw configuration or Telegram update data, and never paste bot tokens into conversation.

Risk: Cron repair flows can make broad changes to a user's scheduled jobs.

Mitigation: Prefer native OpenClaw cron commands, review the crontab diff, and require explicit user confirmation before reinstalling crontab entries.

Risk: Test pushes and authentication repairs can interact with live Feishu, Telegram, or WeChat channels.

Mitigation: Require explicit confirmation before sending test messages, changing configs, using sudo, or reauthorizing integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosmofang/skills/openclaw-push-doctor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style diagnostic guidance with shell commands and JSON health-report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English prompt output; check flows may ask the agent to update data/health-report.json.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact/_meta.json; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
