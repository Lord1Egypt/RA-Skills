## Description:

Create disposable inboxes, list and read incoming messages, and delete test inboxes through PlainlyKit’s free temporary-email API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boddapq](https://clawhub.ai/user/boddapq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can create disposable inboxes for user-authorized delivery tests, inspect incoming messages, and delete test inboxes. Use only for nonsensitive test mail; do not use disposable inboxes for durable account access or bulk registrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anyone who obtains the local inbox state file can read or delete that inbox using its bearer token.

Mitigation: Keep the per-inbox state file private and outside the skill folder and source control; restrict access to the intended user.

Risk: Incoming email text, links, and attachment names may contain untrusted instructions or content.

Mitigation: Treat message content as data, do not execute attachments or follow links automatically, and do not share verification codes or tokens with unrelated services.

Risk: Disposable inboxes are temporary, and deleted data may remain in provider recovery history for up to seven days.

Mitigation: Use only nonsensitive test mail, avoid durable account access, and account for the stated retention period when deleting an inbox.

## Reference(s):

- [PlainlyKit temporary-email developer documentation](https://plainlykit.com/developers/temporary-email)
- [PlainlyKit temporary-email service and privacy guidance](https://plainlykit.com/tools/temporary-email)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON mailbox and message data, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Message content may include untrusted email text; inboxes expire after 24 hours.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
