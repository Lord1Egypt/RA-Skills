## Description:

OpenClaw skill for Facebook Messenger Platform workflows, including messaging, webhooks, and Page inbox operations using direct HTTPS requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and implement Facebook Messenger Platform workflows for Page messaging, webhook handling, Send API payloads, and operational guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messenger workflows require Page access tokens and App Secrets, which can expose accounts if logged or shared.

Mitigation: Keep tokens and secrets out of logs, rotate them when possible, and use least-privilege permissions.

Risk: Webhook endpoints can receive forged or replayed events if validation is skipped.

Mitigation: Validate X-Hub-Signature-256 with the App Secret and keep handlers idempotent for retries.

## Reference(s):

- [Messenger Skill Page](https://clawhub.ai/codedao12/skills/messenger)
- [Messenger Platform Overview](references/messenger-api-overview.md)
- [Messaging](references/messaging.md)
- [Webhooks](references/webhooks.md)
- [Permissions and Tokens](references/permissions-and-tokens.md)
- [HTTP Request Templates](references/request-templates.md)
- [Conversation Patterns](references/conversation-patterns.md)
- [Webhook Event Map](references/webhook-event-map.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP request examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Messenger workflow plans, permissions checklists, request payloads, and operational guardrails.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
