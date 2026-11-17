## Description:

Enables agents to use a configured mailbox to receive verification codes, send and receive email, monitor and search inboxes, download attachments, view threads, extract structured data, manage mailbox settings, and configure webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[digidai](https://clawhub.ai/user/digidai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent complete email-based registration flows, retrieve verification codes, manage mailbox content, and automate mailbox-related workflows through a configured mail API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read mailbox content that may include important records or account-recovery messages.

Mitigation: Use a dedicated low-risk mailbox and avoid connecting accounts that receive sensitive records or recovery messages.

Risk: The agent can delete emails and change mailbox or webhook routing settings.

Mitigation: Require explicit user confirmation before deletes, mailbox pause or resume actions, webhook updates, and route changes.

Risk: The authentication token enables broad mailbox actions through the configured mail API.

Mitigation: Restrict who can access MAILS_AUTH_TOKEN and rotate it if it may have been exposed.

Risk: Verification codes or mailbox contents could be forwarded to untrusted destinations.

Mitigation: Avoid forwarding codes or message contents to untrusted recipients, tools, or webhook URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/digidai/skills/mails-for-agent)
- [Publisher profile](https://clawhub.ai/user/digidai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown with HTTP request guidance and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAILS_API_URL, MAILS_AUTH_TOKEN, and MAILS_MAILBOX environment variables.]

## Skill Version(s):

1.8.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
