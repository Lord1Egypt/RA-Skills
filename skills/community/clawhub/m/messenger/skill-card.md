## Description: <br>
OpenClaw skill for Facebook Messenger Platform workflows, including messaging, webhooks, and Page inbox operations using direct HTTPS requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan Facebook Messenger Platform integrations, including Send API messaging, webhook handling, permissions, token handling, and conversation UX guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: App secrets, Page access tokens, verify tokens, webhook payloads, and live recipient IDs are sensitive. <br>
Mitigation: Treat these values as secrets, avoid logging tokens or private conversation data, and use least-privilege permissions. <br>
Risk: Message-sending examples can affect real Messenger users if tested against production Pages or live recipients. <br>
Mitigation: Test with a development Page or approved recipients before sending production messages. <br>
Risk: Webhook handlers can accept spoofed or replayed traffic if verification is incomplete. <br>
Mitigation: Validate webhook signatures, acknowledge events quickly, and keep handlers idempotent for retries. <br>


## Reference(s): <br>
- [Messenger API Overview](references/messenger-api-overview.md) <br>
- [Messaging](references/messaging.md) <br>
- [Webhooks](references/webhooks.md) <br>
- [Permissions and Tokens](references/permissions-and-tokens.md) <br>
- [Request Templates](references/request-templates.md) <br>
- [Conversation Patterns](references/conversation-patterns.md) <br>
- [Webhook Event Map](references/webhook-event-map.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/codedao12/messenger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include direct HTTPS request templates, permissions checklists, webhook handling guidance, and operational guardrails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
