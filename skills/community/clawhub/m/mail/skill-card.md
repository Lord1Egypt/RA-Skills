## Description:

Execute email operations with platform-specific optimizations and secure credential handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to search, read, draft, and send email through himalaya or Apple Mail while preserving explicit review before sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help an agent read and search mailbox contents, which may expose sensitive email data.

Mitigation: Install only when comfortable with mailbox access and review any mailbox-derived results before acting on them.

Risk: The skill can prepare outgoing email, creating a risk of accidental or incorrect sends.

Mitigation: Use the documented draft-review-send workflow and approve sends only after reviewing the complete recipient, subject, and body.

Risk: Credential setup guidance involves mailbox authentication secrets.

Mitigation: Create or update Keychain credentials yourself when possible and use app passwords or OAuth tokens rather than regular account passwords.

Risk: Floating himalaya install commands may resolve to changed behavior over time.

Mitigation: Prefer a trusted pinned himalaya version for repeatable behavior.

## Reference(s):

- [Apple Mail SQLite Queries](artifact/apple-mail.md)
- [himalaya CLI Patterns](artifact/himalaya.md)
- [Email Send Protocol](artifact/sending.md)
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/mail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-review-send workflow; outgoing messages require explicit user approval before send.]

## Skill Version(s):

1.2.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
