## Description:

NexLink is an enterprise connector for Nextcloud, Microsoft Exchange, and YouTube that supports email, calendar, tasks, file management, document understanding, transcript extraction, contacts, analytics, security confirmations, and least-privilege defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asistent-alex](https://clawhub.ai/user/asistent-alex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and team assistants use NexLink to connect Exchange, Nextcloud, and YouTube workflows for mail, calendar, task, file, contact, transcript, and document operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exchange and Nextcloud credentials can grant broad access to mail, files, contacts, tasks, and calendars.

Mitigation: Use dedicated least-privilege service accounts, scoped Nextcloud app passwords, and HTTPS endpoints for every deployment.

Risk: Attachment downloads, public share links, and destructive file, contact, or task operations can affect or expose the wrong data if the target is not checked.

Mitigation: Review exact targets before execution and use per-command confirmation bypasses only after the requested operation has been verified.

Risk: Untrusted local configuration can redirect the connector or expose sensitive operational settings.

Mitigation: Review local config files before use, keep secrets out of version control, and prefer managed secrets for credentials.

## Reference(s):

- [NexLink Setup Guide](artifact/references/setup.md)
- [NexLink Security Best Practices](artifact/references/security-best-practices.md)
- [NexLink ClawHub Listing](https://clawhub.ai/asistent-alex/skills/nexlink)
- [Firma de AI Homepage](https://firmade.ai)
- [NexLink Repository](https://github.com/asistent-alex/openclaw-nexlink)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, modify, download, upload, share, or delete data in connected Exchange and Nextcloud accounts when explicitly commanded.]

## Skill Version(s):

0.15.9 (source: frontmatter, changelog, clawhub metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
