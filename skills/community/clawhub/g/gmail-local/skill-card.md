## Description:

Local Gmail IMAP/SMTP access using a Google App Password. Use when the user wants to search, read, or send Gmail without routing mail through Maton or any third-party proxy. Requires GMAIL_ADDRESS and GMAIL_APP_PASSWORD_FILE. All writes/sends require explicit user approval and --confirm-send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alanwen168](https://clawhub.ai/user/alanwen168)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and agents use this skill to search, read, list, and send Gmail messages directly through local IMAP/SMTP access when the configured account is authorized for that work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has direct IMAP/SMTP access to the configured Gmail account.

Mitigation: Use a dedicated Google App Password for the account and revoke or rotate it when access is no longer needed.

Risk: The local app-password file could expose mailbox access if readable by other users.

Mitigation: Store the credential in an owner-only readable file and keep GMAIL_APP_PASSWORD_FILE pointed to that file.

Risk: Email could be sent to unintended recipients or with unintended content.

Mitigation: Review recipients, subject, and body preview before sending; only run send after explicit approval and with --confirm-send.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alanwen168/skills/gmail-local)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GMAIL_ADDRESS and GMAIL_APP_PASSWORD_FILE; send operations require explicit approval and --confirm-send.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
