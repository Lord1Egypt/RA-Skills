## Description:

Read, search, and sync IMAP mailboxes with UID-safe fetches, precise filters, and attachment-aware workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect IMAP mailboxes, search and fetch messages safely, triage attachments, and maintain incremental sync state across providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox metadata, message bodies, and attachments may contain sensitive personal or business information.

Mitigation: Use the skill only with trusted mailboxes and credential flows, fetch the minimum data needed, and keep network activity scoped to the configured IMAP server.

Risk: Mailbox state can change if messages are marked seen, moved, deleted, flagged, or expunged during a review.

Mitigation: Default to read-safe inspection, preview affected UIDs before mutation, and require explicit user approval or a confirmed standing policy for state-changing operations.

Risk: Large or unnecessary fetches can expose more mailbox content than the task requires.

Mitigation: Start with server-side search, counts, flags, envelopes, headers, and MIME metadata, then fetch bodies or attachments only when needed.

Risk: Incremental sync can skip or duplicate messages if sequence numbers or stale cursors are used.

Mitigation: Use UIDs, track UIDVALIDITY and MODSEQ where available, and rebuild sync state when UIDVALIDITY changes.

Risk: Downloaded attachments may be unsafe to open or execute.

Mitigation: Treat attachments as untrusted content, inspect MIME metadata first, and do not auto-open or execute downloaded files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/imap)
- [Skill homepage](https://clawic.com/skills/imap)
- [Setup - IMAP](artifact/setup.md)
- [Search and Fetch](artifact/search-and-fetch.md)
- [State, Flags, and Sync Rules](artifact/state-and-flags.md)
- [Attachments and MIME Handling](artifact/attachments.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with mailbox plans, command examples, triage reports, and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IMAP search filters, UID-safe fetch plans, attachment triage details, and local memory templates; mailbox data is fetched only from the user-configured IMAP endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
