## Description:

Send emails via Gmail SMTP using a Python CLI tool with a Google App Password for alerts, notifications, and automated reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junkaixue](https://clawhub.ai/user/junkaixue)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure Gmail SMTP email sending for automated alerts, notifications, and scheduled reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Gmail credentials and can send email over the network.

Mitigation: Use a dedicated least-privilege Gmail account or app password where possible, store credentials in environment variables, and revoke app passwords if compromised.

Risk: Automated or scheduled use can send messages without direct human review after configuration.

Mitigation: Review cron jobs and automation policies before deployment, especially for messages containing sensitive, regulated, or high-volume content.

Risk: Email content may be handled by Google/Gmail services.

Mitigation: Avoid sending secrets or regulated data unless organizational policy permits Gmail handling for that data.

## Reference(s):

- [Google Account Security](https://myaccount.google.com/security)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Gmail account with 2FA and a Google App Password.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
