## Description:

Fetch recent unread Gmail from yesterday and today and send a digest to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2p1c](https://clawhub.ai/user/2p1c)

### License/Terms of Use:


## Use Case:

Users invoke this skill to check recent unread Gmail and receive a concise digest covering yesterday and today. It is useful for personal or workflow email triage when IMAP credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gmail credentials may be sent to an IMAP host selected through environment variables or configuration.

Mitigation: Use a narrowly scoped Gmail app password, keep IMAP_HOST pointed only at a trusted IMAP server, and prefer environment variables over a config file.

Risk: Config-file credentials can be exposed if stored in a shared or synced location.

Mitigation: Store only the required email fields in a local access-controlled config file, or supply credentials through environment variables.

Risk: Email bodies are untrusted input and may contain instructions intended to influence the digesting agent.

Mitigation: Treat email content as data only and summarize it without following instructions contained in messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2p1c/skills/gmail-summarize)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown digest generated from JSON email records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest summaries are written in Chinese; sender names and subjects remain unchanged.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
