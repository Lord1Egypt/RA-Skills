## Description:

Read, search, send, trash, move, and label Gmail via IMAP using Gmail address and Google App Password environment variables, with no Google API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottgl9](https://clawhub.ai/user/scottgl9)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent read, search, send, move, label, and trash Gmail messages through IMAP and SMTP with credentials supplied through environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moving or trashing email can affect the wrong message if message identifiers are mishandled.

Mitigation: Review actions before execution, use stable IMAP UIDs, and confirm message metadata before move or trash commands.

Risk: The skill depends on a Gmail App Password stored in environment variables.

Mitigation: Use a dedicated Google App Password, protect GMAIL_IMAP_USER and GMAIL_IMAP_PASSWORD, and avoid printing or logging credential values.

## Reference(s):

- [Gmail IMAP Reference](references/gmail-imap-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/skills/gmail-imap)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output from the Gmail helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GMAIL_IMAP_USER and GMAIL_IMAP_PASSWORD environment variables; commands may access, send, move, label, or trash Gmail messages.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
