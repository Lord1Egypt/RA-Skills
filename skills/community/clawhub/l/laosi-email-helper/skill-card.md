## Description:

Email Helper Pro helps agents draft, template, send, read, search, and archive email using SMTP and IMAP with local draft persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and external agents can use this skill to prepare email drafts, apply common message templates, send messages through SMTP, inspect recent inbox messages through IMAP, and keep draft records locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access mailboxes and send email.

Mitigation: Use only scoped or app-specific credentials and require explicit confirmation before any send or inbox-read action.

Risk: Message drafts may be persisted locally in plaintext.

Mitigation: Avoid sensitive draft content unless local storage controls are acceptable, and remove drafts that should not remain on disk.

Risk: SMTP login can be used without TLS.

Mitigation: Keep TLS enabled and do not submit real credentials over non-TLS SMTP connections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-email-helper)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown with Python and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include email draft content, SMTP/IMAP configuration examples, and mailbox operation guidance.]

## Skill Version(s):

2.0.0 (source: server release metadata, frontmatter, and hub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
