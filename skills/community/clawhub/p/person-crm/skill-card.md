## Description:

Personal relationship manager powered by Feishu/Lark Bitable. Track contacts, interactions, birthdays (including Chinese lunar calendar), anniversaries, and get proactive reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelyl](https://clawhub.ai/user/andrelyl)

### License/Terms of Use:

MIT

## Use Case:

External users and personal productivity agents use this skill to maintain a private relationship memory in Feishu/Lark Bitable, including contacts, interaction history, birthdays, anniversaries, and follow-up reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save sensitive personal and third-party relationship details from casual conversation.

Mitigation: Use explicit save commands where possible and review records before storing personal notes, birthdays, phone numbers, or relationship context.

Risk: Bulk contact import, phone-contact sync, and exports can move large amounts of personal data into or out of Feishu/Lark Bitable.

Mitigation: Run dry-run previews before imports, confirm the records to be synced or exported, and avoid phone-contact sync unless the user intentionally enables it.

Risk: Feishu/Lark credentials and Bitable tokens are required in local configuration.

Mitigation: Protect the local OpenClaw configuration file, avoid sharing credentials, and rotate Feishu/Lark app secrets if exposure is suspected.

Risk: Optional scheduled reminders give the agent recurring access to CRM data.

Mitigation: Enable the cron reminder only when recurring access is desired and review the configured channel, schedule, and permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andrelyl/skills/person-crm)
- [ClawHub Homepage Metadata](https://clawhub.ai/AndreLYL/person-crm)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Feishu](https://www.feishu.cn)
- [Lark](https://www.larksuite.com)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown responses with JSON configuration snippets, shell commands, and contact import or export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Feishu/Lark Bitable records and optional local import scripts for CSV, vCard, OCR, and phone-contact workflows.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
