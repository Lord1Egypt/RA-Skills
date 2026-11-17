## Description:

Gmail Litiao helps agents access Gmail through Maton managed OAuth to read, send, and manage messages, threads, labels, and drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to guide Gmail mailbox operations through the Maton gateway, including reading messages, sending email, managing drafts, labels, threads, trash, and OAuth connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact mailbox actions such as sending drafts, modifying labels, and trashing messages.

Mitigation: Require explicit user review before sending email, sending drafts, modifying labels, deleting OAuth connections, or moving messages to trash.

Risk: The skill depends on MATON_API_KEY and includes troubleshooting guidance that can print the credential.

Mitigation: Avoid running or sharing commands that print MATON_API_KEY; verify configuration without exposing the token in logs or chat output.

Risk: Connected Gmail mailboxes may contain sensitive personal or business email.

Mitigation: Install and use the skill only for accounts where Maton API credential access to the connected mailbox is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/gmail-litiao)
- [Gmail API REST reference](https://developers.google.com/gmail/api/reference/rest)
- [Gmail users.messages.list](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list)
- [Gmail users.messages.get](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get)
- [Gmail users.messages.send](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send)
- [Gmail users.threads.list](https://developers.google.com/gmail/api/reference/rest/v1/users.threads/list)
- [Gmail users.labels.list](https://developers.google.com/gmail/api/reference/rest/v1/users.labels/list)
- [Gmail users.drafts.create](https://developers.google.com/gmail/api/reference/rest/v1/users.drafts/create)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline HTTP examples and Python or JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Gmail OAuth connection]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
