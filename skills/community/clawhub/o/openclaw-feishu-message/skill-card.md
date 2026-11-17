## Description:

Send Feishu/Lark direct messages and work follow-ups from OpenClaw. Use when the user wants to search for a person in Feishu/Lark, resolve a user, create a 1:1 chat, or send a bot-authored follow-up message about work done, status updates, reminders, or polite nudges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systransform88](https://clawhub.ai/user/systransform88)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to resolve Feishu/Lark contacts, create direct chats when requested, and send bot-authored work messages or follow-ups from OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled plaintext contact-cache data can expose personal contact identifiers.

Mitigation: Remove the bundled contact-cache data before distribution or installation and avoid storing sensitive contact details unless the deployment has an approved retention policy.

Risk: The skill can send real Feishu/Lark messages, and sending is enabled by default when configured.

Mitigation: Require preview and explicit confirmation before sending, and set sending to disabled until an operator intentionally enables it.

Risk: Weak or ambiguous recipient resolution can send a message to the wrong person.

Mitigation: Reject ambiguous recipient matches and require a confirmed unique recipient before sending.

## Reference(s):

- [API notes](references/api-notes.md)
- [ClawHub skill page](https://clawhub.ai/systransform88/skills/openclaw-feishu-message)

## Skill Output:

**Output Type(s):** [Text, API calls, Configuration, Guidance]

**Output Format:** [Text responses with JSON-formatted tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform Feishu/Lark employee lookup, chat creation, message preview, and bot message sending when configured with tenant credentials and scopes.]

## Skill Version(s):

0.1.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
