## Description:

Provides a CLI for managing 126.com NetEase mail, including receiving, sending, searching, organizing, attachment downloads, and mailbox statistics with JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slamw](https://clawhub.ai/user/slamw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate a 126.com mailbox through explicit CLI commands for setup, reading, sending, searching, mailbox management, attachment download, and statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The mailbox authorization code is stored weakly and grants access to the configured 126.com account.

Mitigation: Use only an account the agent is intended to access, protect the local configuration file, and revoke or rotate the authorization code when access is no longer needed.

Risk: Send, forward, delete, and move operations can expose information or irreversibly change mailbox state.

Mitigation: Manually confirm recipients, message content, UIDs, folders, and destructive actions before running the command.

Risk: Attachment downloads may write attacker-controlled filenames into the selected output directory.

Mitigation: Download attachments only into a non-sensitive staging directory and avoid broad attachment download workflows until filename sanitization is fixed.

Risk: Automated or scheduled mailbox operations could amplify mistakes across many messages.

Mitigation: Limit automation scope, use small limits or narrow search criteria, and require review for send, forward, delete, move, and download actions.

## Reference(s):

- [Mail-126 data schema](references/data-schema.md)
- [ClawHub skill page](https://clawhub.ai/slamw/skills/mail-126)
- [Publisher profile](https://clawhub.ai/user/slamw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with bash command examples; executed CLI commands return JSON objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided 126.com email address and authorization code; mail operations use IMAP and SMTP over SSL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
