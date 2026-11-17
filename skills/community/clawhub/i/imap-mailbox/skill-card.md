## Description:

Read and manage emails via IMAP protocol. List, read, search, and download email attachments. Supports digest mode for daily briefings. Triggers: check email, read inbox, new mail, email digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shimonxin](https://clawhub.ai/user/shimonxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect IMAP mailboxes, read and search messages, generate daily email digests, mark messages read or unread, and download attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs IMAP credentials and can read mailbox contents.

Mitigation: Install only in trusted environments, use least-privilege or app-specific credentials when available, and rotate or revoke tokens periodically.

Risk: TLS certificate verification is disabled in the IMAP connection.

Mitigation: Enable certificate verification and review IMAP host settings before using the skill with real mailbox credentials.

Risk: Email-derived digests and attachment files may be saved to local workspace storage.

Mitigation: Review storage locations, retention, and access controls before processing sensitive mailbox content.

Risk: Attachment downloads can use sender-provided filenames.

Mitigation: Sanitize attachment filenames and constrain downloads to an expected output directory before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shimonxin/skills/imap-mailbox)
- [Publisher profile](https://clawhub.ai/user/shimonxin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Plain text and Markdown summaries, with shell command usage and downloaded local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write email digests and attachment files to local workspace storage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
