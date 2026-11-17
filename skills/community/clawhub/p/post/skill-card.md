## Description:

Manage IMAP email with the Post CLI and daemon, including reading, searching, drafting, replies, attachments, and scoped per-agent API-key access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email-assistant agents use Post to inspect and organize configured IMAP mailboxes, prepare email drafts and replies, export messages or attachments, and set up scoped access to mail servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling and existing `.env` files may expose mail access credentials.

Mitigation: Review the credential and `.env` handling before setup; use the narrowest practical per-agent API key and avoid broad shared tokens.

Risk: Bulk mailbox actions and a daemon that can start at login may make unintended changes or run hooks without a fresh prompt.

Mitigation: Review the configured daemon and hooks, and verify the target server, mailbox, and message UIDs before bulk move, archive, trash, or junk actions.

## Reference(s):

- [Post project homepage](https://github.com/Cocoanetics/Post)
- [ClawHub release page](https://clawhub.ai/odrobnik/skills/post)
- [Setup guide](SETUP.md)
- [Common tasks](references/common-tasks.md)
- [IDLE hook schema](references/hook-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Email drafts and task guidance in text or Markdown, structured results in JSON, and CLI commands or configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, export, draft, or organize mail in configured IMAP mailboxes; UID values are mailbox-scoped.]

## Skill Version(s):

1.11.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
