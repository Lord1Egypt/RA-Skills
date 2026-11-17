## Description:

Send NEAR reports and alerts via email with SMTP configuration, scheduling, and automatic reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaiss](https://clawhub.ai/user/shaiss)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure SMTP settings and generate NEAR account balance reports intended for email delivery, alerts, and scheduled reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP passwords are accepted through command-line arguments and stored in a local plaintext configuration file.

Mitigation: Use an app-specific SMTP password, avoid reusable account passwords, review shell history exposure, and rotate credentials after testing.

Risk: The artifact overstates email sending, alerts, and scheduling because the shipped script prints reports and placeholder messages unless additional implementation is added.

Mitigation: Treat email delivery, alerting, and scheduling as unfinished until nodemailer and a scheduler are configured and tested in the deployment environment.

## Reference(s):

- [Nodemailer](https://nodemailer.com/)
- [NEAR RPC API](https://docs.near.org/api/rpc)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes SMTP configuration to ~/.near-email/config.json and prints generated NEAR account reports to stdout.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
