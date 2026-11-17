## Description:

Use for Sendbird Chat Platform API v3 server-side integration - users, group channels, open channels, messages, metadata, moderation, bots, announcements, and statistics - with caller-owned application credentials and preview-first mutation confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover and apply Sendbird Chat Platform API v3 endpoints for server-side user, channel, message, moderation, bot, announcement, and statistics workflows. It helps them preview caller-directed requests, manage local credentials, and require explicit confirmation before mutations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-owned Sendbird API tokens could be exposed through logs, examples, committed files, or broad local environment access.

Mitigation: Use least-privilege Sendbird tokens where possible, keep tokens out of logs and examples, and store credentials only in the caller's local environment or browser session.

Risk: Sendbird management actions such as sending messages, deleting channels, blocking users, or scheduling announcements can change application state.

Mitigation: Preview the exact request path, body, and side effects locally, then require explicit caller confirmation before executing mutations.

Risk: Unpinned Pontx tooling could introduce supply-chain uncertainty.

Mitigation: Pin and verify Pontx package versions before installation or use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and code identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local request previews, endpoint-resolution guidance, and confirmation prompts before API mutations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
