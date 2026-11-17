## Description:

Manage voice agents, place and transfer calls, handle telephony events, and retrieve call records using the NoddyAI API at graine.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabh171998](https://clawhub.ai/user/rishabh171998)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to construct authorized HTTP requests for Graine/NoddyAI voice-agent management, outbound and inbound telephony, batch calls, call records, token management, and webhook handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful telephony and account operations could place calls, transfer live calls, revoke tokens, delete agents, or change webhook URLs without sufficient user intent.

Mitigation: Require explicit user confirmation before outbound or batch calls, transfers, token revocation, agent deletion, and inbound webhook URL changes; summarize affected numbers, agent IDs, tokens, or URLs before acting.

Risk: Phone numbers, CSV uploads, call transcripts, recordings, webhook payloads, API keys, and organization IDs are sensitive data.

Mitigation: Use only credentials supplied by the user or host configuration, never embed placeholder secrets, redact Bearer tokens when echoing headers, and treat call artifacts and webhook payloads according to the user's consent, security, and retention obligations.

Risk: Webhook configuration can send call event data to an unintended external endpoint.

Mitigation: Set or change webhook URLs only after the user confirms the endpoint is under their control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rishabh171998/skills/graineai)
- [Skill instructions](artifact/SKILL.md)
- [Endpoint reference](artifact/endpoints.md)
- [Request examples](artifact/examples.md)
- [Webhook payloads](artifact/webhooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP request examples, curl commands, and JSON bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied Graine/NoddyAI API credentials and org_id; Bearer tokens should be redacted if headers are shown.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
