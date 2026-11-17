## Description:

Gmail API integration with managed OAuth for reading, sending, and managing emails, threads, labels, and drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbyzzhao](https://clawhub.ai/user/bobbyzzhao)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect an agent to Gmail through Maton's managed OAuth service for reading, sending, searching, labeling, drafting, and managing messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support powerful Gmail actions, including sending messages, sending drafts, modifying labels, trashing messages, and deleting OAuth connections.

Mitigation: Require explicit user approval of the exact target, content, and intended operation before any send, draft-send, label modification, trash, or connection deletion action.

Risk: The skill depends on MATON_API_KEY and unsafe handling could expose the key in logs or transcripts.

Mitigation: Do not print or share MATON_API_KEY; use a non-disclosing presence check and rotate the key if it appears in logs or transcripts.

Risk: Gmail access is routed through Maton's managed OAuth service.

Mitigation: Install only if the user trusts Maton with Gmail access and is comfortable routing Gmail operations through that service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bobbyzzhao/skills/gmail-1-0-6)
- [Gmail API Overview](https://developers.google.com/gmail/api/reference/rest)
- [Gmail Users Messages: List](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list)
- [Gmail Users Messages: Get](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get)
- [Gmail Users Messages: Send](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send)
- [Gmail Users Threads: List](https://developers.google.com/gmail/api/reference/rest/v1/users.threads/list)
- [Gmail Users Labels: List](https://developers.google.com/gmail/api/reference/rest/v1/users.labels/list)
- [Gmail Users Drafts: Create](https://developers.google.com/gmail/api/reference/rest/v1/users.drafts/create)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code blocks, HTTP endpoint examples, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and MATON_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
