## Description:

Helps agents manage MailerLite subscribers, groups, campaigns, automations, and forms through an authorized account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, operators, and developers use this skill to inspect or manage MailerLite audiences, campaigns, forms, and automations with an authorized connection. Changes to contacts, campaigns, or automations require user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized actions can change real subscriber data and email campaigns.

Mitigation: Confirm each write and its target before execution; prefer read-only requests when possible.

Risk: Webhooks or automations may forward events or trigger ongoing actions.

Mitigation: Obtain separate approval for each setup, limit destinations to those requested, and remove unused triggers.

Risk: Overbroad or retained account access can expose audience data.

Mitigation: Prefer OAuth, grant only necessary access, and revoke unused connections.

## Reference(s):

- [MailerLite skill release](https://clawhub.ai/byungkyu/skills/mailerlite)
- [MailerLite API documentation](https://developers.mailerlite.com/docs/)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require an authorized MailerLite connection; confirm writes before execution.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
