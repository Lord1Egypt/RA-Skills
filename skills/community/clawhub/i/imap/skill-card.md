## Description: <br>
Read, search, and sync IMAP mailboxes with UID-safe fetches, precise filters, and attachment-aware workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and mailbox administrators use this skill to inspect IMAP mailboxes, search and fetch messages, triage attachments, and manage incremental sync state while keeping mailbox mutations explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox access can expose sensitive message metadata, message bodies, attachments, and authentication flows. <br>
Mitigation: Use only trusted mailbox endpoints and local credential flows, keep secrets out of ~/imap/, and fetch only the data required for the current task. <br>
Risk: Mailbox-changing operations such as flag updates, moves, deletes, and expunge can alter user-visible mail state. <br>
Mitigation: Keep read-only behavior as the default and require explicit confirmation or a standing policy before any mutating action. <br>
Risk: Incremental sync can skip or duplicate messages if volatile sequence numbers or stale cursors are used. <br>
Mitigation: Use UID-based checkpoints, track UIDVALIDITY and MODSEQ when available, and rescan when UIDVALIDITY changes. <br>
Risk: Attachments may contain untrusted or unexpectedly large content. <br>
Mitigation: Inspect MIME structure and attachment metadata first, then download only requested parts without opening or executing downloaded files automatically. <br>


## Reference(s): <br>
- [ClawHub IMAP Skill](https://clawhub.ai/ivangdavila/imap) <br>
- [Skill Homepage](https://clawic.com/skills/imap) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Setup - IMAP](artifact/setup.md) <br>
- [Search and Fetch](artifact/search-and-fetch.md) <br>
- [State, Flags, and Sync Rules](artifact/state-and-flags.md) <br>
- [Attachments and MIME Handling](artifact/attachments.md) <br>
- [Troubleshooting](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline commands, mailbox plans, result summaries, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local memory templates and mailbox workflow notes under ~/imap/ when the user enables durable memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
