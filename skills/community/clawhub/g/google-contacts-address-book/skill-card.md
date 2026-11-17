## Description:

Google Contacts API integration with managed OAuth for searching, inspecting, creating, and updating contacts and contact groups stored in Google People.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to connect a Google account through ClawLink, inspect Google Contacts data, and perform confirmed contact, group, photo, and batch changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact, group, photo, and batch write operations can change or delete data in the connected Google account.

Mitigation: Require clear user confirmation before any write or delete operation, including the target resource and intended effect.

Risk: Connecting the wrong Google account could expose or modify unintended contacts.

Mitigation: Connect only the intended Google account and review the OAuth scopes during pairing.

Risk: The skill relies on the ClawLink plugin and hosted OAuth connection.

Mitigation: Install only if the user trusts ClawLink and the ClawHub plugin source.

## Reference(s):

- [Google People API Overview](https://developers.google.com/people/api/rest)
- [Google Contacts API](https://developers.google.com/contacts/v3)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-contacts-address-book)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-contacts-address-book)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Google account through ClawLink; write operations require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release evidence, released 2026-06-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
