## Description:

Sends email over SMTP with configurable recipient, subject, body, and account credentials such as a Gmail App Password.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaskies](https://clawhub.ai/user/jaskies)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to configure SMTP credentials and send plain-text email messages from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles SMTP credentials for sending email.

Mitigation: Use a dedicated app password with minimal permissions and provide it through a protected environment or secret manager.

Risk: Credential values may be supplied through command-line arguments.

Mitigation: Prefer environment variables or a secret manager so credentials are less likely to appear in shell history or process listings.

Risk: The security guidance recommends review before trusting the script with important email credentials.

Mitigation: Review the script before installing and consider using a verified SSL context before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaskies/skills/mail-sender-jaskies)
- [Publisher profile](https://clawhub.ai/user/jaskies)
- [Google Account](https://myaccount.google.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMTP account credentials supplied through environment variables or command-line arguments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
