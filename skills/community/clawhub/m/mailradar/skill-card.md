## Description:

MailRadar turns the last 7 days of Feishu mailbox activity into an offline HTML workboard and daily Feishu card with task and deadline reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzhe223-tech](https://clawhub.ai/user/chenzhe223-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams using Feishu Mail can use this skill to summarize recent flagged and inbox messages into a store-opening workboard, track deadlines, and push daily status cards to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install persistent full-access daily automation.

Mitigation: Run the installer with --no-automation first and enable scheduled automation only after confirming that persistent WorkBuddy automation is acceptable.

Risk: Email-derived content may be written to local files, sent for LLM translation, rendered into HTML, and delivered through Feishu messages.

Mitigation: Use --no-push for local preview, avoid sensitive mailboxes unless approved, and review generated files before sharing or enabling push delivery.

Risk: Feishu push delivery depends on the configured recipient open_id.

Mitigation: Verify the recipient open_id with lark-cli contacts before enabling push delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenzhe223-tech/skills/mailradar)
- [中文翻译层说明](references/cn-translate.md)
- [部署与分享指南](references/deploy.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, local JSON outputs, an offline HTML dashboard, and Feishu card delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local email-derived JSON files, a self-contained HTML dashboard, Feishu cards or attachments, and an optional daily WorkBuddy automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
