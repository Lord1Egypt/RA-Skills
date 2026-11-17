## Description:

Email for AI agents. Create mailboxes, send and receive emails via API. No browser, no OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishavmukherji](https://clawhub.ai/user/rishavmukherji)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to create agent mailboxes, send email, receive and search inbox messages, and configure webhooks through Neynar's hosted REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring inbox polling can keep using the hosted email API key in the background if scheduled without limits or cleanup.

Mitigation: Approve polling schedules explicitly, set an end time, keep the API key in secure storage, and know how to remove the recurring task or rotate the key.

Risk: Mailbox API keys are returned only once and cannot be recovered.

Mitigation: Store the API key immediately in a secure secret store and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rishavmukherji/skills/neynar-inbox)
- [Publisher profile](https://clawhub.ai/user/rishavmukherji)
- [Neynar Inbox homepage](https://email.neynar.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include API endpoints, request headers, payload examples, polling setup, webhook configuration, and API-key handling notes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
