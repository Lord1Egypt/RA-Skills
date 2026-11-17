## Description:

AgentMail Email helps agents create and manage dedicated AgentMail inboxes, send and receive email, and configure webhook-based email workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidsteelerose](https://clawhub.ai/user/davidsteelerose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to provision AgentMail inboxes, send and receive messages, and build webhook-driven email workflows for support, task intake, document processing, or agent identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook examples and test servers can expose email data or trigger authenticated email actions from unverified inbound requests.

Mitigation: Verify webhook signatures, keep test receivers local unless intentionally exposed, and require human review before inbound emails create issues, tasks, replies, or other external actions.

Risk: Inbound email content can carry prompt injection or untrusted instructions into an agent workflow.

Mitigation: Use sender and inbox allowlists, mark email content as untrusted input, and isolate review workflows before delivering email content to an agent.

Risk: Email payloads may contain sensitive message bodies, attachments, addresses, or API-related metadata.

Mitigation: Avoid logging full payloads, protect AGENTMAIL_API_KEY, and review examples before installing or copying them into production handlers.

## Reference(s):

- [AgentMail Skill Page](https://clawhub.ai/davidsteelerose/skills/k2ljl-agentmail)
- [AgentMail Console](https://console.agentmail.to)
- [AgentMail API Reference](references/API.md)
- [AgentMail Webhooks Guide](references/WEBHOOKS.md)
- [AgentMail Usage Examples](references/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AgentMail API key for live API operations.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
